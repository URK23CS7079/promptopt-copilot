import pytest
from app.core.evaluation import evaluate_variants
from app.models.schemas import PromptVariant
import pandas as pd
from pathlib import Path

def test_evaluation_metrics(tmp_path):
    # Create test CSV
    test_file = tmp_path / "test.csv"
    test_file.write_text("input,output\nhello,world\nfoo,bar")
    
    variants = [
        PromptVariant(
            id=1,
            content="Test prompt",
            parameters={}
        )
    ]
    
    results = evaluate_variants(variants, str(test_file))
    
    assert len(results) == 1
    assert "exact_match" in results[0].metrics

def test_file_loading(tmp_path):
    # Test JSON loading
    json_file = tmp_path / "test.json"
    json_file.write_text('[{"input":"test","output":"result"}]')
    
    data = load_test_data(str(json_file))
    assert isinstance(data, pd.DataFrame)
    assert data.shape[0] == 1