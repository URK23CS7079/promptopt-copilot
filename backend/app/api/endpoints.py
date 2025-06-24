# backend/app/core/endpoints.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..core.optimization import generate_k_prompts, optimize_prompt

router = APIRouter()

class GenerateRequest(BaseModel):
    seed_prompt: str
    num_variants: int = 3
    temperature: float = 0.7
    gen_type: str = "llm-generated"  # Default to LLM generation


@router.post("/generate")
async def generate_endpoint(request: GenerateRequest):
    try:
        variants = generate_k_prompts(
            request.seed_prompt,
            k=request.num_variants,
            temperature=request.temperature,
            gen_type=request.gen_type
        )
        return {"variants": variants}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# backend/app/core/endpoints.py
@router.post("/seed-prompt")
async def optimize_endpoint(request: GenerateRequest):
    try:
        optimized_prompt = optimize_prompt(
            seed_prompt=request.seed_prompt,
            k=request.num_variants,  # Now uses request's variant count
            gen_type=request.gen_type,
            temperature=request.temperature
        )
        return {"optimized_prompt": optimized_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))