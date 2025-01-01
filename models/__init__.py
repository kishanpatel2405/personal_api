from datetime import datetime

from sqlalchemy import Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, Mapped, mapped_column, declarative_base

Base = declarative_base()


class Country(Base):
    __tablename__ = "country_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    iso2: Mapped[str] = mapped_column(String, index=True)
    iso3: Mapped[str] = mapped_column(String, index=True)
    phone_code: Mapped[str] = mapped_column(String, index=True)
    currency: Mapped[str] = mapped_column(String, index=True)
    currency_name: Mapped[str] = mapped_column(String, index=True)
    currency_symbol: Mapped[str] = mapped_column(String, index=True)
    emoji: Mapped[str] = mapped_column(String, index=True)
    emoji_iu: Mapped[str] = mapped_column(String, index=True)

    states: Mapped[list["State"]] = relationship("State", back_populates="country", cascade="all, delete-orphan")


class State(Base):
    __tablename__ = "state_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    state_code: Mapped[str] = mapped_column(String, index=True)
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("country_data.id"))

    country: Mapped["Country"] = relationship("Country", back_populates="states")
    cities: Mapped[list["City"]] = relationship("City", back_populates="state", cascade="all, delete-orphan")


class City(Base):
    __tablename__ = "city_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, index=True)
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("state_data.id"))

    state: Mapped["State"] = relationship("State", back_populates="cities")


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
    country_id: Mapped[int] = mapped_column(Integer, ForeignKey("country_data.id"), nullable=True)
    state_id: Mapped[int] = mapped_column(Integer, ForeignKey("state_data.id"), nullable=True)
    city_id: Mapped[int] = mapped_column(Integer, ForeignKey("city_data.id"), nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    country = relationship("Country", back_populates="users")
    state = relationship("State", back_populates="users")
    city = relationship("City", back_populates="users")
