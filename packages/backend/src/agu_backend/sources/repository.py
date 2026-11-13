import re
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import Engine, select
from sqlalchemy.dialects.postgresql import insert

from agu_backend.sources.models import RawVersion


class RawVersionRepository:
    """PostgreSQL adapter; calling code must store/check actual bytes separately."""

    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    def record_raw_version(
        self, source_id: UUID, sha256: str, storage_key: str, retrieved_at: datetime
    ) -> UUID:
        if retrieved_at.tzinfo is None or retrieved_at.utcoffset() is None:
            raise ValueError("retrieved_at must include timezone")
        if not re.fullmatch(r"[0-9a-f]{64}", sha256):
            raise ValueError("SHA-256 must be 64 lowercase hexadecimal characters")
        if not storage_key.strip() or len(storage_key) > 1024:
            raise ValueError("storage_key must have 1..1024 characters")

        with self.engine.begin() as connection:
            created = connection.execute(
                insert(RawVersion)
                .values(
                    id=uuid4(),
                    source_id=source_id,
                    sha256=sha256,
                    storage_key=storage_key,
                    retrieved_at=retrieved_at.astimezone(UTC),
                )
                .on_conflict_do_nothing(constraint="uq_raw_source_checksum")
                .returning(RawVersion.id)
            ).scalar_one_or_none()
            if created is not None:
                return created
            # Separate statement gets a new READ COMMITTED snapshot after the winning insert.
            return connection.execute(
                select(RawVersion.id).where(
                    RawVersion.source_id == source_id, RawVersion.sha256 == sha256
                )
            ).scalar_one()
