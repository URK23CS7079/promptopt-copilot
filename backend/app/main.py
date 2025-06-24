from fastapi import FastAPI
from .api import endpoints

app = FastAPI(
    title="PromptOpt Co-Pilot",
    description="Prompt optimization assistant for local development",
    version="1.0.0"
)
app.include_router(endpoints.router)

@app.get("/")
async def root():
    return {"message": "PromptOpt Co-Pilot API"}