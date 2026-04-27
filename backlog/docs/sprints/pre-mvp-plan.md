# Pre-MVP Plan — MHS Demo by May 31, 2026

## Hedef / Goal

**31 Mayıs 2026'ya kadar** çalışan, uçtan uca bir demo ortamı:
- 5 demo kullanıcısı oluşturulmuş ve veritabanında seed edilmiş
- Her kullanıcının MHS skoru 6 kategoride hesaplanmış
- Web arayüzünde kullanıcı seçilip skor gösterilebilir
- `docker compose up` ile tüm sistem ayağa kalkar

---

## Zaman Analizi

| Faktör | Değer |
|--------|-------|
| Başlangıç | 27 Nisan 2026 |
| Son tarih | 31 Mayıs 2026 |
| Toplam takvim günü | **34 gün** |
| Claude Code quota kaybı tahmini | %30 (~10 gün) |
| Efektif çalışma günü | **~24 gün** |
| Toplam iş yükü (saat) | ~23 saat |
| Günlük hedef | 1 task / gün |
| Buffer (quota + bug fix) | **10 gün** |

### Claude Code Quota Kısıtlamaları
- Günlük API limiti dolduğunda session sıfırlanana kadar beklenir (~8-24 saat)
- Yoğun context window tüketen tasklar (Sonnet, 30K+ token) günde 1 task = 1 oturum
- Haiku taskları daha hızlı tüketir, günde 2 yapılabilir
- En riskli dönem: M2 Score Engine (en karmaşık algoritmik iş)

---

## Pre-MVP Kapsam (Ne var, ne YOK)

### ✅ Pre-MVP'de VAR
- Docker Compose: Next.js + FastAPI + PostgreSQL
- Seed edilmiş 5 demo kullanıcısı (gerçek kayıt YOK)
- 6 kategorili basitleştirilmiş MHS skor hesabı
- REST API: `GET /api/v1/scores/{user_id}`
- Profil sayfası: skor + kategori breakdown
- Demo mode user switcher (JWT auth YOK)

### ❌ Pre-MVP'de YOK (sonraki sprintlerde)
- JWT authentication / OAuth
- Gerçek aktivite gönderme UI'ı
- Celery / Redis arka plan işleri
- Neo4j graph katmanı (network multiplier)
- Badge sistemi
- Feed / social timeline
- Angel AI (post-MVP, task 900+)
- GitHub Actions CI (opsiyonel)

---

## Milestone Planı

```
Nisan         Mayıs
27  28  29  30  1   2   3   4   5   6   7   8   9   10  11  12  13  14
│                               │               │           │
START                          M1 deadline    M2+M3 deadline
                               (3 Mayıs)      (11 Mayıs)

15  16  17  18  19  20  21  22  23  24  25  26  27  28  29  30  31
                    │                                           │
                  M4 deadline                               M5 DEMO
                  (21 Mayıs)                               (31 Mayıs)
```

---

## M1: Dev Environment (Deadline: 3 Mayıs)

**Hedef:** `docker compose up` → Next.js + FastAPI + PostgreSQL ayakta

| Task | Başlık | Model | Süre | Sıra |
|------|--------|-------|------|------|
| TASK-1 | Repo Setup + Docker + CI | Sonnet | ~3h | 1. çalıştır |
| TASK-2 | PostgreSQL Schema + Alembic | Sonnet | ~2h | TASK-1 sonrası paralel |
| TASK-3 | FastAPI Project Scaffold | Sonnet | ~2h | TASK-1 sonrası paralel |

**Execution sırası:**
```
Gün 1: TASK-1 (Docker + monorepo)
Gün 2: TASK-2 ‖ TASK-3 (iki ayrı terminal/oturum — paralel)
```

**Quota riski:** ORTA — Docker kurulumu genellikle sorunsuz ama ARM64 uyumluluk sorunları çıkabilir.

**Başarı kriteri:**
- `curl http://localhost:8000/health` → `{"status": "ok"}`
- `curl http://localhost:3000` → Next.js anasayfa
- `alembic upgrade head` → tablo oluşturma başarılı

---

## M2: Score Engine (Deadline: 11 Mayıs)

**Hedef:** API'den gerçek skor hesabı döner

