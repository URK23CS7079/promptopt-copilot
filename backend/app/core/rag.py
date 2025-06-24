from typing import List, Dict
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from pathlib import Path

class RAGValidator:
    def __init__(self, data_dir: str = "data/rag"):
        self.data_dir = Path(data_dir)
        self.index = None
        
    def build_index(self):
        documents = SimpleDirectoryReader(self.data_dir).load_data()
        self.index = VectorStoreIndex.from_documents(documents)
        return self.index
    
    def validate_prompt(self, prompt: str, top_k: int = 3) -> List[Dict]:
        if not self.index:
            self.build_index()
            
        query_engine = self.index.as_query_engine(similarity_top_k=top_k)
        response = query_engine.query(
            f"Validate if this prompt follows RAG best practices: {prompt}"
        )
        
        return [
            {"node": node.node, "score": node.score}
            for node in response.source_nodes
        ]
    
    def generate_rag_hints(self, prompt: str) -> Dict:
        validation = self.validate_prompt(prompt)
        hints = {
            "needs_context": False,
            "suggested_chunks": []
        }
        
        if any("retrieval" in node.node.text.lower() for node in validation):
            hints["needs_context"] = True
            hints["suggested_chunks"] = [
                node.node.text[:200] + "..." 
                for node in validation[:2]
            ]
            
        return hints