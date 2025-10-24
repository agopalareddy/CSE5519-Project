from transformers import pipeline

pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")

messages = [
     {
         "role": "user",
         "content": [
             {"type": "text", "text": "What is 5 times 5?"},
         ],
     }
 ]

outputs = pipe(text=messages)

result = outputs[0]["generated_text"]

print(result)