import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db
from .users import get_current_user
from typing import List
from datetime import datetime

router = APIRouter(prefix="/api/v1/assignments", tags=["assignments"])

def check_teacher_role(user: models.User):
    if user.role != "teacher":
        raise HTTPException(status_code=403, detail="Not authorized to perform this action.")

@router.post("/", response_model=schemas.Assignment)
def create_assignment(
    assignment: schemas.AssignmentCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_teacher_role(current_user)

    try:
        due_date_obj = datetime.strptime(assignment.due_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid due date format. Please use YYYY-MM-DD."
        )

    db_assignment = models.Assignment(
        title=assignment.title,
        description=assignment.description,
        due_date=due_date_obj,
        teacher_id=current_user.id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

@router.get("/", response_model=List[schemas.Assignment])
def get_assignments(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    assignments = db.query(models.Assignment).all()
    return assignments

@router.post("/{assignment_id}/submit", status_code=status.HTTP_201_CREATED)
def submit_assignment(
    assignment_id: int,
    submission_text: str = Form(...),
    submission_file: UploadFile = File(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can submit assignments.")

    file_path = None
    if submission_file:
        if not os.path.exists("uploads"):
            os.makedirs("uploads")
        file_location = f"uploads/{submission_file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(submission_file.file.read())
        file_path = file_location

    db_submission = models.Submission(
        submission_text=submission_text,
        submission_file=file_path,
        student_id=current_user.id,
        assignment_id=assignment_id
    )
    db.add(db_submission)
    db.commit()
    return {"message": "Submission received successfully."}

@router.get("/{assignment_id}/submissions", response_model=List[schemas.Submission])
def view_submissions(
    assignment_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    check_teacher_role(current_user)
    submissions = db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()
    return submissions