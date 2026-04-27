# EPIC-006 — Badge & Achievement System

## Status: `blocked` (needs EPIC-003)
## Priority: P1 (Sprint 2)

## Goal
Implement all 4 badge layers with automatic award logic and display components.

## Scope

### Layer 1 — Score-level badges (7, automatic)
🌱 Awakening (0-99) → 🌟 Rising Star (100-249) → 💫 Contributor (250-399)
→ ⭐ Impact Maker (400-549) → 🏆 Change Agent (550-699)
→ 🌍 Humanity Champion (700-849) → 👑 Humanity Legend (850-1000)

### Layer 2 — Activity badges (17)
Volunteer 🤲, Academic 📖, Inventor 💡, Blood Donor 🩸, Climate Warrior 🌳,
Ocean Guardian 🌊, Food Hero 🍽️, Coder 💻, Educator 🎓, Artist 🎨,
Peacekeeper ☮️, Crisis Responder 🆘, Elder 🐣, Time Giver ⌛,
Heartbeat ❤️‍🔥, Timeless ⏳, Pathfinder 🧭

### Layer 3 — Honorary titles (11)
Angel 👼, Butterfly 🦋, Peacemaker 🤍, Diamond 💎, Healer 🩺,
Peace 🕊️, Champion 🏅, Hero 🆘, Scientist 🔬, Seedling 🌱, Dev 💻

### Layer 4 — Group/collective badges (5)

## Tasks
- TASK-030: Badge showcase component (frontend)
- Badge award logic is part of TASK-007 (score calculator)
- Group badges are part of TASK-024 (collective MHS)

## Definition of Done
- [ ] Level badge automatically updates when score crosses threshold
- [ ] Activity badges awarded when activity criteria met
- [ ] Badge grid displays correctly on profile page
- [ ] Badge metadata (criteria, rarity) accessible via API
