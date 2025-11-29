from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from core.base_model import BaseModel


class Token(BaseModel):
    """
    Model for storing refresh tokens in the database.

    In the hybrid model, only refresh tokens are stored in the database.
    Access tokens are JWT (stateless) and don't need to be stored.
    """
    __tablename__ = "auth_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(255), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("auth_users.id"), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationship with user
    user = relationship("User", back_populates="tokens")
