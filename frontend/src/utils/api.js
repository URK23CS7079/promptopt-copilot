const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export const fetchModels = async () => {
  const response = await fetch(`${API_BASE_URL}/models/available`);
  if (!response.ok) {
    throw new Error('Failed to fetch models');
  }
  return response.json();
};

export const generateVariants = async (basePrompt, numVariants = 5) => {
  const response = await fetch(`${API_BASE_URL}/prompts/generate-variants`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content: basePrompt,
      num_variants: numVariants,
    }),
  });
  if (!response.ok) {
    throw new Error('Failed to generate variants');
  }
  return response.json();
};

export const evaluatePrompts = async (variants, testData) => {
  const formData = new FormData();
  formData.append('test_data', testData);
  formData.append('variants', JSON.stringify(variants));
  
  const response = await fetch(`${API_BASE_URL}/prompts/evaluate`, {
    method: 'POST',
    body: formData,
  });
  if (!response.ok) {
    throw new Error('Failed to evaluate prompts');
  }
  return response.json();
};