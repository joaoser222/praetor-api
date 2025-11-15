from sqlalchemy import Boolean, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from core.base_model import Base, TimestampMixin

user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)

class User(Base, TimestampMixin, AsyncAttrs):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=False)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String(100))
    
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)

    roles = relationship("Role", secondary=user_roles, backref="users", lazy="selectin")