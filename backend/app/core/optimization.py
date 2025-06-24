#backend/app/core/optimization.py
from typing import List
from .generation import llm_generate
from .evaluation import PromptEvaluator
import random
from typing import List, Callable


def optimize_prompt(seed_prompt: str, k: int = 5,
    gen_type: str = "hybrid",**params) -> str:
   
    # 1. Generate variants using existing method
    variants = generate_k_prompts(
        seed_prompt=seed_prompt,
        k=k,
        gen_type=gen_type,
        **params
    )
    # 2. Get outputs for evaluation
    # print("=" * 40)
    # print("From optimize_prompt")
    # print(f"Generated {len(variants)} variants for optimization:")
    # outputs = [llm_generate(v) for v in variants]
    # print("Outputs generated for evaluation:")
    # for i, output in enumerate(outputs):
    #     print(f"Variant {i+1}: {output}")

    #3. Prompt-Focused Evaluation
    evaluator = PromptEvaluator()
    scores = evaluator.evaluate_outputs(variants, seed_prompt)


    # 3. Output-Focused Evaluation
    # evaluator = PromptEvaluator()
    # print("variants and their outputs:")
    # print(list(zip(variants, outputs)))
    # scores = evaluator.evaluate_outputs(list(zip(variants, outputs)),seed_prompt)
    print(f"Scores for variants: {scores}")
    # Return variant with highest (clarity+completeness+accuracy+usefulness)/40 score
    return max(scores.items(), key=lambda x: x[1])[0]


def generate_k_prompts(seed_prompt: str, k: int, gen_type: str, **params):
    variants = []
    if not seed_prompt.strip():
        raise ValueError("Seed prompt cannot be empty")
    
    if gen_type == "llm-generated":
        variants=_llm_generated_variants(seed_prompt, k, params)
        return variants
    elif gen_type == "rule-based":
        variants = _rule_based_variants(seed_prompt, k)
        return variants
    elif gen_type == "hybrid" or k > 5:
        rule_based = _rule_based_variants(seed_prompt, k//2)
        llm_based = _llm_generated_variants(seed_prompt, k - len(rule_based), params)
        variants = rule_based + llm_based
        return variants
    else:
        raise ValueError(f"Unknown gen_type: {gen_type}")

def _rule_based_variants(seed_prompt: str, k: int) -> List[str]:
    """Generate prompt variants by combining mutations and modifiers."""

    # ✏️ Structural rewrites of the seed prompt
    mutations: List[Callable[[str], str]] = [
        lambda s: f"Explain {s} in simple terms",
        lambda s: f"What is {s}? Describe concisely",
        lambda s: f"Analyze {s} with examples",
        lambda s: f"Compare {s} to similar concepts",
        lambda s: f"List 3 key points about {s}",
        lambda s: f"Rewrite this clearly: {s}",
        lambda s: s.replace(" ", "_").upper(),
        lambda s: s + " (detailed technical explanation)",
    ]

    # 📋 Modifiers to add more instruction
    modifiers: List[str] = [
        "Provide step-by-step reasoning",
        "Include 2-3 examples",
        "Use formal academic tone",
        "Be extremely concise",
        "Add 'Think carefully before answering'",
        "Specify target audience: beginners",
        "Specify target audience: experts",
        "Add 'Verify your facts'",
        "Use bullet points",
        "Include a checklist"
    ]

    k = min(k, len(mutations), len(modifiers))

    selected_mutations = random.sample(mutations, k)
    selected_modifiers = random.sample(modifiers, k)
    variants = []
    for mutate_fn, modifier in zip(selected_mutations, selected_modifiers):
        base = mutate_fn(seed_prompt)

        if base.endswith(('.', '!', '?')):
            full = f"{base} {modifier}"
        else:
            full = f"{base}. {modifier}"

        variants.append(full)
    return variants or [seed_prompt]

def _llm_generated_variants(seed_prompt: str, k: int, params: dict) -> List[str]:
    """Use local LLM to generate improved prompts"""
    prompt = f"""You are a prompt engineer. Given this prompt, improve it in {k} different ways.
Make each version clearer, more precise, or more helpful.
Original Prompt: "{seed_prompt}"
List the {k} improved prompts below, numbered 1 to {k}.""" 
    response = llm_generate(prompt, sysprompt="You are an expert prompt engineer with deep knowledge of effective prompting techniques. Your task is to improve prompts to make them clearer, more specific, and more likely to yield high-quality responses from AI systems.", **params) 
    # Parse numbered list from LLM response
    variants = []
    for line in response.split('\n'):
        if line.strip() and line[0].isdigit():
            variant = line.split('.', 1)[1].strip()
            variants.append(variant)
            if len(variants) >= k:
                break
    print("=" * 40)
    print("LLM Generated Variants:")
    print(variants)
    print("=" * 40)
    return variants or [seed_prompt]  # Fallback if parsing fails