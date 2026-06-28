# app/main.py

from fastapi import FastAPI
from app.api import weapons

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Granblue Fastest-Comp Finder API is running"}

app.include_router(weapons.router, prefix="/weapons", tags=["weapons"])