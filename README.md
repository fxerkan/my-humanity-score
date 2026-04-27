<div align="center">

# 🌍 My Humanity Score (MHS)

### *"Your impact on humanity — measured, tracked, and celebrated."*

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL%203.0-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Status: Pre-MVP](https://img.shields.io/badge/Status-Pre--MVP-orange.svg)]()

**[🇹🇷 Türkçe](#türkçe) · [🇬🇧 English](#english)**

</div>

---

## English

**My Humanity Score** is a 100% free, open-source platform that measures, visualizes, and celebrates every person's positive contribution to humanity — without any discrimination based on religion, language, race, gender, nationality, disability, or political affiliation.

### What it does

Users build a verifiable **MHS Score (0–1000)** by logging, claiming, and connecting activities that positively impact society across 6 weighted categories:

| Category                  | Weight | Examples                                      |
| ------------------------- | ------ | --------------------------------------------- |
| 🤝 Social Impact          | 25%    | Volunteering, mentoring, community leadership |
| 🌱 Environmental          | 20%    | Carbon reduction, conservation, clean energy  |
| 💡 Knowledge & Innovation | 20%    | Open source, research, patents, teaching      |
| 💼 Economic Contribution  | 15%    | Job creation, entrepreneurship, donations     |
| 🎨 Cultural & Artistic    | 10%    | Art, music, cultural heritage                 |
| 🗳️ Civic & Political    | 10%    | Rights advocacy, democracy, peacebuilding     |

### Score Levels

| Level             | Score     |    |
| ----------------- | --------- | -- |
| Awakening         | 0–99     | 🌱 |
| Rising Star       | 100–199  | 🌟 |
| Contributor       | 200–349  | 💫 |
| Impact Maker      | 350–499  | ⭐ |
| Change Agent      | 500–649  | 🏆 |
| Humanity Champion | 650–799  | 🌍 |
| Humanity Legend   | 800–1000 | 👑 |

### Core Principles

- **100% Free forever** — no paid plans, no corporate subscriptions
- **Fully open source** — AGPL-3.0 license, copyleft protection
- **Community governed** — RFC voting, transparent algorithm
- **Zero discrimination** — `FORBIDDEN_SCORING_FEATURES` enforced at code level
- **Transparent scoring** — algorithm published and auditable by anyone

### Tech Stack

| Layer     | Technology                                                      |
| --------- | --------------------------------------------------------------- |
| Frontend  | Next.js 15 (App Router) + TypeScript + Tailwind CSS + shadcn/ui |
| Backend   | FastAPI (Python 3.12) + SQLAlchemy 2 + Alembic                  |
| Database  | PostgreSQL 16 + Redis 7 + Neo4j                                 |
| ML / AI   | HuggingFace Transformers + Llama/Mistral (Angel AI)             |
| Queue     | Celery + Redis                                                  |
| Container | Docker Compose                                                  |
| CI/CD     | GitHub Actions                                                  |

### Project Status

> **Pre-MVP** — Foundation & planning phase. Target: working demo by May 31, 2026.

See [`backlog/docs/sprints/pre-mvp-plan.md`](backlog/docs/sprints/pre-mvp-plan.md) for the detailed roadmap.

### Getting Started (Development)

```bash
# Clone
git clone https://github.com/fxerkan/my-humanity-score.git
cd my-humanity-score

# Start all services
docker compose up -d

# Seed demo data (after first boot)
docker compose exec api python scripts/seed_demo.py

# Open the app
open http://localhost:3000

# API docs
open http://localhost:8000/docs
```

### Repository Structure

```
my-humanity-score/
├── CLAUDE.md              ← AI agent master context
├── AGENTS.md              ← Agent roles & routing
├── README.md              ← This file
├── apps/
│   ├── web/               ← Next.js 15 frontend
│   ├── api/               ← FastAPI backend
│   └── ml/                ← ML scoring services
├── packages/
│   ├── score-engine/      ← MHS calculation core
│   ├── angel-ai/          ← Angel AI module
│   └── shared/            ← Shared types & utils
├── backlog/               ← Backlog.md task management
│   ├── tasks/             ← 47 active tasks
│   ├── docs/epics/        ← 12 epics
│   └── docs/sprints/      ← Sprint plans
├── concept/               ← Product concept docs (read-only reference)
├── scripts/               ← Dev tooling & migration scripts
└── docs/                  ← Architecture, ethics, ADRs
```

### Task Management

This project uses [Backlog.md](https://github.com/MrLesk/Backlog.md) for task management.

```bash
# Install
npm i -g backlog.md

# View tasks
backlog board
backlog browser          # Web UI at http://localhost:6420

# See Pre-MVP milestones
backlog milestone list --plain
```

See [`backlog/README.md`](backlog/README.md) for the full workflow guide.

### Contributing

This project is community-driven. Before contributing:

1. Read [`CLAUDE.md`](CLAUDE.md) — master context for all contributors and AI agents
2. Read [`AGENTS.md`](AGENTS.md) — agent roles and task routing
3. Read [`concept/MHS_KB_02_Technical.md`](concept/MHS_KB_02_Technical.md) — technical architecture
4. Pick a task from `backlog board` and move it to "In Progress"
5. One PR per task. Tests required.

### Ethics Charter

The MHS scoring algorithm **must never** use:

```python
FORBIDDEN_SCORING_FEATURES = [
    'religion', 'ethnicity', 'race', 'gender', 'sexual_orientation',
    'nationality', 'language', 'disability', 'political_affiliation',
    'economic_status', 'education_level'
]
```

Annual bias audits are published publicly. See [`concept/MHS_KB_02_Technical.md`](concept/MHS_KB_02_Technical.md) for the full ethics charter.

### License

[GNU Affero General Public License v3.0](LICENSE) — copyleft, all derivatives must remain open source.

---

## Türkçe

**İnsalık Skorum**, her insanın insanlığa olan olumlu katkısını — din, dil, ırk, cinsiyet, milliyet, engellilik veya siyasi görüş ayrımı gözetmeksizin — ölçen, görselleştiren ve kutlayan %100 ücretsiz, açık kaynaklı bir platformdur.

### Ne Yapar?

Kullanıcılar, topluma olumlu katkı sağlayan aktivitelerini kayıt altına alarak, talep ederek ve bağlayarak 6 ağırlıklı kategoride doğrulanabilir bir **MHS Skoru (0–1000)** oluşturur:

| Kategori              | Ağırlık | Örnekler                                         |
| --------------------- | ---------- | ------------------------------------------------- |
| 🤝 Sosyal Etki        | %25        | Gönüllülük, mentorluk, toplum liderliği      |
| 🌱 Çevre             | %20        | Karbon azaltımı, koruma, temiz enerji           |
| 💡 Bilgi & İnovasyon | %20        | Açık kaynak, araştırma, patent, öğretmenlik |
| 💼 Ekonomik Katkı    | %15        | İş yaratma, girişimcilik, bağış             |
| 🎨 Kültür & Sanat   | %10        | Sanat, müzik, kültürel miras                   |
| 🗳️ Sivil & Siyasi   | %10        | Haklar savunuculuğu, demokrasi, barış          |

### Temel İlkeler

- **Sonsuza kadar %100 ücretsiz** — ücretli plan yok, kurumsal abonelik yok
- **Tam açık kaynak** — AGPL-3.0 lisansı, copyleft koruması
- **Topluluk yönetimi** — RFC oylaması, şeffaf algoritma
- **Sıfır ayrımcılık** — `FORBIDDEN_SCORING_FEATURES` kod düzeyinde zorunlu kılınmış
- **Şeffaf puanlama** — algoritma herkes tarafından incelenebilir

### Proje Durumu

> **Pre-MVP** — Temel altyapı ve planlama aşaması. Hedef: 31 Mayıs 2026'ya kadar çalışan demo.

Ayrıntılı yol haritası için [`backlog/docs/sprints/pre-mvp-plan.md`](backlog/docs/sprints/pre-mvp-plan.md) dosyasına bakın.

### Geliştirmeye Başlama

```bash
# Klon
git clone https://github.com/fxerkan/my-humanity-score.git
cd my-humanity-score

# Tüm servisleri başlat
docker compose up -d

# Demo verisi yükle (ilk başlatmadan sonra)
docker compose exec api python scripts/seed_demo.py

# Uygulamayı aç
open http://localhost:3000

# API dökümantasyonu
open http://localhost:8000/docs
```

### Katkıda Bulunma

Katkıda bulunmadan önce:

1. [`CLAUDE.md`](CLAUDE.md) — tüm katkıcılar ve AI ajanlar için ana bağlam
2. [`AGENTS.md`](AGENTS.md) — ajan rolleri ve görev yönlendirme
3. `backlog board` üzerinden bir task seçin
4. Bir PR = Bir task. Test zorunludur.

### Lisans

[GNU Affero General Public License v3.0](LICENSE) — copyleft, tüm türevler açık kaynak kalmalıdır.

---

<div align="center">

Made with 🤖 & ❤️ for humanity by [FXerkan](https://github.com/fxerkan/my-humanity-score) · AGPL-3.0

</div>
