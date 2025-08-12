# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models.chat import User
from app.core.security import verify_password
from jose import jwt, JWTError
from fastapi import HTTPException, status
from app.config import settings
from typing import List
from sqlalchemy.orm import Session
from app.models.chat import RoomMember
from typing import Optional

def get_user_by_email(db: Session, email: str):
    """
    Fetch a user by email from the database.
    """
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate user by email and password.
    Returns user object if valid, else None.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user



def get_user_id_from_token(token: str, db: Session) -> Optional[int]:
    """
    Validate JWT token and return user ID if valid
    Args:
        token: JWT token string
        db: Database session
    Returns:
        user_id if valid, None otherwise
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            return None
            
        user = db.query(User).filter(User.email == email).first()
        if user is None:
            return None
            
        return user.id
    except JWTError as e:
        print(f"JWT Error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

def get_user_ids_in_room(room_id: int, db: Session) -> List[int]:
    """
    Get all user IDs in a specific chat room
    Args:
        room_id: ID of the chat room
        db: Database session
    Returns:
        List of user IDs in the room
    """
    try:
        members = db.query(RoomMember.user_id).filter(
            RoomMember.room_id == room_id
        ).all()
        return [member[0] for member in members] if members else []
    except Exception as e:
        print(f"Error getting room members: {e}")
        return []