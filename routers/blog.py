from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from .. import schemas, database, models


router = APIRouter()

get_db = database.get_db


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    blog = models.Blog(
        title=request.title, body=request.body, author_id=request.author_id
    )
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return blog


@router.get("/blogs", response_model=List[schemas.ShowBlog], tags=["Blogs"])
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    tags=["Blogs"],
)
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with id {id} is not found in DB",
        )
    return blog


@router.delete("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def delete_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog object with ID {id} is not found in the DB",
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return {"detail": f"Blog object with id {id} has been deleted successfully"}


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update_blog(
    id: int, request: schemas.Blog, response: Response, db: Session = Depends(get_db)
):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        new_blog = models.Blog(title=request.title, body=request.body)
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        response.status_code = 201
        return {
            "detail": "As there is no object available with this ID in the DB, \
                       hence created new Blog object with the payload."
        }
    blog.update(request.model_dump())
    db.commit()
    return {"detail": f"Blog with id {id} has successfully updated"}
