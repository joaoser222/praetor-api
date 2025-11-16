from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from core.base_model import Base, TimestampMixin

role_permissions = Table(
    'auth_role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permissions.id'), primary_key=True)
)

class Role(Base, TimestampMixin, AsyncAttrs):
    __tablename__ = "auth_roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255))

    permissions = relationship("Permission", secondary=role_permissions, backref="roles", lazy="selectin")

