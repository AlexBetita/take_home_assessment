from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from db import User, Session, get_db, verify_password, create_access_token, get_password_hash

router = APIRouter(
    tags=["auth"],
    responses={404: {"description": "Endpoint not found"}},
)

class UserData(BaseModel):
    username: str = Field(..., min_length=3, description="Username must be at least 3 characters long")
    password: str = Field(..., min_length=3, description="Password must be at least 3 characters long")

@router.post("/signup")
def signup(signup_data: UserData, db: Session = Depends(get_db)):
    username = signup_data.username
    password = signup_data.password
    
    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    hashed_password = get_password_hash(password)
    new_user = User(username=username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully", "user_id": new_user.id, "username": new_user.username}

@router.post("/login")
def login(login_data: UserData, db: Session = Depends(get_db)):
    username = login_data.username
    password = login_data.password
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    # token = create_access_token({"sub": user.username})
    # return {"access_token": token, "token_type": "bearer"}
    return {"user_id": user.id, "username": user.username}

@router.post("/logout")
def logout():
    return {"message": "Logged out"}