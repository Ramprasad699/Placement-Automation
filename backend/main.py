from fastapi import FastAPI, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .database import Base, engine

from . import (
    models,
    schemas,
    placement_models,
    placement_schemas,
    registration_models,
    registration_schemas,
    excel_report

)

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

@app.post("/students/{student_id}/register/{drive_id}")
def register_student(
    student_id: str,
    drive_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()

    if not student:
        return {
            "message": "Student not found"
        }

    drive = db.query(placement_models.PlacementDrive).filter(
        placement_models.PlacementDrive.id == drive_id
    ).first()

    if not drive:
        return {
            "message": "Placement drive not found"
        }

    if student.cgpa < drive.min_cgpa:
        return {
            "message": "Student is not eligible for this drive"
        }

    if student.branch != drive.eligible_branch:
        return {
            "message": "Student branch is not eligible for this drive"
        }

    existing_registration = db.query(
        registration_models.Registration
    ).filter(
        registration_models.Registration.student_id == student_id,
        registration_models.Registration.placement_drive_id == drive_id
    ).first()

    if existing_registration:
        return {
            "message": "Student already registered for this drive"
        }

    new_registration = registration_models.Registration(
        student_id=student_id,
        placement_drive_id=drive_id,
        status="Registered"
    )

    db.add(new_registration)
    db.commit()
    db.refresh(new_registration)

    return {
        "message": "Student registered successfully!",
        "student_id": student_id,
        "placement_drive_id": drive_id,
        "status": new_registration.status
    }

@app.get("/students/{student_id}/registrations")
def get_student_registrations(
    student_id: str,
    db: Session = Depends(get_db)
):
    registrations = db.query(
        registration_models.Registration
    ).filter(
        registration_models.Registration.student_id == student_id
    ).all()

    result = []

    for registration in registrations:
        drive = db.query(
            placement_models.PlacementDrive
        ).filter(
            placement_models.PlacementDrive.id == registration.placement_drive_id
        ).first()

        if drive:
            result.append({
                "company_name": drive.company_name,
                "job_role": drive.job_role,
                "status": registration.status,
                "drive_date": drive.drive_date,
                "registration_deadline": drive.registration_deadline
            })

    return result

@app.get("/placement-drives/{drive_id}/registrations")
def get_drive_registrations(
    drive_id: int,
    db: Session = Depends(get_db)
):
    drive = db.query(
        placement_models.PlacementDrive
    ).filter(
        placement_models.PlacementDrive.id == drive_id
    ).first()

    if not drive:
        return {
            "message": "Placement drive not found"
        }

    registrations = db.query(
        registration_models.Registration
    ).filter(
        registration_models.Registration.placement_drive_id == drive_id
    ).all()

    result = []

    for registration in registrations:
        student = db.query(
            models.Student
        ).filter(
            models.Student.student_id == registration.student_id
        ).first()

        if student:
            result.append({
                "student_id": student.student_id,
                "name": student.name,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "status": registration.status
            })

    return result

@app.get("/placement-drives/{drive_id}/not-registered")
def get_not_registered_students(
    drive_id: int,
    db: Session = Depends(get_db)
):
    drive = db.query(
        placement_models.PlacementDrive
    ).filter(
        placement_models.PlacementDrive.id == drive_id
    ).first()

    if not drive:
        return {
            "message": "Placement drive not found"
        }

    eligible_students = db.query(
        models.Student
    ).filter(
        models.Student.cgpa >= drive.min_cgpa,
        models.Student.branch == drive.eligible_branch
    ).all()

    result = []

    for student in eligible_students:
        registration = db.query(
            registration_models.Registration
        ).filter(
            registration_models.Registration.student_id == student.student_id,
            registration_models.Registration.placement_drive_id == drive_id
        ).first()

        if not registration:
            result.append({
                "student_id": student.student_id,
                "name": student.name,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "status": "Not Registered"
            })

    return 

@app.get("/placement-drives/{drive_id}/registrations/excel")
def download_registration_report(
    drive_id: int,
    db: Session = Depends(get_db)
):
    drive = db.query(
        placement_models.PlacementDrive
    ).filter(
        placement_models.PlacementDrive.id == drive_id
    ).first()

    if not drive:
        return {
            "message": "Placement drive not found"
        }

    registrations = db.query(
        registration_models.Registration
    ).filter(
        registration_models.Registration.placement_drive_id == drive_id
    ).all()

    result = []

    for registration in registrations:
        student = db.query(
            models.Student
        ).filter(
            models.Student.student_id == registration.student_id
        ).first()

        if student:
            result.append({
                "student_id": student.student_id,
                "name": student.name,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "status": registration.status
            })

    filename = f"registration_report_{drive_id}.xlsx"

    excel_report.create_registration_report(
        result,
        filename
    )

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )

@app.get("/placement-drives/{drive_id}/not-registered/excel")
def download_not_registered_report(
    drive_id: int,
    db: Session = Depends(get_db)
):
    drive = db.query(
        placement_models.PlacementDrive
    ).filter(
        placement_models.PlacementDrive.id == drive_id
    ).first()

    if not drive:
        return {
            "message": "Placement drive not found"
        }

    eligible_students = db.query(
        models.Student
    ).filter(
        models.Student.cgpa >= drive.min_cgpa,
        models.Student.branch == drive.eligible_branch
    ).all()

    result = []

    for student in eligible_students:
        registration = db.query(
            registration_models.Registration
        ).filter(
            registration_models.Registration.student_id == student.student_id,
            registration_models.Registration.placement_drive_id == drive_id
        ).first()

        if not registration:
            result.append({
                "student_id": student.student_id,
                "name": student.name,
                "branch": student.branch,
                "cgpa": student.cgpa,
                "status": "Not Registered"
            })

    filename = f"not_registered_report_{drive_id}.xlsx"

    excel_report.create_registration_report(
        result,
        filename
    )

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=filename
    )