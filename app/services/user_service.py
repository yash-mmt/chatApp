# app/services/user_service.py

from sqlalchemy.orm import Session
from app.models.chat import User
from app.core.security import verify_password


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
