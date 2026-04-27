# MHS Knowledge Base — Belge 2: Teknik Mimari & Veri Modeli

## 1. SİSTEM MİMARİSİ GENEL BAKIŞ

```
┌─────────────────────────────────────────────────┐
│                   MHS PLATFORM                  │
├─────────────┬───────────────┬───────────────────┤
│    Web App     │   Admin Panel                  │
│   (Next.js)    │   (Next.js)                    │
└──────┬──────┴───────┬───────┴──────┬────────────┘
       │              │              │
       └──────────────▼──────────────┘
                 API Gateway
              (Kong / AWS API GW)
       ┌──────────────┼──────────────┐
       ▼              ▼              ▼
  Auth Service   Core API      ML Service
  (Node.js)     (FastAPI)      (Python)
       │              │              │
       ▼              ▼              ▼
  Auth DB      PostgreSQL    ML Models
  (Redis)      + Neo4j       (HuggingFace)
                    │
                    ▼
              ClickHouse
              (Analytics)
```

## 2. VERİTABANI ŞEMASI

### Kullanıcı Tablosu (PostgreSQL)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    display_name VARCHAR(200),
    country_code CHAR(2),
    city VARCHAR(100),
    birth_year SMALLINT,
    profession VARCHAR(100),
    education_level VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_verified BOOLEAN DEFAULT FALSE,
    privacy_settings JSONB DEFAULT '{
        "profile_public": true,
        "score_visible": true,
        "activities_visible": true,
        "hidden_factors_visible_to_self": true
    }'
);

CREATE TABLE mhs_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    score_date DATE NOT NULL,
    
    -- Temel kategoriler (0–200 her biri)
    social_impact_score DECIMAL(6,2) DEFAULT 0,
    environmental_score DECIMAL(6,2) DEFAULT 0,
    knowledge_innovation_score DECIMAL(6,2) DEFAULT 0,
    economic_contribution_score DECIMAL(6,2) DEFAULT 0,
    cultural_artistic_score DECIMAL(6,2) DEFAULT 0,
    civic_political_score DECIMAL(6,2) DEFAULT 0,
    
    -- Hesaplanmış ham skor
    raw_mhs DECIMAL(7,2) DEFAULT 0,
    
    -- Gizli çarpanlar (sadece ML servisi okuyabilir)
    carbon_penalty DECIMAL(5,2) DEFAULT 0,
    toxicity_penalty DECIMAL(5,2) DEFAULT 0,
    network_multiplier DECIMAL(4,3) DEFAULT 1.0,
    consistency_multiplier DECIMAL(4,3) DEFAULT 1.0,
    geo_equity_multiplier DECIMAL(4,3) DEFAULT 1.0,
    
    -- Final skor
    final_mhs DECIMAL(7,2) DEFAULT 0,
    mhs_level VARCHAR(30),
    
    percentile_global DECIMAL(5,2),
    percentile_country DECIMAL(5,2),
    percentile_age_group DECIMAL(5,2),
    percentile_profession DECIMAL(5,2)
);

CREATE TABLE activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    activity_type VARCHAR(50) NOT NULL,
    -- Types: volunteer, donation, academic_pub, open_source, 
    --        civic_engagement, environmental_action, art_creation,
    --        job_creation, community_leadership, conflict_resolution
    
    category VARCHAR(50),
    title TEXT,
    description TEXT,
    evidence_url TEXT,
    evidence_file_path TEXT,
    
    impact_score_awarded DECIMAL(5,2),
    verified_by VARCHAR(50), -- 'system', 'partner_ngo', 'peer_review', 'manual'
    verification_status VARCHAR(20) DEFAULT 'pending',
    
    started_at DATE,
    ended_at DATE,
    is_ongoing BOOLEAN DEFAULT FALSE,
    
    metadata JSONB, -- platform-specific data
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE connected_platforms (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    platform_name VARCHAR(50) NOT NULL,
    platform_user_id VARCHAR(200),
    access_token_hash VARCHAR(255), -- sadece hash saklanır
    scopes_granted TEXT[],
    last_synced_at TIMESTAMPTZ,
    sync_frequency_hours INTEGER DEFAULT 24,
    is_active BOOLEAN DEFAULT TRUE
);
```

### Neo4j Grafik Şeması (Sosyal Ağ)

```cypher
// Kullanıcı Düğümü
CREATE (u:User {
  id: uuid,
  mhs: float,
  country: string,
  impact_category: string
})

