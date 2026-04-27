# Backlog.md — MHS Proje Görev Yönetimi Rehberi

> **English version:** [README.md](README.md)

Bu rehber, My Humanity Score (MHS / Kindora) projesinde **Backlog.md**'nin Developer, Analyst, Tester, Data Crawler, Data Visualizer ve Reviewer gibi farklı roller tarafından nasıl kullanılacağını açıklar.

---

## İçindekiler

1. [Dizin Yapısı](#dizin-yapısı)
2. [Temel Kavramlar](#temel-kavramlar)
3. [Role Göre Günlük CLI Referansı](#role-göre-günlük-cli-referansı)
4. [Epic Oluşturma](#epic-oluşturma)
5. [Task Oluşturma](#task-oluşturma)
6. [Draft Task Oluşturma](#draft-task-oluşturma)
7. [Task Yaşam Döngüsü](#task-yaşam-döngüsü)
8. [Döküman ve Karar Yönetimi](#döküman-ve-karar-yönetimi)
9. [Kanban Board ve Tarayıcı Arayüzü](#kanban-board-ve-tarayıcı-arayüzü)
10. [Bağımlılık Yönetimi](#bağımlılık-yönetimi)
11. [Task Şablonları](#task-şablonları)
12. [MHS Etiket Kuralları](#mhs-etiket-kuralları)
13. [AI Ajan Entegrasyonu](#ai-ajan-entegrasyonu)

---

## Dizin Yapısı

```
backlog/
├── README.md                  ← İngilizce versiyon
├── README.tr.md               ← Bu dosya (Türkçe)
├── config.yml                 ← Backlog.md proje yapılandırması
│
├── tasks/                     ← Tüm aktif tasklar (düz, Markdown dosyaları)
│   ├── task-1 - Başlık.md
│   ├── task-2 - Başlık.md
│   └── task-900 - Başlık.md   ← Post-MVP tasklar (900+ aralığı)
│
├── drafts/                    ← Henüz geliştirmeye hazır olmayan fikirler
│
├── docs/                      ← Referans dökümanlar
│   ├── epics/                 ← Epic planlama dökümanları
│   │   ├── epic-001-foundation.md
│   │   ├── epic-002-auth-profiles.md
│   │   └── ...
│   └── sprints/               ← Sprint planlama dökümanları
│       └── sprint-01-foundation.md
│
├── decisions/                 ← Mimari Karar Kayıtları (ADR)
│
├── milestones/                ← Milestone takibi
│
├── completed/                 ← Arşivlenmiş tamamlanmış tasklar
└── archive/                   ← Arşivlenmiş iptal/ertelenmiş tasklar
```

### Task Numaralandırma Kuralı

| Aralık | Amaç |
|--------|------|
| 1–99 | MVP Sprint 1 — Temel Altyapı |
| 100–199 | MVP Sprint 2 — Temel Özellikler |
| 200–299 | MVP Sprint 3 — Gelişmiş Özellikler |
| 300–399 | MVP Sprint 4 — Son Rötuşlar ve Lansman |
| 400–499 | Veri rolleri (Analyst, Crawler, Visualizer) |
| 900+ | **Post-MVP** — Angel AI, ileri yönetişim |

---

## Temel Kavramlar

| Kavram | Ne İşe Yarar | Nerede Saklanır |
|--------|-------------|----------------|
| **Task** | Tek bir iş birimi (1 oturum / 1 PR) | `backlog/tasks/task-N - Başlık.md` |
| **Draft** | Geliştirmeye hazır olmayan fikir | `backlog/drafts/` |
| **Epic** | Ortak bir hedefi olan ilgili tasklar grubu | `backlog/docs/epics/epic-NNN-*.md` |
| **Sprint** | Zaman sınırlı task seti | `backlog/docs/sprints/sprint-NN-*.md` |
| **Decision** | Mimari Karar Kaydı (ADR) | `backlog/decisions/` |
| **Milestone** | Bir sürüm için gruplandırılmış tasklar | `backlog milestone` komutu ile |

**Altın kural:** 1 task = 1 ajan oturumu = 1 PR. Bir task birden fazla oturumda tamamlanıyorsa alt tasklara bölünmeli.

---

## Role Göre Günlük CLI Referansı

### Herkes — Güne Başlarken

```bash
# Her şeye bir bakışta göz at
backlog board

# Web arayüzünü aç (port 6420)
backlog browser

# Üzerinde çalışılanları gör
backlog task list --status "In Progress" --plain

# Başlanabilecek sıradaki taskları gör (bloker yok)
backlog sequence list --plain

# Bir şey ara
backlog search "scoring"
```

---

### Developer

```bash
# Sıradaki taske bak
backlog task list --status "To Do" --priority high --plain

# Taski tam olarak görüntüle
backlog task view 7

# Çalışmaya başla — In Progress'e al
backlog task edit 7 --status "In Progress" --assignee "@me"

# Kodlarken uygulama notları ekle
backlog task edit 7 --append-notes "SQLAlchemy 2 async session kullanıldı"

# Kabul kriteri işaretle
backlog task edit 7 --check-ac 1

# Tamamlandı olarak işaretle
backlog task edit 7 --status "Done"

# Ana task altında alt task oluştur
backlog task create "activities.user_id için index ekle" \
  --parent 2 \
  --priority high \
  --labels "epic001-foundation,database"

# Bağımlılık ekle
backlog task edit 8 --dep 7

# Tamamlanan taski arşivle
backlog task archive 7
```

---

### Analyst / Data Analyst

```bash
# Veri kalitesi ile ilgili taskleri listele
backlog task list --plain | grep -i "quality\|label\|mdm"

# Veri ile ilgili taskleri ara
backlog search "data quality" --type task

# Kalite kontrol taski oluştur
backlog task create "Haftalık veri kalitesi raporu çalıştır" \
  --priority medium \
  --labels "epic011-ml-ai,data-analyst" \
  --ac "Kalite raporu reports/quality/YYYY-MM-DD.md'ye yazılsın" \
  --ac "Sıfır toleranslı ihlal bulunmasın"

# Mimari karar kaydet
backlog decision create "10M satırda activities tablosu için partition kullan"

# Bağımlılık yürütme sırasını gör
backlog sequence list --plain

# Bloklananları kontrol et
backlog task list --plain | grep -i "blocked"
```

---

### Tester / QA

```bash
# Test edilmeye hazır taskleri bul
backlog task list --status "In Progress" --plain

# Bir özelliğe bağlı test taski oluştur
backlog task create "JWT auth sınır durumlarını test et" \
  --priority high \
  --labels "epic002-auth,tester" \
  --dep 4 \
  --ac "Yanlış şifreyle giriş 401 döner (403 değil)" \
  --ac "Süresi dolmuş token, yenileme ipucuyla 401 döner" \
  --ac "55 dakika sonra refresh token çalışır"

# Kabul kriterlerini doğrulandı olarak işaretle
backlog task edit 34 --check-ac 1 --check-ac 2

# Hata notu ekle
backlog task edit 34 --append-notes "HATA: token tam süresi dolduğunda refresh endpoint 500 döner"

# Hata raporu için draft oluştur
backlog draft create "Hata: Aktivitesi olmayan kullanıcılar skor hesabında atlıyor"

# Drafti gerçek taska terfi et
backlog draft promote 3
```

---

### Data Crawler

```bash
# Tüm crawler tasklarını gör
backlog task list --plain | grep -i "crawl\|integrat\|sync"

# Yeni crawler taski oluştur
backlog task create "Idealist.org gönüllülük tarayıcısı ekle" \
  --priority medium \
  --labels "epic009-integrations,data-crawler" \
  --ac "BaseCrawler alt sınıfı apps/api/crawlers/idealist.py'de oluşturuldu" \
  --ac "Hız sınırı: 2 istek/sn uygulandı" \
  --ac "robots.txt kontrol edildi ve uyuldu" \
  --ac "Mock httpx yanıtlarıyla birim testleri geçiyor"

# Bir crawler için referans döküman oluştur
backlog doc create "Idealist API Hız Limitleri" --path docs/integrations/idealist.md
```

---

### Data Visualizer

```bash
# Tüm görselleştirme tasklarını gör
backlog task list --plain | grep -i "chart\|dashboard\|visual\|widget"

# Grafik taski oluştur
backlog task create "Genel istatistikler için kategori dağılımı donut grafiği" \
  --priority medium \
  --labels "epic012-frontend,data-visualizer" \
  --ac "recharts + MHS_COLORS tasarım token'ları kullanılıyor" \
  --ac "5'ten az kullanıcılı gruplar gizleniyor (anonimleştirme)" \
  --ac "Erişilebilir: role=img, aria-label, figcaption"

# Paydaş güncellemesi için board dışa aktar
backlog board export sprint1-durum.md
```

---

### Reviewer / Tech Lead

```bash
# Tam board görünümü
backlog board --milestones

# Bir task için bağımlılık zincirini kontrol et
backlog sequence list --plain

# Tüm yüksek öncelikli öğeleri gör
backlog task list --priority high --plain

# 30 günden eski tamamlanan taskleri arşivle
backlog cleanup

# Board anlık görüntüsünü dışa aktar
backlog board export --filename "$(date +%Y-%m-%d)-board-snapshot.md"

# Mimari karar kaydet
backlog decision create "Skor hesaplama için FastAPI BackgroundTasks yerine Celery kullan"
```

---

## Epic Oluşturma

Epicler planlama dökümanlarıdır — `backlog/docs/epics/` altında yaşar ve doğrudan `backlog` CLI ile yönetilmez. Şu şablonu kullanarak Markdown dosyaları olarak oluşturun:

```bash
# Yeni bir epic dökümanı oluştur
backlog doc create "EPIC-013 — Bildirim Sistemi" --path docs/epics/epic-013-bildirimler.md
```

### Epic Şablonu

```markdown
# EPIC-NNN — [Epic Başlığı]

## Durum: `ready` | `in-progress` | `done` | `deferred`

## Öncelik: P0 (Sprint 1) | P1 (Sprint 2) | P2 (Sprint 3) | P3 (Post-MVP)

## Hedef
[Bu epicin ne sağladığını ve MHS kullanıcılarına neden önemli olduğunu açıklayan 1–2 paragraf.]

## Kapsam
- [Özellik veya çıktı 1]
- [Özellik veya çıktı 2]
- [Özellik veya çıktı 3]

## Kapsam Dışı
- [Kapsam genişlemesini önlemek için açıkça hariç tutulan her şey]

## Tasklar
- TASK-N: [Task başlığı] — [Ajan] — [Model] — [~Xs]

## Bağımlılıklar
- EPIC-NNN gerektirir (neden)

## Tamamlanma Kriteri
- [ ] [Ölçülebilir sonuç 1]
- [ ] [Ölçülebilir sonuç 2]
- [ ] Bu epicteki tüm tasklar Done durumunda
- [ ] Kapsamda açık hata yok
```

---

## Task Oluşturma

### CLI ile (hızlı tasklar için önerilir)

```bash
backlog task create "Hız sınırlayıcı middleware uygula" \
  --priority high \
  --labels "epic001-foundation,developer,sonnet" \
  --dep 3 \
  --ac "Tüm endpoint'ler IP başına 100 istek/dk ile sınırlandırılmış" \
  --ac "429 yanıtı Retry-After başlığı içeriyor" \
  --ac "Hız sınırı yapılandırması settings.py'de (hardcoded değil)"
```

### Dosya ile (karmaşık tasklar için önerilir)

`backlog/tasks/task-N - Başlık.md` dosyasını aşağıdaki şablonu kullanarak elle oluşturun.

### Task Dosyası Şablonu

```markdown
---
id: TASK-N
assignee: []
title: "Kısa, emir kipinde task başlığı"
status: To Do
priority: high | medium | low
labels: ["epic00N-slug", "ajan-rol", "model-etiketi"]
dependencies:
  - task-N
acceptance_criteria:
  - "Gözlemlenebilir sonuç 1 (kullanıcı yönlü veya sistem düzeyinde)"
  - "Gözlemlenebilir sonuç 2"
created_date: 'YYYY-MM-DD SS:DD'
updated_date: 'YYYY-MM-DD SS:DD'
mhs_epic: EPIC-00N Başlık
mhs_agent: Developer | Analyst | Tester | Data Crawler | Data Visualizer
mhs_model: claude-sonnet-4-6 | claude-haiku-4-5 | claude-opus-4-7 | gemini-2.5-pro
mhs_estimated_tokens: 25000
mhs_estimated_hours: 2
---

# TASK-N — [Başlık]

## Açıklama
[Ne yapılacağını ve MHS için neden önemli olduğunu açıklayan 2–4 cümle.]

## Çıktılar
[Üretilecek spesifik dosyalar, endpoint'ler, bileşenler veya betikler.]

## Teknik Notlar
[Uygulama ipuçları, önemli kısıtlamalar, sınır durumlar veya kavram dokümanlarına referanslar.]

## Referanslar
- [concept/MHS_KB_02_Technical.md — ilgili bölüm]
- [ilgili ADR veya harici döküman]
```

---

## Draft Task Oluşturma

Henüz tam olarak belirtilmemiş fikirler için draft kullanın:

```bash
# Draft oluştur
backlog draft create "Aylık zorlukların oyunlaştırılmasını araştır"

# Tüm draftları listele
backlog draft list --plain

# Draft görüntüle
backlog draft view 1

# Hazır olduğunda gerçek taska terfi et
backlog draft promote 1

# Takip edilmeyecek drafti arşivle
backlog draft archive 1
```

---

## Task Yaşam Döngüsü

```
DRAFT → TO DO → IN PROGRESS → DONE → [arşiv/tamamlandı]
  ↑                  ↓
  └── geri al ←── (çalışma hazır olmadığını ortaya koyarsa)
```

| Durum | Anlamı | Kim Ayarlar |
|-------|--------|-------------|
| `To Do` | Belirtilmiş, başlamaya hazır | Herhangi biri |
| `In Progress` | Aktif olarak üzerinde çalışılıyor | Atanan kişi |
| `In Review` | Kod incelemesi bekleniyor | Atanan kişi |
| `Done` | Tüm kabul kriterleri karşılandı | Atanan kişi |

### CLI ile durum geçişleri

```bash
backlog task edit N --status "In Progress"
backlog task edit N --status "In Review"
backlog task edit N --status "Done"
backlog task archive N          # completed/ klasörüne taşı
backlog task demote N           # drafts'a geri al
```

---

## Döküman ve Karar Yönetimi

### Dökümanlar (spesifikasyonlar, entegrasyon rehberleri, raporlar)

```bash
# Döküman oluştur
backlog doc create "Idealist API Entegrasyon Rehberi" \
  --path docs/integrations/idealist.md

# Tüm dökümanları listele
backlog doc list --plain

# Döküman görüntüle
backlog doc view idealist-api
```

### Mimari Karar Kayıtları (ADR)

```bash
# Karar kaydet
backlog decision create "Şema yönetimi için Django migrations yerine Alembic kullan"

# ADR dosyaları backlog/decisions/ altında görünür
```

ADR şablonu (`backlog decision create` tarafından otomatik oluşturulur):

```markdown
# Karar: [Başlık]

## Durum: proposed | accepted | deprecated | superseded

## Bağlam
[Bu kararı zorunlu kılan durum neydi?]

## Karar
[Ne kararlaştırıldı?]

## Sonuçlar
[Ne daha kolaylaşıyor? Ne daha zorlaşıyor?]
```

---

## Kanban Board ve Tarayıcı Arayüzü

```bash
# Terminal Kanban board
backlog board

# Yatay düzen (varsayılan)
backlog board --layout horizontal

# Milestone'a göre grupla
backlog board --milestones

# Web tarayıcı arayüzü (takım değerlendirmeleri için önerilir)
backlog browser
# http://localhost:6420 adresinde açılır

# Board'ı Markdown olarak dışa aktar (asenkron paylaşım için)
backlog board export
backlog board export --filename "$(date +%Y-%m-%d)-sprint-degerlendirme.md"
```

---

## Bağımlılık Yönetimi

```bash
# Oluştururken bağımlılık belirt
backlog task create "Auth middleware ekle" --dep 3 --dep 4

# Mevcut taska bağımlılık ekle
backlog task edit 8 --dep 7

# Yürütme sırasını gör (tüm bağımlılıklara göre)
backlog sequence list --plain

# Blokersiz taskleri filtrele
backlog task list --plain   # (tüm bağımlılıkları Done olan taskleri kontrol et)
```

**MHS bağımlılık kuralları:**
- Bir task, tüm `dependencies`'i `Done` olmadan `In Progress`'e alınamaz
- Dairesel bağımlılık oluşturma
- Post-MVP tasklar (900+) MVP tasklara bağımlı olabilir, tersi geçerli değildir

---

## Task Şablonları

### Backend API Endpoint'i

```bash
backlog task create "GET /api/v1/scores/{user_id}" \
  --priority high \
  --labels "epic003-scoring,developer,sonnet" \
  --dep 7 \
  --ac "Kimliği doğrulanmış kullanıcı için MHS skor dağılımı döner" \
  --ac "Kullanıcı bulunamazsa 404 döner" \
  --ac "Başka kullanıcının özel verisine erişilirse 403 döner" \
  --ac "p95'te yanıt süresi < 200ms" \
  --ac "OpenAPI şeması güncellendi"
```

### Frontend Bileşeni

```bash
backlog task create "ScoreRingChart bileşeni" \
  --priority medium \
  --labels "epic012-frontend,developer,sonnet,data-visualizer" \
  --dep 5 \
  --dep 8 \
  --ac "recharts ile 6 kategorili radar grafiği render ediyor" \
  --ac "design-tokens.ts'den MHS_COLORS token'ları kullanıyor" \
  --ac "Erişilebilir: role=img, aria-label, sr-only figcaption" \
  --ac "data=[] olduğunda boş durum render ediliyor" \
  --ac "Storybook story'si eklendi"
```

### Veritabanı Migration

```bash
backlog task create "Activities tablosuna index ekle" \
  --priority high \
  --labels "epic001-foundation,developer,sonnet,database" \
  --dep 2 \
  --ac "1M satırda alembic upgrade head 30 saniyede tamamlanıyor" \
  --ac "EXPLAIN ANALYZE yaygın sorgularda index kullanımını gösteriyor" \
  --ac "alembic downgrade -1 temiz şekilde geri alıyor"
```

### Veri Kalitesi Kontrolü

```bash
backlog task create "Haftalık veri kalitesi raporu — activities tablosu" \
  --priority medium \
  --labels "epic011-ml-ai,data-analyst,haiku" \
  --ac "Betik production DB boyutunda < 5 dakikada çalışıyor" \
  --ac "Rapor reports/quality/YYYY-MM-DD-activities.md'ye yazılıyor" \
  --ac "Sıfır toleranslı ihlaller CI'ı başarısız kılıyor"
```

---

## MHS Etiket Kuralları

Etiketler `kategori-slug` formatını izler. Task başına birden fazla etiket kullanın.

### Epic etiketleri (her zaman bir tane ekle)

| Etiket | Epic |
|--------|------|
| `epic001-foundation` | EPIC-001 Temel Altyapı |
| `epic002-auth` | EPIC-002 Kimlik Doğrulama & Kullanıcı Profilleri |
| `epic003-scoring` | EPIC-003 MHS Puanlama Motoru |
| `epic004-activity` | EPIC-004 Aktivite Sistemi & Doğrulama |
| `epic006-badges` | EPIC-006 Rozet & Başarı Sistemi |
| `epic007-social` | EPIC-007 Sosyal Akış & Zaman Çizelgesi |
| `epic008-groups` | EPIC-008 Gruplar & Topluluklar |
| `epic009-integrations` | EPIC-009 Platform Entegrasyonları |
| `epic010-admin` | EPIC-010 Admin & Yönetişim |
| `epic011-ml-ai` | EPIC-011 ML/AI Servisleri |
| `epic012-frontend` | EPIC-012 Frontend UI/UX |
| `epic990-angel-ai` | EPIC-990 Angel AI (post-MVP) |

### Ajan / Rol etiketleri (her zaman bir tane ekle)

| Etiket | Rol |
|--------|-----|
| `developer` | Özellik geliştirme |
| `tester` | QA, test takımları |
| `data-analyst` | Veri kalitesi, etiketleme, MDM |
| `data-crawler` | Entegrasyonlar, tarayıcılar |
| `data-visualizer` | Grafikler, dashboard'lar, widget'lar |
| `reviewer` | Kod incelemesi, mimari |

### Model etiketleri (her zaman bir tane ekle)

| Etiket | Model | Ne Zaman Kullan |
|--------|-------|----------------|
| `sonnet` | claude-sonnet-4-6 | Karmaşık özellikler |
| `haiku` | claude-haiku-4-5 | Basit CRUD, testler |
| `opus` | claude-opus-4-7 | Mimari, analiz |
| `gemini-pro` | gemini-2.5-pro | Araştırma, crawling |

### Özel etiketler

| Etiket | Anlamı |
|--------|--------|
| `post-mvp` | MVP lansmanı için gerekli değil |
| `blocked` | Çözülmemiş harici bloker var |
| `database` | Şema veya migration değişikliği içeriyor |
| `security` | Güvenliğe duyarlı değişiklik |
| `ethics` | Puanlama algoritmasına veya önyargı mantığına dokunuyor |
| `sprint-1` ile `sprint-4` arası | Sprint ataması |

---

## AI Ajan Entegrasyonu

### MCP Sunucusu (önerilir)

Backlog.md MCP sunucusu, Claude Code'un CLI komutları olmadan doğrudan task okuyup yazmasını sağlar.

```bash
# Zaten yapılandırıldı — doğrula:
claude mcp list   # şunu göstermeli: backlog ✓ Connected

# Yeniden eklemeniz gerekirse:
claude mcp add backlog --scope user -- backlog mcp start
```

Claude Code oturumlarında şöyle diyebilirsiniz:
> "Task 7'yi In Progress'e al"
> "Scoring API'ye Redis önbelleği eklemek için bir task oluştur"
> "Task 19'u hangi tasklar bloke ediyor?"

### CCPM Skill (spesifikasyon odaklı geliştirme)

CCPM (`~/.claude/skills/ccpm`), PRD → Epic → GitHub Issues → Paralel Ajanlar iş akışını etkinleştirir.

```
Claude Code'da şöyle söyleyin:
  "Push bildirimleri eklemek için bir PRD yaz"
  "Bu PRD'yi bir epice dönüştür"
  "Epici tasklara ayır"
  "Taskleri GitHub Issues'a senkronize et"
  "Issue 7 üzerinde çalışmaya başla"
  "Standup'ı çalıştır"
```

### `backlog agents` — AI araçlarına talimatları senkronize et

```bash
# CLAUDE.md, AGENTS.md, GEMINI.md'yi mevcut backlog kurallarıyla güncelle
backlog agents --update-instructions
```
