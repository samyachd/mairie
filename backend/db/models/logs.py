from __future__ import annotations
from datetime import datetime, timezone
from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column
from db.db import Base

class Log(Base):
    __tablename__ = "logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey("user.id"), nullable=True)
    timestamp: Mapped[datetime] = mapped_column(default=lambda: datetime.now(timezone.utc))

    # Action
    action: Mapped[str] = mapped_column(String(50))      # "creation", "modification", "suppression"
    table_cible: Mapped[str] = mapped_column(String(50)) # "ordinateurs", "ecrans", "licences"
    item_id: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Détails optionnels
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)  # infos supplémentaires