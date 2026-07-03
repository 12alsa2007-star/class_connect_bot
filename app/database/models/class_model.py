from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel


class Class(BaseModel):
    """Модель класса/сообщества"""
    __tablename__ = "classes"

    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    graduation_year = Column(Integer, nullable=False)
    invite_code = Column(String(50), unique=True, nullable=False, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationships
    owner = relationship("User", back_populates="owned_classes", foreign_keys=[owner_id])
    members = relationship("ClassMember", back_populates="class_")
    events = relationship("Event", back_populates="class_")
    places = relationship("Place", back_populates="class_")

    def __repr__(self):
        return f"<Class(id={self.id}, name={self.name}, year={self.graduation_year})>"

    @property
    def member_count(self):
        return len(self.members)

    def get_member_role(self, user_id: int) -> str:
        for member in self.members:
            if member.user_id == user_id:
                return member.role
        return None

    def is_owner(self, user_id: int) -> bool:
        return self.owner_id == user_id

    def is_admin(self, user_id: int) -> bool:
        role = self.get_member_role(user_id)
        return role in ["owner", "admin"]

    def is_member(self, user_id: int) -> bool:
        return self.get_member_role(user_id) is not None