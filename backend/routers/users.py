from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .. import models, schemas, auth
from ..database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

# --- Modification 1: Added redirect_slashes=False for flexibility ---
router = APIRouter(prefix="/api/v1/users", tags=["users"], redirect_slashes=False)

# Define a constant for the common exception
CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> models.User:
    """
    Dependency function to get the current authenticated user from a JWT.

    Raises a 401 Unauthorized exception if the token is invalid or the user
    is not found.
    """
    try:
        # --- Modification 2: Use user ID in the JWT payload for faster lookup ---
        payload = auth.jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise CREDENTIALS_EXCEPTION
    except auth.JWTError:
        raise CREDENTIALS_EXCEPTION
    
    # Query the database for the user by ID
    user = db.query(models.User).filter(models.User.id == user_id).first()
    
    if user is None:
        raise CREDENTIALS_EXCEPTION
    
    return user

@router.get("/me/", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    """
    Returns the details of the currently authenticated user.
    """
    return current_user