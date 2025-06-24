# backend/tests/test_llama.py (new)
from pathlib import Path
import pytest
from app.core.llama_integration import LocalLLM

@pytest.fixture
def llm():
    project_root = Path(__file__).parent.parent.parent.parent
    default_path = project_root / "models" / "phi-3-mini.Q4_K_M.gguf"
    default_path = default_path.absolute().resolve()
    return LocalLLM(default_path)

def test_llm_initialization(llm):
    assert llm.llm is not None

def test_prompt_evaluation(llm):
    results = llm.evaluate_prompt("Explain AI", [{"input": "What is AI?", "output": "Artificial Intelligence"}])
    assert len(results) > 0