from langsmith import Client
from promptlayer import PromptLayer
import os
from typing import Dict, Any

class EvaluationLogger:
    def __init__(self):
        self.langsmith_client = Client()
        self.pl = PromptLayer(api_key=os.getenv('PROMPTLAYER_API_KEY'))
    
    def log_to_langsmith(self, run_id: str, inputs: Dict, outputs: Dict, evaluation: Dict):
        self.langsmith_client.create_feedback(
            run_id,
            key="prompt_metrics",
            score=evaluation.get('score', 0),
            comment=str(evaluation)
        )
    
    def log_to_promptlayer(self, prompt_name: str, prompt_template: str, metadata: Dict[str, Any]):
        return self.pl.prompts.publish(
            prompt_name,
            prompt_template,
            metadata=metadata
        )
    
    def log_evaluation(self, run_data: Dict[str, Any]):
        # Log to both services
        self.log_to_langsmith(**run_data)
        pl_id = self.log_to_promptlayer(
            prompt_name=run_data['prompt_name'],
            prompt_template=run_data['prompt_template'],
            metadata=run_data['metadata']
        )
        return {
            "langsmith_run_id": run_data['run_id'],
            "promptlayer_id": pl_id
        }