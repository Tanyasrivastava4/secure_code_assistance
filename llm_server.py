# server/llm_server.py
"""
Secure Code Assistant - LLM Server
Loads CodeLLaMA-7B directly from HuggingFace and serves code generation via FastAPI.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# ------------------------
# Configurations
# ------------------------
HF_MODEL_NAME = "codellama/CodeLLaMA-7B-hf"  # HuggingFace model name
MAX_TOKENS = 1024
USE_FP16 = True
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# If your model is gated, set your HF token here (or set as environment variable)
HF_TOKEN = os.getenv("HF_TOKEN")  # safer to store token in env variable

# ------------------------
# Request Body Schema
# ------------------------
class GenerateRequest(BaseModel):
    prompt: str
    language: str = "python"

# ------------------------
# Initialize FastAPI
# ------------------------
app = FastAPI(title="Secure Code Assistant LLM Server")

# ------------------------
# Load Tokenizer and Model
# ------------------------
print(f"[INFO] Loading tokenizer and model from HuggingFace: {HF_MODEL_NAME} ...")
try:
    tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_NAME, token=HF_TOKEN)
    model = AutoModelForCausalLM.from_pretrained(
        HF_MODEL_NAME,
        torch_dtype=torch.float16 if USE_FP16 and DEVICE == "cuda" else torch.float32,
        token=HF_TOKEN
    )
    model.to(DEVICE)
    print(f"[INFO] Model loaded on {DEVICE}.")
except Exception as e:
    print(f"[ERROR] Failed to load model: {e}")
    raise e

# ------------------------
# API Endpoint: Generate Code
# ------------------------
@app.post("/generate")
def generate_code(req: GenerateRequest):
    """
    Generate secure code based on the prompt and language.
    """
    try:
        input_ids = tokenizer(req.prompt, return_tensors="pt").input_ids.to(DEVICE)
        outputs = model.generate(
            input_ids,
            max_new_tokens=MAX_TOKENS,
            do_sample=True,
            temperature=0.2
        )
        code = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return {"code": code}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation failed: {e}")

# ------------------------
# API Endpoint: Health Check
# ------------------------
@app.get("/health")
def health():
    """
    Simple health check endpoint to verify the server is running.
    """
    return {"status": "ok", "device": DEVICE, "model": HF_MODEL_NAME}

# ------------------------
# Run Server
# ------------------------
if __name__ == "__main__":
    import uvicorn
    # Bind to IPv6 (::) instead of IPv4 (0.0.0.0)
    uvicorn.run("server.llm_server:app", host="::", port=8000, reload=True)
