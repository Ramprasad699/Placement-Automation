from sqlalchemy import Column, Integer, String, Float, Date
from .database import Base


class PlacementDrive(Base):
    __tablename__ = "placement_drives"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, nullable=False)
    job_role = Column(String, nullable=False)
    min_cgpa = Column(Float, nullable=False)
    eligible_branch = Column(String, nullable=False)
    registration_link = Column(String, nullable=False)
    drive_date = Column(Date, nullable=False)
    registration_deadline = Column(Date, nullable=False)