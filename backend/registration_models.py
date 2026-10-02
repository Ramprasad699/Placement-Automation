from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)

    student_id = Column(
        String,
        ForeignKey("students.student_id"),
        nullable=False
    )

    placement_drive_id = Column(
        Integer,
        ForeignKey("placement_drives.id"),
        nullable=False
    )

    status = Column(
        String,
        default="Registered",
        nullable=False
    )