from transformers import pipeline
import torch

device = 0 if torch.cuda.is_available() else -1  # 0 = first GPU, -1 = CPU
pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it", device=device)

print(pipe.device)
