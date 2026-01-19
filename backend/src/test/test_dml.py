import torch
import torch_directml

dml = torch_directml.device()
print("✅ DirectML device:", dml)
print("torch version:", torch.__version__)