| Task | Başlık | Model | Süre | Bağımlılık |
|------|--------|-------|------|-----------|
| TASK-7 | MHS Score Calculator | Sonnet | ~3h | TASK-2 |
| TASK-8 | Scoring Categories API | Sonnet | ~2h | TASK-7 |

**Execution sırası:**
```
Gün 3-4: TASK-7 (score algorithm — en kritik task)
Gün 5: TASK-8 (API endpoint wrapper)
```

**Quota riski:** YÜKSEK — Score calculator karmaşık matematiksel mantık içeriyor.
TASK-7 büyük ihtimalle günlük quota'nın büyük kısmını tüketir.

**Pre-MVP için basitleştirmeler:**
- Carbon penalty: sabit bir lookup tablosu (Climatiq API bağlantısı OLMADAN)
- Network multiplier: 1.0 sabit (Neo4j olmadan)
- Toxicity penalty: 0 (toxic-BERT olmadan)
- Consistency + geographic multiplier: basit kural tabanlı

**Başarı kriteri:**
- `GET /api/v1/scores/1` → Elif Kaya için JSON skor döner
- Skor 0-1000 aralığında, 6 kategori breakdown içeriyor

---

## M3: Frontend Shell (Deadline: 11 Mayıs)

**Hedef:** `localhost:3000` → şık, gerçek uygulama görünümü

| Task | Başlık | Model | Süre | Bağımlılık |
|------|--------|-------|------|-----------|
| TASK-5 | Next.js App Shell + Routing | Sonnet | ~3h | TASK-1 |

**Not:** M2 ile paralel çalıştırılabilir (farklı oturum/terminal).

**Quota riski:** DÜŞÜK — Next.js scaffold Sonnet için rutin iş.

**Başarı kriteri:**
- TailwindCSS + shadcn/ui çalışıyor
- `/` ve `/profile` rotaları var
- MHS tasarım token'ları (`MHS_COLORS`) tanımlı

---

## M4: Demo Integration (Deadline: 21 Mayıs)

**Hedef:** Kullanıcı seçilince gerçek skor görünür

| Task | Başlık | Model | Süre | Bağımlılık |
|------|--------|-------|------|-----------|
| TASK-45 | Seed Data Script | Haiku | ~1h | TASK-2, TASK-7 |
| TASK-46 | Demo Mode User Switcher | Haiku | ~1h | TASK-5 |
| TASK-6 | User Profile Page | Sonnet | ~4h | TASK-46, TASK-8 |

**Execution sırası:**
```
Gün 9: TASK-45 (seed script — hızlı, Haiku)
Gün 10: TASK-46 (demo switcher — hızlı, Haiku)
Gün 11-12: TASK-6 (profil sayfası — en büyük frontend taski)
```

**Quota riski:** ORTA-YÜKSEK — TASK-6 karmaşık UI bileşeni, genellikle 2 oturum gerektirir.

**Başarı kriteri:**
- `python scripts/seed_demo.py` → 5 kullanıcı + aktivite + skor DB'de
- Header dropdown → demo kullanıcı seç
- `/profile?userId=1` → Elif Kaya'nın profili ve skoru görünür

---

## M5: Pre-MVP Demo (Deadline: 31 Mayıs)

**Hedef:** Temiz, demo edilebilir, çöken yeri olmayan sistem

| Task | Başlık | Model | Süre | Bağımlılık |
|------|--------|-------|------|-----------|
| TASK-47 | Score Display Integration | Sonnet | ~2h | TASK-6, TASK-8 |
| TASK-34 | Unit + Integration Tests (mini) | Haiku | ~2h | M4 tamamı |

**Buffer:** 22-31 Mayıs arası 10 günlük buffer.
- Quota kaynaklı gecikmeler
- Integration hataları
- UI polish
- Demo script yazımı

**Quota riski:** DÜŞÜK — Integration + testler basit, hata düzeltme öngörülmüş.

**Başarı kriteri (demo gününde):**
- [ ] `git clone && docker compose up` → sistem 3 dakikada ayakta
- [ ] `python scripts/seed_demo.py` → 5 kullanıcı seed edildi
- [ ] Tarayıcıdan 5 farklı kullanıcı arasında geçiş yapılabiliyor
- [ ] Her kullanıcının farklı skoru ve kategori dağılımı görünüyor
- [ ] Hiçbir hata konsola yazılmıyor
- [ ] Mobil görünüm kabul edilebilir durumda

