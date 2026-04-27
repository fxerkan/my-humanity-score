# MHS Knowledge Base v2.0 — Belge 3: Angel AI, Rozet Ekosistemi & UX

## 1. ANGEL AI — TAM SPESİFİKASYON

### Angel AI Kişiliği & Persona
Angel AI, platformun içine entegre edilmiş, açık kaynak LLM tabanlı AI asistanıdır.

**Persona:**
- İsim: **Angel** (platform genelinde böyle anılır)
- Ton: Sıcak, teşvik edici, yargılamayan, kültürel açıdan duyarlı
- Dil: Kullanıcının sistem diline otomatik uyum (30+ dil)
- Ayrım: Din, ırk, cinsiyet, milliyet bazlı hiçbir önyargı içermez
- Limit: Angel AI asla kişisel bilgi saklamaz; her oturum başı kullanıcı verisi profilden çekilir

### Teknik Mimari

```
┌───────────────────────────────────┐
│           ANGEL AI CORE           │
├────────────┬──────────────────────┤
│  GUARDIAN  │      MENTOR          │
│  Module    │      Module          │
├────────────┼──────────────────────┤
│ • Toxicity │ • Monthly Review     │
│ • Fake det.│ • Task Suggestion    │
│ • Anomaly  │ • Motivation Push    │
│ • DLP      │ • Similar Profiles   │
│ • Bot det. │ • Goal Tracking      │
└────────────┴──────────────────────┘
         │              │
    ┌────▼────┐    ┌────▼────┐
    │Guardian │    │ Mentor  │
    │  DB     │    │  DB     │
    │(threats)│    │(history)│
    └─────────┘    └─────────┘
```

### Guardian Module — Detaylı Kurallar

**Kural Seti (Örnek):**
```python
class AngelGuardian:
    
    THREAT_LEVELS = {
        'LOW': 1,       # uyar
        'MEDIUM': 2,    # filtrele + uyar
        'HIGH': 3,      # askıya al + kurul bildir
        'CRITICAL': 4   # anında engelle + log
    }
    
    def analyze_content(self, content: str, user_id: str) -> ThreatReport:
        threats = []
        
        # Toksiklik kontrolü
        tox_score = self.toxicity_model.predict(content)
        if tox_score > 0.85:
            threats.append(Threat('TOXIC_CONTENT', 'HIGH', tox_score))
        
        # Nefret söylemi (din, ırk, cinsiyet bazlı)
        hate_result = self.hate_speech_detector.detect(content)
        if hate_result.detected:
            threats.append(Threat('HATE_SPEECH', 'CRITICAL', hate_result.score))
        
        # Doxxing / kişisel bilgi ifşa
        if self.pii_detector.contains_pii(content):
            threats.append(Threat('PII_EXPOSURE', 'HIGH'))
        
        return ThreatReport(user_id, threats, datetime.utcnow())
    
    def analyze_profile(self, profile: UserProfile) -> FakeScore:
        """Sahte profil tespiti"""
        signals = {
            'account_age_hours': profile.age_hours,
            'activity_velocity': profile.activities_per_day,
            'profile_completeness': profile.completeness_pct,
            'ip_reputation': self.ip_check(profile.ip),
            'behavioral_pattern': self.behavior_model.predict(profile),
            'email_domain_trust': self.email_trust(profile.email)
        }
        return self.fake_classifier.predict(signals)
    
    def detect_coordinated_attack(self, events: list) -> bool:
        """Koordineli saldırı tespiti (bot network vb.)"""
        # Kısa sürede benzer IP'den çok sayıda kayıt
        # Benzer profil içerikleri
        # Aynı hedefe yönelik koordineli spam
        return self.attack_detector.analyze(events)
```

### Mentor Module — Aylık Değerlendirme Formatı

