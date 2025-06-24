# backend/tests/test_db.py (new)
import pytest
from app.models.database import SessionLocal
from app.models.schemas import PromptCreate

@pytest.mark.asyncio
async def test_db_connection():
    async with SessionLocal() as session:
        test_prompt = PromptCreate(content="Test", parameters={})
        session.add(test_prompt)
        await session.commit()
        assert test_prompt.id is not None