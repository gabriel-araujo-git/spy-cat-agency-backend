from sqlalchemy.orm import Session
from app import models, schemas
import requests


BREEDS = [
  "Abyssinian",
  "American Bobtail",
  "American Curl",
  "American Shorthair",
  "American Wirehair",
  "Arabian Mau",
  "Australian Mist",
  "Balinese",
  "Bambino",
  "Bengal",
  "Birman",
  "Bombay",
  "British Longhair",
  "British Shorthair",
  "Burmese",
  "Burmilla",
  "California Spangled",
  "Chantilly-Tiffany",
  "Chartreux",
  "Chausie",
  "Cheetoh",
  "Colorpoint Shorthair",
  "Cornish Rex",
  "Cymric",
  "Cyprus",
  "Devon Rex",
  "Donskoy",
  "Dragon Li",
  "Egyptian Mau",
  "European Burmese",
  "Exotic Shorthair",
  "Havana Brown",
  "Himalayan",
  "Japanese Bobtail",
  "Javanese",
  "Khao Manee",
  "Korat",
  "Kurilian",
  "LaPerm",
  "Maine Coon",
  "Malayan",
  "Manx",
  "Munchkin",
  "Nebelung",
  "Norwegian Forest Cat",
  "Ocicat",
  "Oriental",
  "Persian",
  "Pixie-bob",
  "Ragamuffin",
  "Ragdoll",
  "Russian Blue",
  "Savannah",
  "Scottish Fold",
  "Selkirk Rex",
  "Siamese",
  "Siberian",
  "Singapura",
  "Snowshoe",
  "Somali",
  "Sphynx",
  "Tonkinese",
  "Toyger",
  "Turkish Angora",
  "Turkish Van",
  "York Chocolate"
]

def validate_breed(breed: str) -> bool:
    if breed in BREEDS:
        return True
    return False

#def validate_breed(breed: str) -> bool:
#    try:
#        response = requests.get(THECATAPI_BREEDS_URL, timeout=5)
#        if response.status_code != 200:
#            return False
#        breeds = response.json()
#        return any(breed.lower() in b['name'].lower() for b in breeds)
#    except requests.RequestException:
#        return False


# SpyCats
def get_spy_cat(db: Session, cat_id: int):
    return db.query(models.SpyCat).filter(models.SpyCat.id == cat_id).first()

def get_spy_cats(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.SpyCat).offset(skip).limit(limit).all()

def create_spy_cat(db: Session, cat: schemas.SpyCatCreate):
    if not validate_breed(cat.breed):
        return None
    db_cat = models.SpyCat(
        name=cat.name,
        years_of_experience=cat.years_of_experience,
        breed=cat.breed,
        salary=cat.salary,
    )
    db.add(db_cat)
    db.commit()
    db.refresh(db_cat)
    return db_cat

def update_spy_cat_salary(db: Session, cat_id: int, salary: float):
    cat = get_spy_cat(db, cat_id)
    if not cat:
        return None
    cat.salary = salary
    db.commit()
    db.refresh(cat)
    return cat

def delete_spy_cat(db: Session, cat_id: int):
    cat = get_spy_cat(db, cat_id)
    if not cat:
        return False
    # Check if cat has assigned mission
    if cat.mission:
        return False
    db.delete(cat)
    db.commit()
    return True

# Missions
def get_mission(db: Session, mission_id: int):
    return db.query(models.Mission).filter(models.Mission.id == mission_id).first()

def get_missions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Mission).offset(skip).limit(limit).all()

def create_mission(db: Session, mission: schemas.MissionCreate):
    db_mission = models.Mission(completed=False)
    # Assign cat if provided and if cat is available (no mission assigned)
    if mission.cat_id:
        cat = get_spy_cat(db, mission.cat_id)
        if not cat or cat.mission:
            return None
        db_mission.cat_id = mission.cat_id

    for target in mission.targets:
        db_target = models.Target(
            name=target.name,
            country=target.country,
            notes=target.notes or "",
            completed=target.completed,
        )
        db_mission.targets.append(db_target)
    db.add(db_mission)
    db.commit()
    db.refresh(db_mission)
    return db_mission

def delete_mission(db: Session, mission_id: int):
    mission = get_mission(db, mission_id)
    if not mission:
        return False
    if mission.cat_id:
        return False  # Cannot delete mission assigned to a cat
    db.delete(mission)
    db.commit()
    return True

def update_target_notes(db: Session, target_id: int, notes: str):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        return None
    if target.completed or target.mission.completed:
        return None
    target.notes = notes
    db.commit()
    db.refresh(target)
    return target

def mark_target_completed(db: Session, target_id: int):
    target = db.query(models.Target).filter(models.Target.id == target_id).first()
    if not target:
        return None
    target.completed = True
    db.commit()
    # Check if all targets are completed, then mark mission completed
    mission = target.mission
    if all(t.completed for t in mission.targets):
        mission.completed = True
        db.commit()
    db.refresh(target)
    return target

def assign_cat_to_mission(db: Session, mission_id: int, cat_id: int):
    mission = get_mission(db, mission_id)
    cat = get_spy_cat(db, cat_id)
    if not mission or not cat or cat.mission:
        return None
    mission.cat_id = cat_id
    db.commit()
    db.refresh(mission)
    return mission
