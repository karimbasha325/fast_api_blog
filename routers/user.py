from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List

from .. import schemas, database, models, hashing


router = APIRouter()

get_db = database.get_db


@router.post("/user", status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    try:
        hashed_pwd = hashing.Hash.get_password_hash(request.password)
        new_user = models.User(
            name=request.name,
            email=request.email,
            password=hashed_pwd,
            is_active=request.is_active,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "detail": f"User with name {request.name} has been created sucessfully!"
        }
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"An user with email {request.email} is already existed in our system. \
                     Please try with another email address.",
        )


@router.get(
    "/users",
    response_model=List[schemas.ShowUser],
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get(
    "/user/{email}",
    response_model=schemas.ShowUser,
    status_code=status.HTTP_200_OK,
    tags=["Users"],
)
def get_user_details(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found the user with this email.",
        )
    return user


@router.delete("/user/{email}", status_code=status.HTTP_200_OK, tags=["Users"])
def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with email {email} is not found.",
        )
    db.delete(user)
    db.commit()
    return {"detail": "Deleted Successfully"}
