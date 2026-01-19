import os
import time
import threading
from dotenv import load_dotenv

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

try:
    import torch_directml
except Exception:
    torch_directml = None

load_dotenv()

MODEL_ID = os.getenv("LOCAL_MODEL_ID", "Qwen/Qwen2.5-1.5B-Instruct")
LOCAL_DEVICE = os.getenv("LOCAL_DEVICE", "cpu").lower().strip()  # cpu | dml

MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "128"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))

DO_SAMPLE_RAW = os.getenv("DO_SAMPLE", "false").lower().strip()
DO_SAMPLE = DO_SAMPLE_RAW in ("1", "true", "yes", "y")

_infer_lock = threading.Lock()

def get_device():
    if LOCAL_DEVICE == "cpu":
        return "cpu"
    if LOCAL_DEVICE == "dml" and torch_directml is not None:
        return torch_directml.device()
    return "cpu"

DEVICE = get_device()

print("========================================")
print(f"✅ Loading model: {MODEL_ID}")
print(f"✅ Target device: {DEVICE}")
print("========================================")

tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

# ✅ 일단 CPU로만 로딩 (안전)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float32
)
model.eval()

# ✅ 현재 모델 device 상태 추적
_current_device = "cpu"

def _ensure_device(target):
    """
    target: "cpu" or DirectML device object
    """
    global _current_device

    # 이미 cpu면 패스
    if target == "cpu" and _current_device == "cpu":
        return

    # DirectML로 올리기 시도
    if target != "cpu" and _current_device != "dml":
        model.to(target)
        _current_device = "dml"
        return

    # CPU로 내리기
    if target == "cpu" and _current_device != "cpu":
        model.to("cpu")
        _current_device = "cpu"


def ask_hf(q: str) -> dict:
    start = time.perf_counter()

    messages = [
        {"role": "system", "content": "You are a helpful assistant. Answer concisely in Korean."},
        {"role": "user", "content": q},
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(prompt, return_tensors="pt")

    used_device = "cpu" if DEVICE == "cpu" else "dml"

    try:
        with _infer_lock:
            _ensure_device(DEVICE)

            if DEVICE == "cpu":
                inputs = {k: v.to("cpu") for k, v in inputs.items()}
            else:
                inputs = {k: v.to(DEVICE) for k, v in inputs.items()}

            with torch.no_grad():
                output_ids = model.generate(
                    **inputs,
                    max_new_tokens=MAX_NEW_TOKENS,
                    do_sample=DO_SAMPLE,
                    temperature=TEMPERATURE,
                )

    except Exception as e:
        # ✅ GPU에서 터지면 CPU로 fallback
        used_device = "cpu"
        with _infer_lock:
            _ensure_device("cpu")
            inputs = {k: v.to("cpu") for k, v in inputs.items()}

            with torch.no_grad():
                output_ids = model.generate(
                    **inputs,
                    max_new_tokens=MAX_NEW_TOKENS,
                    do_sample=DO_SAMPLE,
                    temperature=TEMPERATURE,
                )

    text = tokenizer.decode(output_ids[0], skip_special_tokens=True)

    if q in text:
        answer = text.split(q, 1)[-1].strip()
    else:
        answer = text.strip()

    elapsed_ms = int((time.perf_counter() - start) * 1000)

    return {
        "answer": answer,
        "elapsed_ms": elapsed_ms,
        "device": used_device,
        "model": MODEL_ID,
    }