// Takip ilişkisi
(u1:User)-[:FOLLOWS {since: date}]->(u2:User)

// Aktivite ağı — başkalarını etkileyen aktiviteler
(u:User)-[:CREATED]->(a:Activity {type, impact, reach})
(a:Activity)-[:BENEFITED]->(population:Group {size, location})

// Organizasyon üyeliği
(u:User)-[:MEMBER_OF {role, since}]->(org:Organization {name, type, verified})

// Etki zinciri
(u1:User)-[:INSPIRED]->(u2:User) // u1'in aktivitesi u2'yi harekete geçirdi
```

## 3. SKOR HESAPLAMA MOTORU (Python)

```python
from dataclasses import dataclass
from typing import Optional
import numpy as np

@dataclass
class UserProfile:
    user_id: str
    country_code: str
    age: int
    
@dataclass
class RawCategoryScores:
    social_impact: float  # 0-200
    environmental: float  # 0-200
    knowledge_innovation: float  # 0-200
    economic_contribution: float  # 0-200
    cultural_artistic: float  # 0-200
    civic_political: float  # 0-200

@dataclass
class HiddenFactors:
    carbon_footprint_kg_yearly: float
    toxicity_index: float  # 0-1, NLP-based
    financial_charity_ratio: float  # donations/income
    network_reach: int  # unique people reached
    consistency_months: int  # months of continuous activity

class MHSCalculator:
    
    CATEGORY_WEIGHTS = {
        'social_impact': 0.25,
        'environmental': 0.20,
        'knowledge_innovation': 0.20,
        'economic_contribution': 0.15,
        'cultural_artistic': 0.10,
        'civic_political': 0.10
    }
    
    # Karbon ceza eşikleri (kg CO2/yıl)
    CARBON_THRESHOLDS = {
        'very_low': 2000,    # 0 ceza
        'low': 5000,         # -5 puan
        'medium': 10000,     # -20 puan
        'high': 20000,       # -50 puan
        'very_high': 50000   # -100 puan
    }
    
    def calculate_raw_score(self, scores: RawCategoryScores) -> float:
        """Kategori ağırlıklarıyla ham skoru hesapla"""
        weighted = (
            scores.social_impact * self.CATEGORY_WEIGHTS['social_impact'] +
            scores.environmental * self.CATEGORY_WEIGHTS['environmental'] +
            scores.knowledge_innovation * self.CATEGORY_WEIGHTS['knowledge_innovation'] +
            scores.economic_contribution * self.CATEGORY_WEIGHTS['economic_contribution'] +
            scores.cultural_artistic * self.CATEGORY_WEIGHTS['cultural_artistic'] +
            scores.civic_political * self.CATEGORY_WEIGHTS['civic_political']
        )
        # Ham skor max 1000
        return min(weighted * 5, 1000)
    
    def calculate_hidden_adjustments(
        self, 
        raw_score: float,
        hidden: HiddenFactors,
        profile: UserProfile
    ) -> dict:
        """Gizli faktörleri hesapla"""
        
        # Karbon cezası
        carbon_penalty = self._get_carbon_penalty(hidden.carbon_footprint_kg_yearly)
        
        # Toksiklik cezası
        toxicity_penalty = hidden.toxicity_index * 80  # max -80 puan
        
        # Ağ çarpanı (logaritmik)
        network_multiplier = 1 + (np.log10(max(hidden.network_reach, 1)) * 0.05)
        network_multiplier = min(network_multiplier, 1.5)  # max 1.5x
        
        # Tutarlılık çarpanı
        consistency_multiplier = 1 + (min(hidden.consistency_months, 120) / 400)
        
        # Coğrafi eşitlik çarpanı
        geo_multiplier = self._get_geo_multiplier(profile.country_code)
        
        return {
            'carbon_penalty': carbon_penalty,
            'toxicity_penalty': toxicity_penalty,
            'network_multiplier': network_multiplier,
            'consistency_multiplier': consistency_multiplier,
            'geo_multiplier': geo_multiplier
        }
    
    def calculate_final_mhs(
        self,
        scores: RawCategoryScores,
        hidden: HiddenFactors,
        profile: UserProfile
    ) -> float:
        """Final MHS skoru"""
        raw = self.calculate_raw_score(scores)
        adj = self.calculate_hidden_adjustments(raw, hidden, profile)
        
        adjusted = (raw 
                   * adj['network_multiplier'] 
                   * adj['consistency_multiplier']
                   * adj['geo_multiplier'])
        
        final = adjusted - adj['carbon_penalty'] - adj['toxicity_penalty']
        
        return max(0, min(1000, round(final, 1)))
    
    def get_level(self, score: float) -> str:
        levels = [
            (0, 'Awakening'),
            (101, 'Contributor'),
            (251, 'Changemaker'),
            (501, 'Catalyst'),
            (701, 'Champion'),
            (851, 'Luminary'),
            (951, 'Humanity Legend')
        ]
        level = 'Awakening'
        for threshold, name in levels:
            if score >= threshold:
                level = name
        return level
    
    def _get_carbon_penalty(self, kg_yearly: float) -> float:
        if kg_yearly <= 2000: return 0
        if kg_yearly <= 5000: return 5
        if kg_yearly <= 10000: return 20
        if kg_yearly <= 20000: return 50
        return 100
    
    def _get_geo_multiplier(self, country_code: str) -> float:
        # Düşük gelirli ülkelerden gelen katkılar daha yüksek değer taşır
        high_equity_countries = {'NG', 'ET', 'SD', 'BD', 'PK', 'KH'}
        medium_equity_countries = {'TR', 'BR', 'IN', 'ID', 'PH'}
        
        if country_code in high_equity_countries:
            return 1.3
        elif country_code in medium_equity_countries:
            return 1.1
        return 1.0
