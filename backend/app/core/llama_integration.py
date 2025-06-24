# backend/app/core/llama_integration.py
import os
from pathlib import Path
from typing import Optional
from llama_cpp import Llama

class LlamaModelConnector:
    """Lightweight wrapper for llama.cpp model connection"""
    
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize LLaMA model connector
        
        Args:
            model_path: Optional absolute path to GGUF model.
                      Defaults to project_root/models/phi-3-mini.Q4_K_M.gguf
        """
        # Calculate default path relative to this file's location
        if model_path is None:
            project_root = Path(__file__).parent.parent.parent.parent
            model_path = str(project_root / "models" / "phi-3-mini.Q4_K_M.gguf")
            
        self._validate_model_path(model_path)
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,
            n_threads=max(1, os.cpu_count() - 1),  # Ensure at least 1 thread
            n_gpu_layers=0,
            verbose=False,
            stop= ["<|endoftext|>"]  # Stop at end of text token
        )
    
    def _validate_model_path(self, path: str) -> None:
        """Ensure model exists at specified path"""
        if not os.path.exists(path):
            suggested_path = Path(__file__).parent.parent.parent.parent / "models"
            raise FileNotFoundError(
                f"Model not found at {path}\n"
                f"Please either:\n"
                f"1. Place your GGUF model at: {suggested_path}\n"
                f"2. Or specify the full path when initializing LlamaModelConnector"
            )
    
    def get_model(self) -> Llama:
        """Get the raw Llama instance for direct access"""
        return self.llm
    
    def health_check(self) -> bool:
        """Verify model is responsive"""
        try:
            test_output = self.llm.create_chat_completion(
                messages=[{"role": "system", "content": "ping"}],
                max_tokens=1
            )
            return bool(test_output)
        except Exception:
            return False
        
if __name__ == "__main__":
    # Example usage
    try:
        connector = LlamaModelConnector()
        if connector.health_check():
            print("✅ LLaMA model is ready!")
        else:
            print("❌ LLaMA model health check failed.")
    except Exception as e:
        print(f"Error initializing LLaMA model: {e}")
    model = connector.get_model()
    print(f"LLaMA model loaded successfully: {model.model_path}")
    response = model.create_chat_completion(
        messages=[
            # {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "How are you!"}])
    print("Response:", response["choices"][0]["message"]["content"].strip())