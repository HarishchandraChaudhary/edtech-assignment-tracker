from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="student") # 'student' or 'teacher'

    assignments = relationship("Assignment", back_populates="teacher")
    submissions = relationship("Submission", back_populates="student")

class Assignment(Base):
    __tablename__ = "assignments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    due_date = Column(DateTime, default=datetime.datetime.now)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    
    teacher = relationship("User", back_populates="assignments")
    submissions = relationship("Submission", back_populates="assignment")

class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    submission_text = Column(String)
    submission_file = Column(String, nullable=True) # Path to the file
    submitted_at = Column(DateTime, default=datetime.datetime.now)
    student_id = Column(Integer, ForeignKey("users.id"))
    assignment_id = Column(Integer, ForeignKey("assignments.id"))
    
    student = relationship("User", back_populates="submissions")
    assignment = relationship("Assignment", back_populates="submissions")