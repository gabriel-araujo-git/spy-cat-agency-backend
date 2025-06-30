from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SpyCat, status_code=status.HTTP_201_CREATED)
def create_spy_cat(cat: schemas.SpyCatCreate, db: Session = Depends(get_db)):
    db_cat = crud.create_spy_cat(db, cat)
    if not db_cat:
        raise HTTPException(status_code=400, detail="Invalid breed")
    return db_cat

@router.get("/", response_model=list[schemas.SpyCat])
def read_spy_cats(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    cats = crud.get_spy_cats(db, skip=skip, limit=limit)
    return cats

@router.get("/{cat_id}", response_model=schemas.SpyCat)
def read_spy_cat(cat_id: int, db: Session = Depends(get_db)):
    cat = crud.get_spy_cat(db, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return cat

@router.patch("/{cat_id}", response_model=schemas.SpyCat)
def update_salary(cat_id: int, salary_update: schemas.SpyCatUpdate, db: Session = Depends(get_db)):
    cat = crud.update_spy_cat_salary(db, cat_id, salary_update.salary)
    if not cat:
        raise HTTPException(status_code=404, detail="Spy cat not found")
    return cat

@router.delete("/{cat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cat(cat_id: int, db: Session = Depends(get_db)):
    success = crud.delete_spy_cat(db, cat_id)
    if not success:
        raise HTTPException(status_code=400, detail="Cat not found or assigned to mission")
