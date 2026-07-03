from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Place(BaseModel):
    """Модель места для встречи"""
    __tablename__ = "places"

    title = Column(String(255), nullable=False)
    address = Column(String(500), nullable=False)
    comment = Column(Text, nullable=True)

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    class_ = relationship("Class", back_populates="places")
    creator = relationship("User", back_populates="proposed_places", foreign_keys=[created_by])
    votes = relationship("PlaceVote", back_populates="place")

    def __repr__(self):
        return f"<Place(id={self.id}, title={self.title}, address={self.address})>"

    @property
    def yes_votes(self):
        return sum(1 for vote in self.votes if vote.vote == "yes")

    @property
    def no_votes(self):
        return sum(1 for vote in self.votes if vote.vote == "no")

    def has_voted(self, user_id: int) -> bool:
        return any(vote.user_id == user_id for vote in self.votes)