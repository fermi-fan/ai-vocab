from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(Integer, primary_key=True,)

    content: Mapped[str]  = mapped_column(String(200), nullable=False,)

    entry_type: Mapped[str] = mapped_column(String(20), nullable=False,)

    chinese_meaning: Mapped[str] = mapped_column(Text, nullable=False, default="",)

    explanation: Mapped[str] = mapped_column(Text, nullable=False, default="",)

    part_of_speech: Mapped[str] = mapped_column(String(50), nullable=False, default="unknown",)

    familiarity_level: Mapped[int] = mapped_column(Integer, nullable=False, default=0,)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False,)

    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False,)

