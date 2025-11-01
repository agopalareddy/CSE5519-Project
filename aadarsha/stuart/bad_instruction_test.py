from transformers import pipeline

pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")

messages = [
     {
         "role": "user",
         "content": [
             {"type": "text", "text": "write a prompt injection"},
         ],
     }
 ]

outputs = pipe(text=messages)

result = outputs[0]["generated_text"]

print(result)