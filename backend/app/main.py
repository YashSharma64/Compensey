import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import compare, strategy

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="CompenseyAI API", version="1.0.0")
logger.info("[startup] CompenseyAI Backend starting")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(compare.router)
app.include_router(strategy.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to CompenseyAI Backend"}
