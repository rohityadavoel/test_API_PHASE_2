from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, consultations

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic

app = FastAPI(title="Consultation API", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(consultations.router, prefix="/consultations", tags=["consultations"])
