from fastapi.testclient import TestClient
from app.main import app
from app.models.schemas import PromptCreate

client = TestClient(app)

def test_generate_variants():
    test_prompt = PromptCreate(
        content="Explain machine learning",
        num_variants=3
    )
    response = client.post(
        "/api/v1/prompts/generate-variants",
        json=test_prompt.dict()
    )
    assert response.status_code == 200
    assert len(response.json()) == 3
    assert all("content" in variant for variant in response.json())

def test_evaluate_prompts(tmp_path):
    test_file = tmp_path / "test_data.csv"
    test_file.write_text("input,output\n2+2,4\n3*3,9")
    
    with open(test_file, "rb") as f:
        response = client.post(
            "/api/v1/prompts/evaluate",
            files={"test_data": f},
            data={"variants": '[{"content":"test"}]'}
        )
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)