from sqlalchemy import Column, Integer, ForeignKey, String, UniqueConstraint, Enum
from sqlalchemy.orm import relationship
import enum
from .base import BaseModel


class MemberRole(str, enum.Enum):
    """Роли участника в классе"""
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class ClassMember(BaseModel):
    """Связь пользователя и класса"""
    __tablename__ = "class_members"

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(Enum(MemberRole), default=MemberRole.MEMBER, nullable=False)

    __table_args__ = (
        UniqueConstraint("class_id", "user_id", name="unique_class_member"),
    )

    # Relationships
    class_ = relationship("Class", back_populates="members")
    user = relationship("User", back_populates="class_memberships")

    def __repr__(self):
        return f"<ClassMember(class_id={self.class_id}, user_id={self.user_id}, role={self.role})>"

    @property
    def is_admin(self) -> bool:
        return self.role in [MemberRole.OWNER, MemberRole.ADMIN]

    @property
    def is_owner(self) -> bool:
        return self.role == MemberRole.OWNER
        