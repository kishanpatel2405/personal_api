from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import (Mapped, declarative_base, mapped_column,
                            relationship)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    is_active: Mapped[str] = mapped_column(Boolean, default=True)
    title: Mapped[str] = mapped_column(String, nullable=True)
    first_name: Mapped[str] = mapped_column(String, nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    cell_country_code: Mapped[str] = mapped_column(String, nullable=True)
    mobile_number: Mapped[str] = mapped_column(String, nullable=True)
    address: Mapped[str] = mapped_column(String, nullable=True)
    country_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("country_data.id"), nullable=True
    )
    state_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("state_data.id"), nullable=True
    )
    city_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("city_data.id"), nullable=True
    )
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=True)
\






