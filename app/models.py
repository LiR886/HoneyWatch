from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class LoginAttempt(Base):
    __tablename__ = "login_attempts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False,
    )
    source_ip: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    password_provided: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    password_length: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    user_agent: Mapped[str] = mapped_column(Text, default="", nullable=False)
    endpoint: Mapped[str] = mapped_column(String(255), default="/login", nullable=False)
    method: Mapped[str] = mapped_column(String(16), default="POST", nullable=False)


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
        nullable=False,
    )
    alert_type: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    source_ip: Mapped[str] = mapped_column(String(64), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