```

## 4. API TASARIMI

### REST API Endpoints

```
# Auth
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/oauth/{platform}     # LinkedIn, GitHub, Google

# User Profile
GET    /api/v1/users/{username}           # Public profile
GET    /api/v1/users/me                   # Private profile with hidden factors
PATCH  /api/v1/users/me                   # Update profile

# MHS Score
GET    /api/v1/score/me                   # Full score breakdown
GET    /api/v1/score/me/history           # Historical scores
GET    /api/v1/score/{username}           # Other user's public score
POST   /api/v1/score/recalculate          # Trigger recalculation

# Activities
GET    /api/v1/activities/me
POST   /api/v1/activities
PATCH  /api/v1/activities/{id}
DELETE /api/v1/activities/{id}
POST   /api/v1/activities/{id}/verify     # Request verification

# Leaderboard & Comparison
GET    /api/v1/leaderboard/global
GET    /api/v1/leaderboard/country/{code}
GET    /api/v1/compare?users=id1,id2,id3
GET    /api/v1/analytics/demographics
GET    /api/v1/analytics/category-breakdown

# Platform Connections
GET    /api/v1/connections
POST   /api/v1/connections/{platform}
DELETE /api/v1/connections/{platform}
POST   /api/v1/connections/{platform}/sync

# Feed & Social
GET    /api/v1/feed                       # Impact feed
POST   /api/v1/feed/posts
GET    /api/v1/challenges                 # Active global challenges
POST   /api/v1/challenges/{id}/join
```

## 5. ML/AI SERVİSLERİ

### A. Toksiklik Analizi (NLP)
```python
from transformers import pipeline

class ToxicityAnalyzer:
    def __init__(self):
        self.classifier = pipeline(
            "text-classification",
            model="unitary/toxic-bert",
            top_k=None
        )
    
    def analyze_user_posts(self, posts: list[str]) -> float:
        """
        Returns toxicity_index: 0 (temiz) to 1 (yüksek toksiklik)
        """
        if not posts:
            return 0.0
        
        scores = []
        for post in posts[:100]:  # Son 100 post
            result = self.classifier(post[:512])[0]
            toxic_score = next(
                (r['score'] for r in result if r['label'] == 'toxic'), 0
            )
            scores.append(toxic_score)
        
        return np.mean(scores)
```

### B. Karbon Ayak İzi Hesaplama (Climatiq API)
```python
import httpx

