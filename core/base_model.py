from datetime import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.sql import func



class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)


class BaseModel(DeclarativeBase, TimestampMixin, AsyncAttrs):
    """
    Base model for all database models.
    Includes timestamp mixin and async attributes support.
    """
    __abstract__ = True