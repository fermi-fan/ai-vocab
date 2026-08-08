from pydantic import BaseModel, ConfigDict, Field, field_validator
from enum import StrEnum


class EntryType(StrEnum):
    WORD = "word"
    PHRASE = "phrase"
    SENTENCE = "sentence"


class EntryCreate(BaseModel):
    content: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="用户选中的单词、短语或句子",
    )
    context: str | None = Field(
        default=None,
        max_length=2000,
        description="临时上下文，只用于 AI 判断语境，不保存",
    )

    @field_validator("content")
    @classmethod
    def validate_content(cls, value: str) -> str:
        content = value.strip()

        if not content:
            raise ValueError("Content cannot be empty")

        return content

    @field_validator("context")
    @classmethod
    def clean_context(cls, value: str | None) -> str | None:
        if value is None:
            return None

        context = value.strip()

        if not context:
            return None

        return context

class EntryUpdate(BaseModel):
    familiarity_level: int | None = Field(
        default=None,
        ge=0,
        le=5,
        description="熟悉度等级，范围为 0 到 5",
    )

class EntryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    entry_type: EntryType
    chinese_meaning: str
    explanation: str
    part_of_speech: str
    familiarity_level: int


class EntryListResponse(BaseModel):
    total: int
    items: list[EntryResponse]


class EntryDeleteResponse(BaseModel):
    message: str
    deleted: EntryResponse