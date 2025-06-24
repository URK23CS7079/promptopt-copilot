import dspy
from dspy.teleprompt import BootstrapFewShot, BayesianOptimizer
from dspy.evaluate import Evaluate
from typing import List, Dict, Any
import numpy as np

class PromptOptimizer:
    def __init__(self, llm=None):
        self.llm = llm or dspy.HFClientLocal(model="phi-3-mini")
        dspy.configure(lm=self.llm)
        
        self.optimizers = {
            'bootstrap': BootstrapFewShot(
                metric=self.evaluate_prompt,
                max_bootstrapped_demos=4,
                max_rounds=3
            ),
            'bayesian': BayesianOptimizer(
                metric=self.evaluate_prompt,
                num_threads=4,
                num_candidates=8
            )
        }
        self.evaluator = Evaluate(
            metric=self.evaluate_prompt,
            num_threads=4
        )

    def evaluate_prompt(self, example, pred, trace=None):
        """Unified evaluation function for all optimizers"""
        scores = {
            'exact_match': float(example.expected.lower() in pred.output.lower()),
            'latency': trace['latency'] if trace else 0.0
        }
        return np.mean(list(scores.values())) # Combined score

    def optimize(self, dataset, optimizer_type='bootstrap'):
        """Consistent optimization interface"""
        class PromptSignature(dspy.Signature):
            """Instruction: {instruction}
            Input: {input}
            Output: {output}"""
            instruction = dspy.InputField()
            input = dspy.InputField()
            output = dspy.OutputField()

        class PromptModule(dspy.Module):
            def __init__(self):
                super().__init__()
                self.generate = dspy.Predict(PromptSignature)
            
            def forward(self, instruction, input):
                return self.generate(instruction=instruction, input=input)

        # Validation
        if optimizer_type not in self.optimizers:
            raise ValueError(f"Optimizer {optimizer_type} not supported. Choose from: {list(self.optimizers.keys())}")

        # Optimization
        compiled_prompt = self.optimizers[optimizer_type].compile(
            PromptModule(),
            trainset=dataset
        )
        
        # Evaluation
        eval_results = self.evaluator(compiled_prompt, dataset)
        
        return {
            'compiled_prompt': compiled_prompt,
            'evaluation': eval_results,
            'best_variant': str(compiled_prompt)
        }