class CarbonCalculator:
    BASE_URL = "https://beta3.api.climatiq.io"
    
    async def calculate_flight_emissions(
        self, 
        from_airport: str, 
        to_airport: str, 
        passengers: int = 1
    ) -> float:
        """Returns kg CO2e"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.BASE_URL}/travel/flights",
                headers={"Authorization": f"Bearer {CLIMATIQ_API_KEY}"},
                json={
                    "legs": [{
                        "from": from_airport,
                        "to": to_airport,
                        "passengers": passengers,
                        "class": "economy"
                    }]
                }
            )
        return response.json()['co2e']
```

### C. Aktivite Doğrulama (Evidence Verification)
```python
class ActivityVerifier:
    
    VERIFICATION_METHODS = {
        'volunteer': ['ngo_api', 'certificate_ocr', 'peer_review'],
        'donation': ['receipt_ocr', 'bank_statement_api'],
        'academic': ['doi_lookup', 'google_scholar_api', 'orcid_api'],
        'open_source': ['github_api', 'gitlab_api'],
        'civic': ['government_api', 'electoral_roll']
    }
    
    async def verify(self, activity: dict) -> dict:
        method = self.VERIFICATION_METHODS.get(activity['type'], ['manual'])
        
        for m in method:
            result = await self._try_method(m, activity)
            if result['verified']:
                return {
                    'verified': True,
                    'method': m,
                    'confidence': result['confidence'],
                    'verified_at': datetime.utcnow()
                }
        
        # Otomatik doğrulama başarısız — peer review'a gönder
        return {'verified': False, 'method': 'manual_review_required'}
```

## 6. GİZLİLİK & GÜVENLİK MİMARİSİ

### Zero-Knowledge Gizli Faktörler

```python
# Gizli faktörler (karbon, toksisite, kredi) asla ham değer olarak saklanmaz
# Sadece etki bucketı saklanır

import hashlib
from enum import Enum

class CarbonBucket(Enum):
    EXCELLENT = "excellent"    # <2000 kg/yıl
    GOOD = "good"              # 2000-5000
    AVERAGE = "average"        # 5000-10000
    HIGH = "high"              # 10000-20000
    VERY_HIGH = "very_high"    # >20000

def get_hidden_factor_display(user_id: str, factor_name: str) -> dict:
    """
    Kullanıcı kendi gizli faktörlerini 'bucket' olarak görebilir
    Başkasının faktörleri hiç gösterilmez
    """
    return {
        'factor': factor_name,
        'level': CarbonBucket.GOOD.value,
        'description': 'Your carbon footprint is below average',
        'improvement_tips': ['...']
        # Tam sayısal değer asla döndürülmez
    }
```

### GDPR/KVKK Uyumu

```python
class PrivacyManager:
    
    async def export_user_data(self, user_id: str) -> dict:
        """GDPR Article 20 - Data Portability"""
        return {
            'profile': await self.get_profile(user_id),
            'activities': await self.get_activities(user_id),
            'scores_history': await self.get_scores(user_id),
            'connected_platforms': await self.get_connections(user_id),
            'export_date': datetime.utcnow().isoformat()
        }
    
    async def delete_user_data(self, user_id: str, reason: str):
        """GDPR Article 17 - Right to Erasure"""
        # Soft delete + 30 gün grace period
        await self.anonymize_profile(user_id)
        await self.revoke_all_tokens(user_id)
        await self.schedule_hard_delete(user_id, days=30)
    
    async def anonymize_for_analytics(self, user_data: dict) -> dict:
        """Analytics için kişisel veriyi anonim hale getir"""
        return {
            'country': user_data['country'],
            'age_group': self._age_group(user_data['age']),
            'mhs_score': user_data['mhs_score'],
            'category_scores': user_data['category_scores']
            # İsim, email, lokasyon KALDIRILDI
        }
```

## 7. GERÇEK ZAMANLI SKOR GÜNCELLEMESİ

```python
# Celery + Redis ile arka plan görevleri

from celery import Celery
from celery.schedules import crontab

app = Celery('mhs_tasks')

@app.task
def sync_platform_data(user_id: str, platform: str):
    """Belirli bir platform için kullanıcı verisini güncelle"""
    connector = PlatformConnectorFactory.get(platform)
    data = connector.fetch_new_activities(user_id)
    ActivityProcessor.process(user_id, data)
    ScoreRecalculator.recalculate(user_id)

@app.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    # Her gece yarısı tüm aktif kullanıcıları güncelle
    sender.add_periodic_task(
        crontab(hour=2, minute=0),
        batch_recalculate_scores.s(),
    )
    
    # Karbon verisi — haftalık güncelle
    sender.add_periodic_task(
        crontab(day_of_week=1, hour=3, minute=0),
        update_carbon_factors.s(),
    )
```

---

*Belge 3: UX/UI Tasarım Spesifikasyonları için bkz. MHS_KB_03_UX_Design.md*
