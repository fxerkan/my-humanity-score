#!/usr/bin/env python3
"""Seed script — creates 5 realistic demo users with MHS scores.

Run inside the API container:
    docker compose exec api python /app/scripts/seed_demo.py

Or from the project root (if API port is mapped to 8001):
    docker compose exec api python scripts/seed_demo.py
"""

import asyncio
import sys
from decimal import Decimal
from typing import Any, cast

# Add the API source root to the path so imports work.
sys.path.insert(0, "/app")

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import settings
from core.security import hash_password
from models.score import MHSScore
from models.user import User

# ── Demo user definitions ─────────────────────────────────────────────────────

DEMO_PASSWORD = "Demo1234!"

DEMO_USERS = [
    {
        "username": "elif_kaya",
        "email": "elif@demo.mhs",
        "display_name": "Elif Kaya",
        "bio": "Environmental activist and secondary school teacher. I believe education is the most powerful tool for change. 🌱",
        "country_code": "TUR",
        "score": {
            "total_score": Decimal("342.00"),
            "social_impact": Decimal("68.00"),
            "environmental": Decimal("74.00"),
            "knowledge_innovation": Decimal("52.00"),
            "economic_contribution": Decimal("42.00"),
            "cultural_artistic": Decimal("38.00"),
            "civic_political": Decimal("68.00"),
            "score_level": "advocate",
        },
    },
    {
        "username": "marcus_johnson",
        "email": "marcus@demo.mhs",
        "display_name": "Marcus Johnson",
        "bio": "Open source developer and weekend volunteer at the local food bank. Code for good. 💻",
        "country_code": "USA",
        "score": {
            "total_score": Decimal("438.00"),
            "social_impact": Decimal("95.00"),
            "environmental": Decimal("62.00"),
            "knowledge_innovation": Decimal("98.00"),
            "economic_contribution": Decimal("58.00"),
            "cultural_artistic": Decimal("40.00"),
            "civic_political": Decimal("85.00"),
            "score_level": "advocate",
        },
    },
    {
        "username": "yuna_park",
        "email": "yuna@demo.mhs",
        "display_name": "Yuna Park",
        "bio": "Community organiser, muralist, and jazz musician. Art is how we speak when words fail. 🎨",
        "country_code": "KOR",
        "score": {
            "total_score": Decimal("305.00"),
            "social_impact": Decimal("72.00"),
            "environmental": Decimal("38.00"),
            "knowledge_innovation": Decimal("45.00"),
            "economic_contribution": Decimal("30.00"),
            "cultural_artistic": Decimal("82.00"),
            "civic_political": Decimal("38.00"),
            "score_level": "advocate",
        },
    },
    {
        "username": "amir_hassan",
        "email": "amir@demo.mhs",
        "display_name": "Amir Hassan",
        "bio": "Medical researcher at Cairo University. Regular blood and plasma donor. Science saves lives. 🔬",
        "country_code": "EGY",
        "score": {
            "total_score": Decimal("378.00"),
            "social_impact": Decimal("82.00"),
            "environmental": Decimal("44.00"),
            "knowledge_innovation": Decimal("95.00"),
            "economic_contribution": Decimal("55.00"),
            "cultural_artistic": Decimal("22.00"),
            "civic_political": Decimal("80.00"),
            "score_level": "advocate",
        },
    },
    {
        "username": "sofia_rossi",
        "email": "sofia@demo.mhs",
        "display_name": "Sofia Rossi",
        "bio": "Social entrepreneur building circular economy solutions in Milan. Climate action is business sense. ♻️",
        "country_code": "ITA",
        "score": {
            "total_score": Decimal("392.00"),
            "social_impact": Decimal("78.00"),
            "environmental": Decimal("88.00"),
            "knowledge_innovation": Decimal("58.00"),
            "economic_contribution": Decimal("82.00"),
            "cultural_artistic": Decimal("30.00"),
            "civic_political": Decimal("56.00"),
            "score_level": "advocate",
        },
    },
]


async def seed(session: AsyncSession) -> None:
    """Insert demo users and scores; skip any that already exist."""
    created = 0
    skipped = 0

    for data in DEMO_USERS:
        existing = await session.scalar(select(User).where(User.email == data["email"]))
        if existing:
            print(f"  ⏭  {data['display_name']} already exists — skipping")
            skipped += 1
            continue

        user = User(
            username=data["username"],
            email=data["email"],
            display_name=data["display_name"],
            bio=data["bio"],
            country_code=data["country_code"],
            hashed_password=hash_password(DEMO_PASSWORD),
            is_active=True,
            is_verified=True,
        )
        session.add(user)
        await session.flush()  # get user.id

        score_data = cast(dict[str, Any], data["score"])
        score = MHSScore(
            user_id=user.id,
            total_score=score_data["total_score"],
            social_impact=score_data["social_impact"],
            environmental=score_data["environmental"],
            knowledge_innovation=score_data["knowledge_innovation"],
            economic_contribution=score_data["economic_contribution"],
            cultural_artistic=score_data["cultural_artistic"],
            civic_political=score_data["civic_political"],
            score_level=score_data["score_level"],
        )
        session.add(score)
        created += 1
        print(
            f"  ✅  {data['display_name']} (@{data['username']}) — MHS {score_data['total_score']}"
        )

    await session.commit()
    print(f"\nDone. Created: {created}  |  Skipped (already exist): {skipped}")
    print("\nDemo credentials (all users):")
    print(f"  Password: {DEMO_PASSWORD}")
    for d in DEMO_USERS:
        print(f"  {d['email']}")


async def main() -> None:
    engine = create_async_engine(settings.database_url, echo=False)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    print("🌱 Seeding MHS demo users...\n")
    async with async_session() as session:
        await seed(session)

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(main())