---

## Gantt — Efektif Günler

```
TASK                          Hf1    Hf2    Hf3    Hf4    Hf5
                             Apr28  May5  May12  May19  May26
                              ─────  ─────  ─────  ─────  ─────
TASK-1 Docker+CI             ██
TASK-2 DB Schema               ██
TASK-3 FastAPI                 ██
                             ─────M1─────
TASK-7 Score Calc                   ███
TASK-8 Scoring API                    ██
TASK-5 Next.js Shell                ██
                                   ─M2+M3─
TASK-45 Seed Script                       █
TASK-46 Demo Switcher                     █
TASK-6 Profile Page                       ████
                                         ─M4──
TASK-47 Integration                            ██
TASK-34 Tests (mini)                           ██
BUFFER (quota/bugs)                            ██████████
                                              ─────M5────
```

---

## Quota Gecikmesi Senaryoları

| Senaryo | Etki | Tepki |
|---------|------|-------|
| Günlük limit doldu | 8-24 saat kayıp | Buffer haftasına yığ |
| TASK-7 2 oturum alıyor | +1 gün | M2 deadline → 12 Mayıs'a kayar |
| TASK-6 2 oturum alıyor | +1 gün | M4 deadline → 22 Mayıs'a kayar |
| 3+ task quota'da patlıyor | +3 gün | Buffer tükenir, TASK-34 mini'ye indir |
| Her şey patlıyor | +7 gün | Sadece TASK-47'yi kes, test yok |

**Minimum demo (en kötü senaryo):** M1 + M2 + M3 + TASK-45 + TASK-47 = 5 task,
skor API'den geliyor ama UI minimal olabilir.

---

## Execution Komutları

### M1 — Gün 1
```bash
claude "CLAUDE.md ve backlog/tasks/task-1 - Repo Setup + Docker + CI.md dosyalarını oku.
Monorepo yapısını, Docker Compose geliştirme ortamını (Next.js, FastAPI, PostgreSQL servisleri)
kur. Redis ve Neo4j'yi şimdilik docker-compose.yml'de opsiyonel bırak.
Pre-MVP notu: sadece 3 servis zorunlu — web, api, db.
Kabul kriterlerini yerine getir."
```

### M1 — Gün 2 (iki terminal, paralel)
```bash
# Terminal 1
claude "CLAUDE.md ve backlog/tasks/task-2 - PostgreSQL Schema + Alembic Migrations.md oku.
users ve mhs_scores tablolarını öncelikle yap, activities tablosunu basitleştir.
Pre-MVP: Neo4j, Redis tabloları henüz gerekli değil."

# Terminal 2
claude "CLAUDE.md ve backlog/tasks/task-3 - FastAPI Project Scaffold.md oku.
FastAPI projesini kur. GET /health endpoint'i çalışır hale getir.
Pre-MVP: Auth middleware şimdilik boş bırakılabilir."
```

### M2 — Gün 3–4
```bash
claude "CLAUDE.md, concept/MHS_KB_02_Technical.md ve backlog/tasks/task-7 - MHS Score Calculator.md oku.
Python MHS skor hesaplayıcısını uygula. Pre-MVP basitleştirmeleri:
- Carbon penalty: sabit lookup tablosu (API yok)
- Network multiplier: 1.0 sabit
- Toxicity penalty: 0 sabit
6 kategori ağırlıklarını tam uygula (KB_02'deki formüle göre)."
```

### M3 — Gün 3 veya 4 (M2 ile paralel, ayrı terminal)
```bash
claude "CLAUDE.md ve backlog/tasks/task-5 - Next.js App Shell + Routing.md oku.
Next.js 15 app shell'i kur: TailwindCSS, shadcn/ui, MHS tasarım token'ları,
/profile rotası. Pre-MVP: Auth context şimdilik DemoModeProvider olacak (TASK-46 yapacak)."
```

---

## Demo Script (31 Mayıs)

```bash
# 1. Klon ve başlat
git clone https://github.com/fxerkan/my-humanity-score
cd my-humanity-score
docker compose up -d

# 2. Seed
docker compose exec api python scripts/seed_demo.py

# 3. Demo
open http://localhost:3000
# Header'dan kullanıcı seç → skor görünür
```
