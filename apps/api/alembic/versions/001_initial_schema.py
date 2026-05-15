"""Initial schema: users, mhs_scores, activities, connected_platforms, badges, groups

Revision ID: 001
Revises:
Create Date: 2026-04-27
"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # ── users ─────────────────────────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("username", sa.String(50), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=True),
        sa.Column("display_name", sa.String(100), nullable=True),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("country_code", sa.String(3), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("is_verified", sa.Boolean(), server_default="false", nullable=False),
        sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("deleted_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # ── mhs_scores ────────────────────────────────────────────────────────────
    op.create_table(
        "mhs_scores",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("total_score", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("social_impact", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("environmental", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("knowledge_innovation", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("economic_contribution", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("cultural_artistic", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("civic_political", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("carbon_penalty", sa.Numeric(5, 2), server_default="0", nullable=False),
        sa.Column("toxicity_penalty", sa.Numeric(5, 2), server_default="0", nullable=False),
        sa.Column("network_multiplier", sa.Numeric(4, 3), server_default="1.000", nullable=False),
        sa.Column(
            "consistency_multiplier", sa.Numeric(4, 3), server_default="1.000", nullable=False
        ),
        sa.Column(
            "geo_equity_multiplier", sa.Numeric(4, 3), server_default="1.000", nullable=False
        ),
        sa.Column("score_level", sa.String(30), server_default="awakening", nullable=False),
        sa.Column(
            "calculated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_mhs_scores_user_id", "mhs_scores", ["user_id"])
    op.create_index("ix_mhs_scores_total", "mhs_scores", ["total_score"])

    # ── activities ────────────────────────────────────────────────────────────
    op.create_table(
        "activities",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("category", sa.String(50), nullable=False),
        sa.Column("subcategory", sa.String(50), nullable=True),
        sa.Column("impact_points", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("evidence_url", sa.String(500), nullable=True),
        sa.Column("evidence_type", sa.String(50), nullable=True),
        sa.Column("status", sa.String(30), server_default="pending", nullable=False),
        sa.Column("verification_level", sa.Integer(), server_default="0", nullable=False),
        sa.Column("activity_date", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_activities_user_id", "activities", ["user_id"])
    op.create_index("ix_activities_category", "activities", ["category"])
    op.create_index("ix_activities_status", "activities", ["status"])

    # ── connected_platforms ───────────────────────────────────────────────────
    op.create_table(
        "connected_platforms",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("platform", sa.String(50), nullable=False),
        sa.Column("platform_user_id", sa.String(255), nullable=True),
        sa.Column("platform_username", sa.String(255), nullable=True),
        sa.Column("access_token_encrypted", sa.Text(), nullable=True),
        sa.Column("refresh_token_encrypted", sa.Text(), nullable=True),
        sa.Column("token_expires_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column("last_synced_at", sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id", "platform", name="uq_user_platform"),
    )
    op.create_index("ix_connected_platforms_user_id", "connected_platforms", ["user_id"])

    # ── badges ────────────────────────────────────────────────────────────────
    op.create_table(
        "badges",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("badge_type", sa.String(50), nullable=False),
        sa.Column("badge_code", sa.String(50), nullable=False),
        sa.Column("badge_layer", sa.Integer(), nullable=False),
        sa.Column(
            "awarded_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_badges_user_id", "badges", ["user_id"])
    op.create_index("ix_badges_badge_code", "badges", ["badge_code"])

    # ── groups ────────────────────────────────────────────────────────────────
    op.create_table(
        "groups",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("group_type", sa.String(30), server_default="open", nullable=False),
        sa.Column("avatar_url", sa.String(500), nullable=True),
        sa.Column("owner_id", sa.UUID(), nullable=False),
        sa.Column("collective_score", sa.Numeric(7, 2), server_default="0", nullable=False),
        sa.Column("member_count", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default="true", nullable=False),
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_groups_slug", "groups", ["slug"], unique=True)
    op.create_index("ix_groups_owner_id", "groups", ["owner_id"])

    # ── group_members (join table) ────────────────────────────────────────────
    op.create_table(
        "group_members",
        sa.Column("group_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("role", sa.String(20), server_default="member", nullable=False),
        sa.Column(
            "joined_at",
            sa.TIMESTAMP(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["group_id"], ["groups.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("group_id", "user_id"),
    )

    # ── updated_at trigger function ───────────────────────────────────────────
    op.execute("""
        CREATE OR REPLACE FUNCTION update_updated_at_column()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = now();
            RETURN NEW;
        END;
        $$ language 'plpgsql';
    """)

    # mhs_scores uses calculated_at (not updated_at), so it is excluded from this trigger
    for table in ("users", "activities", "groups"):
        op.execute(f"""
            CREATE TRIGGER trg_{table}_updated_at
            BEFORE UPDATE ON {table}
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
        """)


def downgrade() -> None:
    for table in ("users", "activities", "groups"):
        op.execute(f"DROP TRIGGER IF EXISTS trg_{table}_updated_at ON {table};")

    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column();")

    op.drop_table("group_members")
    op.drop_table("groups")
    op.drop_table("badges")
    op.drop_table("connected_platforms")
    op.drop_table("activities")
    op.drop_table("mhs_scores")
    op.drop_table("users")