```
📊 AYLK ETKİ ÖZETİN — Nisan 2026

Toplam MHS: 742 (geçen ay: 718) ↑ +24 puan

Bu ayki kazanımların:
✅ +18 pts — Deprem yardım gönüllülüğü (12 saat)
✅ +12 pts — GitHub açık kaynak commit (47 katkı)
✅ +6 pts — Blog: İklim değişikliği farkındalık
❌ -12 pts — Uzun mesafe uçuş (2x)

🎯 Sana Özel Hedefler (Mayıs):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Çevresel skor geride — bu ay 1 ağaç dik?
   → Yakın bölgedeki etkinlik: "Yeşil İstanbul" (10 Mayıs)
   
2. Beyin yakın profilinden ilham:
   → Ayşe (MHS: 761) bu ay yerel gıda bankasına katıldı
   → Topluluk mutfağı gönüllüsü aranıyor (2 saat/hafta)
   
3. Bu hafta kolayca yapabileceğin:
   → Elektronik atık toplama noktası: 500m yakında
   → +8–15 puan bekleniyor

💬 Angel'dan not:
"Geçen 3 ay boyunca tutarlı katkı sağladın — 
bu seni Türkiye'deki kullanıcıların %89'unun 
önüne geçirdi. Harika gidiyorsun."
```

### Angel AI — Güvenlik Bildirimi Örnekleri

```
🛡️ Angel Koruması Devrede

Bir kullanıcı profilini raporladı: [Kullanıcı adı]
Gerekçe: Sahte aktivite beyanı şüphesi
Durum: İnceleniyor (48 saat içinde yanıt)
Sen etkilendin mi? [Hayır / Evet, detay ver]

---

⚠️ Olağandışı aktivite tespit edildi

Hesabınıza 3 farklı konumdan giriş yapıldı.
Son giriş: Berlin, Almanya — 14:32 UTC
Altta mı? [Bu benim  /  Hayır, hesabımı kilitle]
```

---

## 2. ROZET EKOSİSTEMİ — TAM ŞEMA

### Katman 1: Skor Seviyeleri (Otomatik)
*(Yukarıda belirtildi — 7 seviye, 🌱 → 👑)*

### Katman 2: Aktivite Rozetleri (Kazanılan)

| Rozet | İkon | Kriter | Doğrulama |
|-------|------|--------|-----------|
| İlk Adım | 🐣 | İlk aktivite kaydı | Otomatik |
| Gönüllü | 🤲 | 10+ saat gönüllülük | Kuruluş onayı |
| 100 Saat | ⌛ | 100 saat toplam gönüllülük | Otomatik (kuruluş onaylı saatler) |
| Akademisyen | 📖 | İlk peer-review yayın | DOI doğrulama |
| Mucit | 💡 | Patent tescili | Patent ofisi belgesi |
| Kan Bağışcısı | 🩸 | Kan bağışı | Hastane belgesi |
| Hayat Kurtaran | ❤️‍🔥 | Organ bağışı / CPR eğitimi | Sağlık kurumu onayı |
| Ağaç Dikici | 🌳 | 10+ ağaç dikilmesi | Koordinatlar + fotoğraf |
| Okyanusa Sahip Çık | 🌊 | Deniz/kıyı temizliği | Grup onayı |
| Gıda Savaşçısı | 🍽️ | Gıda israfı önleme aktivitesi | Kuruluş veya uygulama |
| Açık Kaynak | 💻 | 50+ GitHub commit | GitHub API |
| Eğitimci | 🎓 | 10+ kişiye öğretmenlik | Peer + kuruluş |
| Sanatçı | 🎨 | Sanat eseri toplumsal katkı | Portfolyo + etki |
| Barış Elçisi | ☮️ | Arabuluculuk / çatışma çözümü | Belge |
| Kriz Kahramanı | 🆘 | Aktif kriz bölgesi görevi | Kuruluş onayı |
| Zaman Kapsülü | ⏳ | 5 yıl tutarlı aktivite | Otomatik (zaman bazlı) |
| Mentör | 🧭 | 5+ kişiyi aktif mentörlük | Mentörler + peer |

### Katman 3: Özel Unvanlar (Profil'de Görünen Rozet Rozet)

Bu unvanlar kullanıcının profilinde büyük rozet olarak gösterilir. Diğer kullanıcılar görebilir.

```
╔══════════════════════════════════════════╗
║  👼 Angel  |  🦋 Activist  |  🤍 Volunteer  ║
║  💎 VIP Contributor  |  🩺 Planet Doctor   ║
║  ☮️ Peacemaker  |  🏅 Nobel Laureate       ║
║  🆘 Crisis Hero  |  🔬 Researcher          ║
║  🌱 Climate Guardian  |  💻 Open Source Hero║
╚══════════════════════════════════════════╝
```

