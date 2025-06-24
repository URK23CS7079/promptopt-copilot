#backend/app/core/evaluation.py
from typing import List, Dict
import re
import logging
from .generation import llm_generate

class PromptEvaluator:
    def __init__(self):
        # Short system prompt – leave the real instruction in the user prompt
        self.judge_sysprompt = "You are a helpful and strict AI prompt grader."

    def evaluate_outputs(self, variants: List[str], seed_prompt: str) -> Dict[int, float]:
        """
        Evaluates prompt variants based only on how well they preserve the meaning of the seed prompt.

        Args:
            variants: list of improved prompt variants
            seed_prompt: original user prompt

        Returns:
            Dict of scores {1: 0.9, 2: 0.7, ...} normalized to 0–1 scale
        """
        print("=" * 100)
        print("Evaluating Variants Against Seed Prompt:", seed_prompt)

        variant_text = "\n".join([f"{i+1}. {variant}" for i, variant in enumerate(variants)])
        expected_format = "\n".join([f"Variant {i+1}:\nScore: X/10" for i in range(len(variants))])

        prompt = f"""You are a strict AI prompt grader.

Score each rewritten prompt based ONLY on how well it preserves the meaning and intent of the original prompt.
Do NOT reward extra context or added complexity. Simpler is better.

Examples:
❌ "Explain the steps and importance of Photosynthesis." → Adds "steps" and "importance" → Not same intent → Score: 5/10  
✅ "Briefly define Photosynthesis." → Rephrases clearly → Same intent → Score: 10/10

Seed Prompt:
"{seed_prompt}"

Variants:
{variant_text}

Give a score for each variant from 1 (very different) to 10 (identical), using this format exactly:

{expected_format}

Do NOT explain the score. Do NOT output anything else.
"""

        try:
            response = llm_generate(
                prompt=prompt,
                sysprompt=self.judge_sysprompt,
                temperature=0.0,
                max_tokens=256
            )
            print("LLM Judge Raw Response:\n", response)
            return self._parse_response(response, len(variants))
        except Exception as e:
            logging.error(f"Evaluation failed: {str(e)}")
            return {i + 1: 0.5 for i in range(len(variants))}  # fallback if failed

    def _parse_response(self, response: str, num_variants: int) -> Dict[int, float]:
        """
        Extracts scores like 'Score: X/10' and returns a normalized dict {i: score}
        """
        scores = {}
        for i in range(1, num_variants + 1):
            match = re.search(rf"Variant {i}:\s*Score:\s*(\d+)/10", response)
            if match:
                score = int(match.group(1))
                scores[i] = score / 10.0
            else:
                scores[i] = 0.5  # fallback score if not matched
        return scores