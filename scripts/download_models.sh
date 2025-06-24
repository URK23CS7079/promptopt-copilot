#!/bin/bash

MODELS_DIR="../models"
PHI3_MODEL="phi-3-mini.Q4_K_M.gguf"
MODEL_URL="https://huggingface.co/TheBloke/phi-3-mini-GGUF/resolve/main/phi-3-mini.Q4_K_M.gguf"

mkdir -p "$MODELS_DIR"

if [ ! -f "$MODELS_DIR/$PHI3_MODEL" ]; then
    echo "Downloading $PHI3_MODEL..."
    wget "$MODEL_URL" -O "$MODELS_DIR/$PHI3_MODEL"
else
    echo "$PHI3_MODEL already exists. Skipping download."
fi

echo "Model setup complete."