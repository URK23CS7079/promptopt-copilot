# backend/app/core/generation.py
from .llama_integration import LlamaModelConnector

_LLM = None

def get_llm():
    """Lazy-load singleton LLM instance"""
    global _LLM
    if _LLM is None:
        _LLM = LlamaModelConnector().get_model()
    return _LLM

def llm_generate(prompt: str,sysprompt: str = "Your are helpfull AI assistent",  **params) -> str:
    """
    Central generation function for all components
    Default params match phi-3-mini's recommended settings
    """
    default_params = {
        'temperature': 0.7,
        'top_p': 0.9,
        'max_tokens': 256
        # 'echo': False
    }
    merged_params = {**default_params, **params}
    print("=" * 40)
    print("LLM Generation Request from app/core/generation.py")
    print("=" * 40)
    print(f"Prompt: {prompt}")
    print(f"System prompt: {sysprompt}")
    print(f"Generating with params: {merged_params}")
    result = get_llm().create_chat_completion(
        messages =[
            {"role": "system", "content": sysprompt},
            {"role": "user", "content": prompt}],
        **merged_params
    )
    print("Responce:",result["choices"][0]["message"]["content"].strip())
    print("=" * 40)
    return result["choices"][0]["message"]["content"].strip()

if __name__ == "__main__":
    # Example usage
    try:
        response = llm_generate(prompt="What is capial of frence",sysprompt="Wrong answers only!", temperature=0.5)
        print("Generated response:", response)
    except Exception as e:
        print(f"Error during generation: {e}")