from sqlalchemy import Column, String, BigInteger, Date
from sqlalchemy.orm import relationship
from datetime import date
from .base import BaseModel


class User(BaseModel):
    """Модель пользователя"""
    __tablename__ = "users"

    telegram_id = Column(BigInteger, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True, index=True)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    phone = Column(String(20), nullable=True)
    city = Column(String(255), nullable=True)
    birthday = Column(Date, nullable=True)

    # Relationships
    owned_classes = relationship("Class", back_populates="owner", foreign_keys="Class.owner_id")
    class_memberships = relationship("ClassMember", back_populates="user")
    created_events = relationship("Event", back_populates="creator", foreign_keys="Event.created_by")
    event_votes = relationship("EventVote", back_populates="user")
    proposed_places = relationship("Place", back_populates="creator", foreign_keys="Place.created_by")
    place_votes = relationship("PlaceVote", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, name={self.first_name})>"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def is_registered(self):
        return all([self.first_name, self.last_name, self.city, self.birthday])