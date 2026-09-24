from pydantic import BaseModel
from datetime import date


class PlacementDriveCreate(BaseModel):
    company_name: str
    job_role: str
    min_cgpa: float
    eligible_branch: str
    registration_link: str
    drive_date: date
    registration_deadline: date