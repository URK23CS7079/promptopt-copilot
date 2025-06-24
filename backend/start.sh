#!/bin/bash

# Download model if missing
MODEL_FILE="models/phi-3-mini.Q4_K_M.gguf"
if [ ! -f "$MODEL_FILE" ]; then
    echo "Downloading model..."
    wget https://huggingface.co/MoMonir/Phi-3-mini-128k-instruct-GGUF/resolve/main/phi-3-mini-128k-instruct.Q4_K_M.gguf?download=true \
         -O $MODEL_FILE
fi

# Start service with model path
export LOCAL_LLM_PATH=$MODEL_FILE
uvicorn app.main:app --host 0.0.0.0 --port 8000