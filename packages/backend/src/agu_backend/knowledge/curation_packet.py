"""Minimal private handoff DTOs, not canonical facts or a publication decision.

Review state is reported input only. It cannot authorize serving, source approval,
or activation; those require the later reviewed-revision and bundle services.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Annotated, Literal, Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StrictBool, model_validator

NonEmptyString = Annotated[str, Field(min_length=1, strict=True)]


class FactDraft(BaseModel):
    """Source-preserving scalar proposal; type-specific production schemas follow later."""

    model_config = ConfigDict(extra="forbid")

    key: NonEmptyString
    value: NonEmptyString
    value_type: Literal["text", "number", "date", "code"]
    source_locator: NonEmptyString
    date_precision: Literal["date", "datetime"] | None

    @model_validator(mode="after")
    def validate_value(self) -> Self:
        if not self.key.strip() or not self.value.strip() or not self.source_locator.strip():
            raise ValueError("Fact key, value and source locator must not be blank")
        if self.value_type == "date":
            if self.date_precision == "date":
                parsed_date = date.fromisoformat(self.value)
                if parsed_date.isoformat() != self.value:
                    raise ValueError("Date-only values must retain YYYY-MM-DD precision")
            elif self.date_precision == "datetime":
                parsed_datetime = datetime.fromisoformat(self.value)
                if parsed_datetime.tzinfo is None or parsed_datetime.utcoffset() is None:
                    raise ValueError("Datetime values require an explicit timezone")
            else:
                raise ValueError("Date values require explicit date precision")
        elif self.date_precision is not None:
            raise ValueError("Date precision applies only to date values")
        if self.value_type == "number":
            try:
                numeric_value = Decimal(self.value)
            except InvalidOperation as error:
                raise ValueError("Number values must be decimal strings") from error
            if not numeric_value.is_finite():
                raise ValueError("Number values must be finite")
        return self


class CurationPacket(BaseModel):
    """Private proposal preserving unknown applicability and outstanding quality issues."""

    model_config = ConfigDict(extra="forbid")

    synthetic: StrictBool
    raw_version_id: UUID
    academic_year: Annotated[int, Field(strict=True, ge=1, le=9999)] | None
    program_scope: Literal["all", "specific", "unknown"]
    program_ids: list[NonEmptyString]
    review_state: Literal["draft", "in_review", "approved", "rejected"]
    quality_warnings: list[NonEmptyString]
    facts: list[FactDraft]

    @model_validator(mode="after")
    def validate_scope(self) -> Self:
        if self.program_scope == "specific":
            if not self.program_ids or any(not value.strip() for value in self.program_ids):
                raise ValueError("Specific program scope requires nonblank program IDs")
            if len(set(self.program_ids)) != len(self.program_ids):
                raise ValueError("Specific program IDs must be unique")
        elif self.program_ids:
            raise ValueError("All/unknown scope cannot carry specific program IDs")
        return self
