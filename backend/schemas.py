# from __future__ import annotations
# Pydantic V2 doesn't require this for most simple schemas.
from pydantic import BaseModel, ConfigDict
from typing import Optional
# --- CHANGE 1: Import date and datetime to handle date/time types correctly ---
from datetime import date, datetime

# User Schemas
class UserBase(BaseModel):
    username: str
    
class UserCreate(UserBase):
    password: str
    role: str
    
class User(UserBase):
    id: int
    role: str
    # --- CHANGE 2: Updated from 'orm_mode = True' to 'model_config' for Pydantic V2 ---
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

# Assignment Schemas
class AssignmentBase(BaseModel):
    title: str
    description: str
    # --- NOTE: We keep this as `str` because the frontend sends a string from the form.
    due_date: str

class AssignmentCreate(AssignmentBase):
    pass

class Assignment(AssignmentBase):
    id: int
    teacher_id: int
    # --- CHANGE 3: Changed due_date to `date` to match the SQLAlchemy model's type ---
    due_date: date
    # --- CHANGE 4: Updated from 'orm_mode = True' to 'model_config' for Pydantic V2 ---
    model_config = ConfigDict(from_attributes=True)

# Submission Schemas
class SubmissionBase(BaseModel):
    submission_text: str
    
class SubmissionCreate(SubmissionBase):
    pass

class Submission(SubmissionBase):
    id: int
    # --- CHANGE 5: Changed submitted_at to `datetime` to match SQLAlchemy's DateTime type ---
    submitted_at: datetime
    student_id: int
    assignment_id: int
    submission_file: Optional[str]
    # --- CHANGE 6: Updated from 'orm_mode = True' to 'model_config' for Pydantic V2 ---
    model_config = ConfigDict(from_attributes=True)