**Unvan Kazanma Kriterleri:**

**👼 Angel (Melek)**
- Kazanma: İnsanlık tarihinde kayda değer, olağandışı insani fedakarlık
- Örnek: Savaş bölgesinde yıllarca gönüllü çalışan sağlık personeli
- Doğrulama: Etik Kurul kararı (oy çokluğu)
- Sayı limiti: Her yıl küresel olarak max 100 Angel rozetii

**🦋 Activist**
- Kazanma: 2+ yıl aktif, belgelenmiş aktivizm
- En az 2 referans kuruluş onayı
- Kamusal etki kanıtı

**🤍 Volunteer**
- Kazanma: 500+ saat doğrulanmış gönüllülük
- En az 2 farklı kuruluşta
- Aktif olmaya devam ediyor

**💎 VIP Contributor**
- Kazanma: MHS > 850 + küresel ölçekte etki
- Topluluk oyu (min 500 oy) + Kurul onayı
- Her yıl yenilenmesi gerekir (aktif kalınmalı)

**🩺 Planet Doctor**
- Kazanma: İklim/ekoloji alanında doktora veya eşdeğer uzmanlık
- Peer-reviewed iklim yayınları
- Aktif araştırma veya uygulama

**🏅 Nobel Laureate**
- Kazanma: Nobel Ödülü (herhangi bir alanda)
- Doğrulama: Nobel.org üzerinden otomatik
- Otomatik rozet — kullanıcı talebi gerektirmez

**🆘 Crisis Hero**
- Kazanma: Aktif kriz bölgesinde (savaş/afet) en az 30 gün görev
- MSF, UNHCR, Kızılay gibi onaylı kuruluş onayı
- Her görev yeni rozet kazandırır (birikimli)

### Katman 4: Grup & Kolektif Rozetler

| Rozet | Kriter |
|-------|--------|
| 🏘️ Impact Community | Grup kolektif MHS > 5000 |
| 🌍 Global Brigade | 10+ ülkeden üyesi olan grup |
| 🔥 Active Team | Grup aylık en az 50 aktivite |
| 🌿 Green Squad | Grubun çevre skoru en yüksek %10 |
| 📣 Viral Impact | Grubun faaliyeti 1000+ kişiye ulaştı |

---

## 3. UX TASARIM SİSTEMİ v2

### Tasarım Dili Güncellemesi
Yeni eklemelerle tasarım daha "topluluk odaklı" ve "şeffaf" hissettirmeli.

**Renk Paleti (Korundu + Genişletildi):**
```css
:root {
  --primary: #1A3A4A;       /* Derin deniz — güven */
  --accent: #2DC67D;        /* Canlı yeşil — büyüme */
  --angel-gold: #F0B429;    /* Altın — Angel AI, özel rozetler */
  --crisis-red: #E84855;    /* Kırmızı — kriz uyarı */
  --peace-blue: #4A90E2;    /* Barış mavisi — sivil aktivite */
  --earth-brown: #8B6B47;   /* Toprak — çevre */
  --community-purple: #9B59B6; /* Topluluk mor */
  --open-teal: #00B5AD;     /* Açık kaynak/şeffaflık */
}
```

### Ana Ekran Güncellemeleri

#### Profil Sayfası v2
```
┌─────────────────────────────────────────┐
│  [Avatar]  Zeynep Şahin                 │
│  🌍 İstanbul, Türkiye  |  🔬 Researcher  │
│                                         │
│  ┌──────────────────────────────────┐   │
│  │     MHS: 742  ████████████░░    │   │
│  │     CHAMPION 🏆  |  Top 8% 🌍   │   │
│  └──────────────────────────────────┘   │
│                                         │
│  ÖZEL UNVANLAR:                         │
│  [🦋 Activist] [🤍 Volunteer] [🩺 Planet Doctor] │
│                                         │
│  AKTİVİTE ROZETLERİ:                    │
│  🩸 💡 💻 📖 🌊 🌳 ☮️ +5 daha          │
│                                         │
│  ─────────────────────────────────────  │
│  GRUPLARIN:                             │
│  🌿 İklim Gönüllüleri (Üye: 847)       │
│  📚 Açık Kaynak TR (Üye: 2.341)        │
│                                         │
│  [Profili Paylaş] [Angel AI ile Konuş] │
└─────────────────────────────────────────┘
```

