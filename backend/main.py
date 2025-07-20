from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Import the IntegrityError to handle database constraints
from sqlalchemy.exc import IntegrityError

from . import models, auth, schemas
from .database import engine, get_db, Base
from .routers import users, assignments

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EdTech Assignment Tracker",
    description="API for managing assignments and submissions.",
    version="1.0.0"
)

# CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(assignments.router)

@app.post("/api/v1/auth/signup", status_code=status.HTTP_201_CREATED)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)

    # --- Change 1: Added try...except block to handle duplicate usernames ---
    try:
        db.commit()
        db.refresh(db_user)
        return {"message": "User created successfully."}
    except IntegrityError:
        # If a duplicate username is detected, roll back the session and raise a 400 error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered."
        )

@app.post("/api/v1/auth/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    access_token_expires = auth.timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # --- Change 2: Use user.id in the JWT payload for efficiency ---
    # This matches the change we made in users.py to look up users by ID
    access_token = auth.create_access_token(
        data={"id": user.id, "role": user.role}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}