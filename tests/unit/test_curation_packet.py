import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from agu_backend.knowledge.curation_packet import CurationPacket, FactDraft

FIXTURE = Path(__file__).parents[1] / "fixtures/synthetic/curation-packet.json"


def packet_data() -> dict[str, object]:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def test_round_trip_preserves_unknown_scope_draft_and_ocr_warning() -> None:
    packet = CurationPacket.model_validate(packet_data())
    restored = CurationPacket.model_validate_json(packet.model_dump_json())
    assert restored == packet
    assert restored.synthetic is True
    assert restored.academic_year is None
    assert restored.program_scope == "unknown"
    assert restored.program_ids == []
    assert restored.review_state == "draft"
    assert restored.quality_warnings == ["ocr_table_warning"]
    assert restored.facts[0].value == "2026-12-01"
    assert restored.facts[0].date_precision == "date"
    assert "public_ready" not in restored.model_dump()


@pytest.mark.parametrize(
    ("scope", "ids"),
    [("specific", []), ("all", ["fixture-M"]), ("unknown", ["fixture-M"])],
)
def test_scope_does_not_silently_expand(scope: str, ids: list[str]) -> None:
    data = packet_data() | {"program_scope": scope, "program_ids": ids}
    with pytest.raises(ValidationError):
        CurationPacket.model_validate(data)


def test_specific_scope_keeps_explicit_values() -> None:
    packet = CurationPacket.model_validate(
        packet_data() | {"program_scope": "specific", "program_ids": ["fixture-M"]}
    )
    assert packet.program_ids == ["fixture-M"]
    assert packet.academic_year is None


@pytest.mark.parametrize("field", ["public_ready", "human_approval_actor"])
def test_rejects_unowned_publication_or_approval_fields(field: str) -> None:
    with pytest.raises(ValidationError):
        CurationPacket.model_validate(packet_data() | {field: True})


@pytest.mark.parametrize(
    ("value_type", "value", "precision"),
    [
        ("number", "NaN", None),
        ("number", "Infinity", None),
        ("number", "not-a-number", None),
        ("date", "2026-02-30", "date"),
        ("date", "2026-12-01T23:59:00", "datetime"),
        ("date", "2026-12-01", None),
        ("text", "fixture", "date"),
        ("code", " ", None),
    ],
)
def test_invalid_typed_values_are_rejected(
    value_type: str, value: str, precision: str | None
) -> None:
    with pytest.raises(ValidationError):
        FactDraft.model_validate(
            {
                "key": "fixture-value",
                "value": value,
                "value_type": value_type,
                "source_locator": "synthetic/page-1/table-1/row-2",
                "date_precision": precision,
            }
        )


@pytest.mark.parametrize(
    ("value_type", "value", "precision"),
    [
        ("number", "0", None),
        ("number", "123.40", None),
        ("code", "00120", None),
        ("date", "2026-12-01T09:30:00+07:00", "datetime"),
    ],
)
def test_valid_values_preserve_source_representation(
    value_type: str, value: str, precision: str | None
) -> None:
    fact = FactDraft.model_validate(
        {
            "key": "fixture-value",
            "value": value,
            "value_type": value_type,
            "source_locator": "synthetic/page-1/table-1/row-2",
            "date_precision": precision,
        }
    )
    assert fact.value == value


@pytest.mark.parametrize("ids", [[" "], ["fixture-M", "fixture-M"]])
def test_specific_scope_rejects_blank_or_duplicate_ids(ids: list[str]) -> None:
    with pytest.raises(ValidationError):
        CurationPacket.model_validate(
            packet_data() | {"program_scope": "specific", "program_ids": ids}
        )


def test_date_value_does_not_infer_academic_year() -> None:
    packet = CurationPacket.model_validate(packet_data())
    assert packet.facts[0].value.startswith("2026")
    assert packet.academic_year is None
