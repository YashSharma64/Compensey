from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import compare

app = FastAPI(title="CompenseyAI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(compare.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CompenseyAI Backend"}
