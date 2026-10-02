from pydantic import BaseModel


class RegistrationCreate(BaseModel):
    student_id: str
    placement_drive_id: int