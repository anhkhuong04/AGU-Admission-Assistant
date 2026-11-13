"""Source identity and immutable raw revisions; not publication eligibility."""

import sqlalchemy as sa
from alembic import op

revision = "0001_source_raw_identity"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm")
    op.create_table(
        "sources",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("canonical_url", sa.String(2048), nullable=False, unique=True),
    )
    op.create_table(
        "raw_versions",
        sa.Column("id", sa.Uuid(), primary_key=True),
        sa.Column("source_id", sa.Uuid(), sa.ForeignKey("sources.id"), nullable=False),
        sa.Column("sha256", sa.String(64), nullable=False),
        sa.Column("storage_key", sa.String(1024), nullable=False),
        sa.Column("retrieved_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("source_id", "sha256", name="uq_raw_source_checksum"),
        sa.CheckConstraint("sha256 ~ '^[0-9a-f]{64}$'", name="ck_raw_sha256"),
        sa.CheckConstraint("length(storage_key) > 0", name="ck_raw_storage_key"),
    )
    op.execute("""
        CREATE FUNCTION reject_raw_version_update() RETURNS trigger LANGUAGE plpgsql AS $$
        BEGIN
            RAISE EXCEPTION 'raw revisions are immutable; record a new revision';
        END;
        $$
    """)
    op.execute("""
        CREATE TRIGGER raw_versions_immutable BEFORE UPDATE ON raw_versions
        FOR EACH ROW EXECUTE FUNCTION reject_raw_version_update()
    """)


def downgrade() -> None:
    # Forward-only: retention/deletion and restore must be explicitly planned, never automatic.
    raise RuntimeError("Forward-only migration; restore a reviewed backup instead")
