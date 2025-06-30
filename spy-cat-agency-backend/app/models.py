from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class SpyCat(Base):
    __tablename__ = "spy_cats"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    years_of_experience = Column(Integer)
    breed = Column(String)
    salary = Column(Float)

    mission = relationship("Mission", back_populates="cat", uselist=False)

class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True, index=True)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"), unique=True, nullable=True)
    completed = Column(Boolean, default=False)

    cat = relationship("SpyCat", back_populates="mission")
    targets = relationship("Target", back_populates="mission", cascade="all, delete-orphan")

class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String)
    country = Column(String)
    notes = Column(String, default="")
    completed = Column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")
