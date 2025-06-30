from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cats, missions
from app.database import engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuração CORS
origins = [
    "http://localhost:3000",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo rotas
app.include_router(cats.router, prefix="/cats", tags=["Cats"])
app.include_router(missions.router, prefix="/missions", tags=["Missions"])
