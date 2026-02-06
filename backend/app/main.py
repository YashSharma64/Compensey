from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import compare

app = FastAPI(
    title="CompenseyAI API",
    description="Backend for CompenseyAI - Competitor Intelligence Tool",
    version="1.0.0"
)

# CORS Configuration
origins = [
    "http://localhost:5173",  # Vite default
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(compare.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CompenseyAI Backend"}
