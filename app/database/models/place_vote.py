from sqlalchemy import Column, Integer, ForeignKey, String, Enum, UniqueConstraint
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class PlaceVoteAnswer(str, enum.Enum):
    """Варианты голосов за место"""
    YES = "yes"
    NO = "no"


class PlaceVote(BaseModel):
    """Голос за место"""
    __tablename__ = "place_votes"

    vote = Column(Enum(PlaceVoteAnswer), nullable=False)

    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__ = (
        UniqueConstraint("place_id", "user_id", name="unique_place_vote"),
    )

    # Relationships
    place = relationship("Place", back_populates="votes")
    user = relationship("User", back_populates="place_votes")

    def __repr__(self):
        return f"<PlaceVote(place_id={self.place_id}, user_id={self.user_id}, vote={self.vote})>"