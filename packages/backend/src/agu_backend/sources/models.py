from datetime import datetime
from uuid import UUID

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[UUID] = mapped_column(primary_key=True)
    canonical_url: Mapped[str] = mapped_column(String(2048), unique=True)


class RawVersion(Base):
    __tablename__ = "raw_versions"
    __table_args__ = (
        UniqueConstraint("source_id", "sha256", name="uq_raw_source_checksum"),
        CheckConstraint("sha256 ~ '^[0-9a-f]{64}$'", name="ck_raw_sha256"),
        CheckConstraint("length(storage_key) > 0", name="ck_raw_storage_key"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True)
    source_id: Mapped[UUID] = mapped_column(ForeignKey("sources.id"))
    sha256: Mapped[str] = mapped_column(String(64))
    storage_key: Mapped[str] = mapped_column(String(1024))
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
