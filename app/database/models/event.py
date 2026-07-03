from sqlalchemy import Column, String, Integer, ForeignKey, Text, Date, Time, Boolean, Enum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class EventStatus(str, enum.Enum):
    """Статусы события"""
    VOTING = "voting"
    CONFIRMED = "confirmed"
    ARCHIVED = "archived"


class Event(BaseModel):
    """Модель события (встречи)"""
    __tablename__ = "events"

    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    city = Column(String(255), nullable=True)
    event_date = Column(Date, nullable=True)
    event_time = Column(Time, nullable=True)
    is_online = Column(Boolean, default=False)
    status = Column(Enum(EventStatus), default=EventStatus.VOTING, nullable=False)

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    class_ = relationship("Class", back_populates="events")
    creator = relationship("User", back_populates="created_events", foreign_keys=[created_by])
    votes = relationship("EventVote", back_populates="event")

    def __repr__(self):
        return f"<Event(id={self.id}, title={self.title}, status={self.status})>"

    @property
    def yes_votes(self):
        return sum(1 for vote in self.votes if vote.vote == "yes")

    @property
    def maybe_votes(self):
        return sum(1 for vote in self.votes if vote.vote == "maybe")

    @property
    def no_votes(self):
        return sum(1 for vote in self.votes if vote.vote == "no")

    def has_voted(self, user_id: int) -> bool:
        return any(vote.user_id == user_id for vote in self.votes)