from pydantic import BaseModel, Field, validator
from typing import List, Optional

class SpyCatBase(BaseModel):
    name: str
    years_of_experience: int = Field(..., ge=0)
    breed: str
    salary: float = Field(..., ge=0)

class SpyCatCreate(SpyCatBase):
    pass

class SpyCatUpdate(BaseModel):
    salary: float = Field(..., ge=0)

class SpyCat(SpyCatBase):
    id: int

    class Config:
        orm_mode = True

class TargetBase(BaseModel):
    name: str
    country: str
    notes: Optional[str] = ""
    completed: bool = False

class TargetCreate(TargetBase):
    pass

class Target(TargetBase):
    id: int

    class Config:
        orm_mode = True

class MissionBase(BaseModel):
    completed: bool = False

class MissionCreate(MissionBase):
    cat_id: Optional[int] = None
    targets: List[TargetCreate]

    @validator("targets")
    def validate_targets_count(cls, v):
        if not (1 <= len(v) <= 3):
            raise ValueError("Mission must have between 1 and 3 targets")
        return v

class Mission(MissionBase):
    id: int
    cat_id: Optional[int]
    targets: List[Target]

    class Config:
        orm_mode = True
