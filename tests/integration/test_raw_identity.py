import os
from concurrent.futures import ThreadPoolExecutor
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, select, text
from sqlalchemy.engine import make_url

from agu_backend.sources.models import RawVersion, Source
from agu_backend.sources.repository import RawVersionRepository


@pytest.fixture
def engine():  # type: ignore[no-untyped-def]
    url = os.getenv("TEST_DATABASE_URL")
    if not url:
        pytest.fail("Set TEST_DATABASE_URL to a dedicated, migrated *_test database")
    if not (make_url(url).database or "").endswith("_test"):
        pytest.fail("Refusing a database whose name does not end with _test")
    database = create_engine(url)
    yield database
    database.dispose()


def test_changed_bytes_create_revision_and_retry_preserves_original(engine) -> None:  # type: ignore[no-untyped-def]
    source_id = uuid4()
    retrieved = datetime(2026, 11, 13, tzinfo=UTC)
    with engine.begin() as connection:
        connection.execute(
            Source.__table__.insert().values(
                id=source_id, canonical_url=f"https://example.invalid/synthetic/{source_id}"
            )
        )
    repository = RawVersionRepository(engine)
    first = repository.record_raw_version(source_id, "a" * 64, "fixture:first", retrieved)
    retry = repository.record_raw_version(
        source_id, "a" * 64, "fixture:retry", datetime(2026, 11, 14, tzinfo=UTC)
    )
    second = repository.record_raw_version(source_id, "b" * 64, "fixture:second", retrieved)
    assert first == retry
    assert second != first
    with engine.connect() as connection:
        row = connection.execute(select(RawVersion.__table__).where(RawVersion.id == first)).one()
        assert row.storage_key == "fixture:first"
        assert row.retrieved_at == retrieved


def test_concurrent_retries_deduplicate(engine) -> None:  # type: ignore[no-untyped-def]
    source_id = uuid4()
    with engine.begin() as connection:
        connection.execute(
            Source.__table__.insert().values(
                id=source_id, canonical_url=f"https://example.invalid/synthetic/{source_id}"
            )
        )
    repository = RawVersionRepository(engine)
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(
            executor.map(
                lambda _: repository.record_raw_version(
                    source_id, "c" * 64, "fixture:concurrent", datetime.now(UTC)
                ),
                range(2),
            )
        )
    assert results[0] == results[1]
    with engine.connect() as connection:
        assert (
            len(
                connection.execute(
                    select(RawVersion.id).where(RawVersion.source_id == source_id)
                ).all()
            )
            == 1
        )


def test_naive_timestamp_rejected_before_connection(engine) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(ValueError, match="timezone"):
        RawVersionRepository(engine).record_raw_version(
            uuid4(), "a" * 64, "fixture:naive", datetime(2026, 11, 13)
        )


@pytest.mark.parametrize("checksum", ["invalid", "a" * 63, "G" * 64])
def test_invalid_checksum_rejected(engine, checksum) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(ValueError, match="SHA-256"):
        RawVersionRepository(engine).record_raw_version(
            uuid4(), checksum, "fixture:bad", datetime.now(UTC)
        )


def test_extensions_present(engine) -> None:  # type: ignore[no-untyped-def]
    with engine.connect() as connection:
        extensions = set(connection.execute(text("SELECT extname FROM pg_extension")).scalars())
    assert {"vector", "pg_trgm"} <= extensions


def test_raw_revision_rejects_sql_mutation(engine) -> None:  # type: ignore[no-untyped-def]
    source_id = uuid4()
    with engine.begin() as connection:
        connection.execute(
            Source.__table__.insert().values(
                id=source_id, canonical_url=f"https://example.invalid/synthetic/{source_id}"
            )
        )
    version = RawVersionRepository(engine).record_raw_version(
        source_id, "f" * 64, "fixture:immutable", datetime.now(UTC)
    )
    with pytest.raises(Exception, match="immutable"):
        with engine.begin() as connection:
            connection.execute(
                RawVersion.__table__.update()
                .where(RawVersion.id == version)
                .values(storage_key="fixture:overwritten")
            )
