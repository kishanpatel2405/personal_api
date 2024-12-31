from sqlalchemy import Integer, String, ForeignKey
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