#### Beyan Ekleme Akışı v2
```
ADIM 1/5: Aktivite Türü
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[🆘 Kriz/Saha Görevi]  [🤲 Gönüllülük]
[💡 İnovasyon/Patent]  [📖 Akademik]
[💚 Bağış/Burs]        [🌿 Çevre]
[🎨 Sanat/Kültür]      [☮️ Barış/Haklar]
[🍽️ Gıda Kurtarma]    [💻 Açık Kaynak]
[🏅 Resmi Ödül]        [+ Diğer]

ADIM 2/5: Detaylar
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Başlık: _________________________________
Kuruluş (varsa): _________________________
Tarih: ________ → ________  ☐ Devam ediyor
Etki: Tahminen kaç kişiyi etkiledi? ______
Yer: __________________________________

ADIM 3/5: Kanıt
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[📎 Belge Yükle]  [🔗 Link Ekle]
[📸 Fotoğraf]     [👥 Referans Kişi]
[🏛️ Kuruluş Kodu] [📋 Kuruluş Formu]

Opsiyonel: "Bu aktiviteden ne öğrendin?" (açık metin)

ADIM 4/5: Angel AI Ön Değerlendirme
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏳ Angel inceliyor...

✅ "Kanıtın geçerli görünüyor"
📊 Tahmini etki: +22 ile +38 puan arası
⏰ Tam doğrulama: 3–7 gün

[Kaydet ve Bekle] [Düzenle]

ADIM 5/5: Topluluk Doğrulama
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Beyanın 3 topluluk üyesi tarafından doğrulanmayı bekliyor.
[İlerlemeyi Takip Et]
```

#### Angel AI Chat Arayüzü
```
┌─────────────────────────────────────────┐
│  👼 Angel                         ☰     │
│  ─────────────────────────────────────  │
│                                         │
│  ╭──────────────────────────────────╮   │
│  │ Merhaba Zeynep! Bu ay harika    │   │
│  │ gidiyorsun. Mayıs ayı için 3   │   │
│  │ önerin var — görmek ister misin?│   │
│  ╰──────────────────────────────────╯   │
│                                         │
│  ╭──────────────────────────────────╮   │
│  │                     Tabii ki 🌱 │   │
│  ╰──────────────────────────────────╯   │
│                                         │
│  ╭──────────────────────────────────╮   │
│  │ 1. Çevre — yakınında ağaç dikme │   │
│  │    etkinliği var (10 Mayıs)     │   │
│  │ 2. Sağlık — kan bağışı merkezi  │   │
│  │    bu hafta randevu alıyor      │   │
│  │ 3. Topluluk — İklim Gönüllüleri │   │
│  │    grubuna katılmak ister misin?│   │
│  ╰──────────────────────────────────╯   │
│                                         │
│  [Mesaj yaz...]            [Gönder 📤]  │
└─────────────────────────────────────────┘
```

---

## 4. GRUP SİSTEMİ — DETAYLI SPESİFİKASYON

### Grup Oluşturma Akışı

```python
@dataclass
class Group:
    id: UUID
    name: str
    description: str
    type: str  # 'open', 'closed', 'thematic', 'local', 'org'
    theme: Optional[str]  # 'climate', 'education', 'health' vb.
    location: Optional[str]  # şehir/ülke
    privacy: str  # 'public', 'members_only', 'invite_only'
    
    # Skor paylaşımı
    score_sharing: str  # 'opt_in', 'opt_out', 'disabled'
    show_leaderboard: bool
    
    # Üyelik
    members: list[UUID]
    admins: list[UUID]
    max_members: Optional[int]
    
    # İçerik
    challenges: list[Challenge]
    feed: list[Post]
    collective_mhs: float  # üyelerin ortalaması
    
    created_at: datetime
    badges: list[str]
```

### Grup Feed & Özellikler

