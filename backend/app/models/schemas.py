from pydantic import BaseModel
from typing import List, Dict, Optional
from datetime import datetime

class PromptBase(BaseModel):
    content: str
    parameters: Optional[Dict] = None

class PromptCreate(PromptBase):
    pass

class PromptVariant(PromptBase):
    id: int
    created_at: datetime
    parent_id: Optional[int] = None
    generation_method: str

    class Config:
        from_attributes = True

class EvaluationResult(BaseModel):
    prompt_id: int
    metrics: Dict[str, float]
    test_data_hash: str
    created_at: datetime

class OptimizationRequest(BaseModel):
    base_prompt: str
    dataset: List[Dict]
    optimization_method: str = "bootstrap"

class OptimizationResult(BaseModel):
    optimized_prompt: str
    metrics: Dict[str, float]
    best_variant: str
    improvement: float