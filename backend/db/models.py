from datetime import datetime
from typing import Optional

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Boolean, CheckConstraint, Numeric, SmallInteger, String, Integer, BigInteger, DateTime, ForeignKey, func


class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    father_name: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    email: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(200), nullable=False)

    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())


class Producers(Base):
    __tablename__ = "producers"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Watches(Base):
    __tablename__ = "watches"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    producer_id: Mapped[int] = mapped_column(ForeignKey('producers.id', ondelete="CASCADE"), nullable=False)
    is_whatertightness: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    released_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    size_milimetrs: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False, info={
        "check": CheckConstraint(
            "type IN ('electronical', 'mechanical', 'hybrid')",
            name='valid_type'
        )
    })
    count: Mapped[int] = mapped_column(SmallInteger, nullable=False, info={
        'check': CheckConstraint(
            "count >= 0",
            name='check_count'
        )
    })
    gender: Mapped[str] = mapped_column(String(10), nullable=False, default='unisex', info={
        'check': CheckConstraint(
            "gender IN ('unisex', 'male', 'female')",
            name='valid_gender'
    )})
    price: Mapped[float] = mapped_column(Numeric, nullable=False, info={
        'check': CheckConstraint(
            "price > 0.00",
            name='check_price'
        )
    })

    # подумать что еще добавить


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class VerificationCodes(Base):
    __tablename__ = "verification_codes"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    code: Mapped[int] = mapped_column(SmallInteger, nullable=False)


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), onupdate=func.now())


class Discounts(Base):
    __tablename__ = "discounts"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    discount_code: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    discount_percent: Mapped[int] = mapped_column(SmallInteger, nullable=False)

class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    total_price: Mapped[int] = mapped_column(Numeric, nullable=False, info={
        'check': CheckConstraint(
            "total_price > 0.00",
            name='check_total_price'
        )
    })
    discount: Mapped[Optional[int]] = mapped_column(ForeignKey('discounts.id', ondelete="CASCADE"), nullable=True, default=None)

    is_pickup: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    delivery_address: Mapped[Optional[str]] = mapped_column(String(150), nullable=True)


    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class OrdersWatches(Base):
    __tablename__ = "orders_watches"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id', ondelete="CASCADE"), nullable=False)
    watch_id: Mapped[int] = mapped_column(ForeignKey('watches.id', ondelete="CASCADE"), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class AdminLogs(Base):
    __tablename__ = "admin_logs"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, nullable=False)
    admin_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete="SET NULL"), nullable=True)
    action: Mapped[str] = mapped_column(String(50), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN
    entity: Mapped[str] = mapped_column(String(50), nullable=False)  # users, watches, orders, etc.
    entity_id: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    ip_address: Mapped[Optional[str]] = mapped_column(String(45), nullable=True)  # IPv6

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())