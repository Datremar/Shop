import enum

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Enum,
    DateTime,
    func, Float, ForeignKey
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Gender(enum.Enum):
    male = "male"
    female = "female"


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String, nullable=False)
    patronymic = Column(String, nullable=True, default=None)
    surname = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    gender = Column(Enum(Gender), default=None)
    email = Column(String, nullable=False, unique=True)
    consent = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    profile_pic_dir = Column(String, nullable=True, default=None)


class Good(Base):
    __tablename__ = "Goods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)


class Purchase(Base):
    __tablename__ = "Purchases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    buyer_id = Column(Integer, ForeignKey("Users.id", ondelete="CASCADE"), nullable=False)
    purchased_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", backref="Users")


class PurchaseEntry(Base):
    __tablename__ = "PurchaseEntries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    item_id = Column(Integer, ForeignKey("Goods.id", ondelete="CASCADE"), nullable=False)
    item_quantity = Column(Integer, nullable=False)
    summary_price = Column(Float, nullable=False)

    purchase_id = Column(Integer, ForeignKey("Purchases.id", ondelete="CASCADE"), nullable=False)

    good = relationship("Good", backref="Goods")
    purchase = relationship("Purchase", backref="Purchases")
