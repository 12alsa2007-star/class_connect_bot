from sqlalchemy import Column, Integer, ForeignKey, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class EventVoteAnswer(str, enum.Enum):
    """Варианты голосов за событие"""
    YES = "yes"
    MAYBE = "maybe"
    NO = "no"


class EventVote(BaseModel):
    """Голос за событие"""
    __tablename__ = "event_votes"

    vote = Column(Enum(EventVoteAnswer), nullable=False)

    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("event_id", "user_id", name="unique_event_vote"),
    )

    # Relationships
    event = relationship("Event", back_populates="votes")
    user = relationship("User", back_populates="event_votes")

    def __repr__(self):
        return f"<EventVote(event_id={self.event_id}, user_id={self.user_id}, vote={self.vote})>"