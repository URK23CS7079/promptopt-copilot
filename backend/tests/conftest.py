import pytest
from app.models.database import SessionLocal, engine
from app.models.schemas import PromptCreate
from app.core.llama_integration import LocalLLM
import os

@pytest.fixture(scope="module")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SessionLocal() as session:
        yield session
    await engine.dispose()

@pytest.fixture
def sample_prompt_data():
    return PromptCreate(
        content="Test prompt",
        parameters={"temperature": 0.7}
    )

@pytest.fixture(scope="module")
def llm_fixture():
    return LocalLLM(
        model_path=os.getenv("MODEL_PATH", "models/phi-3-mini.Q4_K_M.gguf")
    )