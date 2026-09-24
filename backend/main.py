from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .database import Base, engine
from . import models, schemas, placement_models, placement_schemas

app = FastAPI(title="Placement Automation")


Base.metadata.create_all(bind=engine)


def get_db():
    db = Session(bind=engine)
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home():
    return {
        "message": "Placement Automation API is running!"
    }

@app.post("/students")
def create_student(
    student: schemas.StudentCreate,
    db: Session = Depends(get_db)
):
    new_student = models.Student(
        student_id=student.student_id,
        name=student.name,
        email=student.email,
        password=student.password,
        branch=student.branch,
        cgpa=student.cgpa
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return {
        "message": "Student created successfully!",
        "student_id": new_student.student_id
    }
@app.post("/placement-drives")
def create_placement_drive(
    drive: placement_schemas.PlacementDriveCreate,
    db: Session = Depends(get_db)
):
    new_drive = placement_models.PlacementDrive(
        company_name=drive.company_name,
        job_role=drive.job_role,
        min_cgpa=drive.min_cgpa,
        eligible_branch=drive.eligible_branch,
        registration_link=drive.registration_link,
        drive_date=drive.drive_date,
        registration_deadline=drive.registration_deadline
    )

    db.add(new_drive)
    db.commit()
    db.refresh(new_drive)

    return {
        "message": "Placement drive created successfully!",
        "company_name": new_drive.company_name
    }

@app.get("/students/{student_id}/eligible-drives")
def get_eligible_drives(
    student_id: str,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        return {
            "message": "Student not found"
        }

    drives = db.query(placement_models.PlacementDrive).filter(
        placement_models.PlacementDrive.min_cgpa <= student.cgpa,
        placement_models.PlacementDrive.eligible_branch == student.branch
    ).all()

    return drives