from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    student_id: str
    name: str
    email: EmailStr
    password: str
    branch: str
    cgpa: float

class StudentLogin(BaseModel):
    email: EmailStr
    password: str