```
🌿 İklim Gönüllüleri Grubu
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
👥 847 üye  |  Kolektif MHS: 8,470 avg  |  🌍 Global

Bu Ay Aktif:
🏅 312 üye aktivite ekledi
🌳 1,240 ağaç dikilmesi beyan edildi
♻️ 47 üye sıfır atık rozetine ulaştı

Grup Meydan Okuması:
🎯 "Mayıs Yeşil Ayı" — 1000 ağaç hedefi
████████░░ %81 tamamlandı (813/1000)

Son Aktiviteler:
🌱 Ahmet K. Antalya orman yangını sonrası 50 fidan dikti
🔬 Sara L. iklim raporunu toplulukla paylaştı
♻️ Mohamed A. Kahire'de e-atık kampanyası başlattı

[Aktivite Paylaş] [Meydan Okuma] [Mesaj]
```

---

## 5. OPEN SOURCE YÖNETİŞİMİ

### GitHub Repository Yapısı
```
kindora/ (veya seçilen isim)
├── 📂 apps/
│   ├── web/          # Next.js
│   ├── mobile/       # React Native
│   └── admin/        # Yönetim paneli
├── 📂 packages/
│   ├── core/         # Skor hesaplama motoru
│   ├── angel-ai/     # Angel AI modülleri
│   ├── api/          # FastAPI backend
│   └── db/           # Şema + migrasyonlar
├── 📂 docs/
│   ├── ALGORITHM.md  # Skor algoritması açıklaması
│   ├── ETHICS.md     # Etik charter
│   ├── CONTRIBUTING.md
│   └── RFC/          # Topluluk önerileri
├── 📂 research/
│   └── anonymized-data/  # Araştırma veri setleri
├── LICENSE           # AGPL-3.0 (en güçlü copyleft)
└── MANIFESTO.md      # Platform manifestosu
```

### Lisans Seçimi: AGPL-3.0
AGPL-3.0 seçiminin nedeni:
- Birisi kodu alıp ticari kullanırsa değişikliklerini de açık kaynak yapması zorunlu
- "Forkla + kapat" saldırısına karşı koruma
- Topluluk ilkeleriyle uyumlu

---

## 6. GİZLİLİK & AYRIM YASAĞI — KOD DÜZEYİNDE

### Ayrım Yasağı — Teknik Uygulama

```python
# Algoritma içinde ayrım yaratan her özelliği engelle

FORBIDDEN_FEATURES = [
    'religion', 'ethnicity', 'race', 'gender', 'sexual_orientation',
    'nationality', 'language', 'disability', 'political_affiliation',
    'economic_status', 'education_level'  # eğitim ağırlık için değil, ayrım için
]

class ScoreEngine:
    def validate_features(self, features: dict) -> None:
        for forbidden in FORBIDDEN_FEATURES:
            if forbidden in features:
                raise EthicsViolationError(
                    f"Feature '{forbidden}' is not allowed in scoring. "
                    f"This violates the MHS Non-Discrimination Charter."
                )
    
    def calculate(self, user_id: str, activities: list) -> float:
        features = self.extract_features(activities)
        self.validate_features(features)  # Her hesaplamada kontrol
        return self._compute(features)
```

### Bias Audit (Yıllık)
```python
class BiasAuditor:
    """Yılda 2 kez çalışır — bağımsız kurul tarafından incelenir"""
    
    def audit(self, score_data: DataFrame) -> BiasReport:
        report = BiasReport()
        
        # Cinsiyet bazlı eşitsizlik kontrolü
        gender_fairness = self.check_group_parity(
            score_data, group_col='gender', score_col='mhs_score'
        )
        
        # Ülke bazlı eşitsizlik (coğrafi düzeltme haricinde)
        country_fairness = self.check_disparate_impact(
            score_data, group_col='country', score_col='raw_mhs'
        )
        
        # Yaş grupları
        age_fairness = self.check_group_parity(
            score_data, group_col='age_group', score_col='mhs_score'
        )
        
        report.add_all([gender_fairness, country_fairness, age_fairness])
        report.publish_to_github()  # Kamuya açık yayın
        
        return report
```

---

*Bu belge serisi MHS Project v2.0 Knowledge Base'ini oluşturur.*
*Tüm dosyalar Claude Projects'e yüklenmeli: Custom Instructions + KB01 + KB02 + KB03*
