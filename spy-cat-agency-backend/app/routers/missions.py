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

@router.post("/", response_model=schemas.Mission, status_code=status.HTTP_201_CREATED)
def create_mission(mission: schemas.MissionCreate, db: Session = Depends(get_db)):
    db_mission = crud.create_mission(db, mission)
    if not db_mission:
        raise HTTPException(status_code=400, detail="Invalid cat assignment or cat unavailable")
    return db_mission

@router.get("/", response_model=list[schemas.Mission])
def read_missions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    missions = crud.get_missions(db, skip=skip, limit=limit)
    return missions

@router.get("/{mission_id}", response_model=schemas.Mission)
def read_mission(mission_id: int, db: Session = Depends(get_db)):
    mission = crud.get_mission(db, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission

@router.delete("/{mission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_mission(mission_id: int, db: Session = Depends(get_db)):
    success = crud.delete_mission(db, mission_id)
    if not success:
        raise HTTPException(status_code=400, detail="Mission not found or assigned to a cat")

@router.patch("/targets/{target_id}/notes", response_model=schemas.Target)
def update_notes(target_id: int, notes_update: dict, db: Session = Depends(get_db)):
    notes = notes_update.get("notes")
    if notes is None:
        raise HTTPException(status_code=400, detail="Notes field required")
    target = crud.update_target_notes(db, target_id, notes)
    if not target:
        raise HTTPException(status_code=400, detail="Target completed or mission completed or not found")
    return target

@router.patch("/targets/{target_id}/complete", response_model=schemas.Target)
def complete_target(target_id: int, db: Session = Depends(get_db)):
    target = crud.mark_target_completed(db, target_id)
    if not target:
        raise HTTPException(status_code=404, detail="Target not found")
    return target

@router.patch("/{mission_id}/assign/{cat_id}", response_model=schemas.Mission)
def assign_cat(mission_id: int, cat_id: int, db: Session = Depends(get_db)):
    mission = crud.assign_cat_to_mission(db, mission_id, cat_id)
    if not mission:
        raise HTTPException(status_code=400, detail="Mission or cat not found or cat unavailable or mission already assigned")
    return mission
