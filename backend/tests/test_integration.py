import pytest
from app.core.optimization import OptimizationEngine
from app.models.schemas import OptimizationRequest

@pytest.fixture
def engine():
    return OptimizationEngine()

@pytest.fixture
def sample_dataset():
    return [
        {"input": "2+2", "output": "4"},
        {"input": "3*3", "output": "9"},
        {"input": "10-5", "output": "5"}
    ]

@pytest.mark.asyncio
async def test_full_optimization(engine, sample_dataset):
    result = engine.run_optimization(
        base_prompt="Calculate the math problem",
        dataset=sample_dataset
    )
    
    assert 'optimized_prompt' in result
    assert isinstance(result['metrics']['accuracy'], float)
    assert len(result['variants']) == 5
    
    print(f"Optimization Results:\n"
          f"Base Prompt: {result['base_prompt']}\n"
          f"Optimized: {result['optimized_prompt']}\n"
          f"Accuracy: {result['metrics']['accuracy']:.2f}")