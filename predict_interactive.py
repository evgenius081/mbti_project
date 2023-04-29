import os
import transformers
from transformers import pipeline
from datasets import ClassLabel

c2l = ClassLabel(names=[
                     "INTJ", "INTP", "ENTJ", "ENTP", 
                     "INFJ", "INFP", "ENFJ", "ENFP",
                     "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                     "ISTP", "ISFP", "ESTP", "ESFP"])

classificator = pipeline("text-classification", model="./model", tokenizer="distilbert-base-uncased", framework="pt", top_k=16)

while True:
    lines = []
    while True:
        line = input("Enter the text, when done enter EOF: ")
        if line != "EOF":
            lines.append(line)
        else:
            break
    text = '\n'.join(lines)

    # split to batches of 512 tokens
    batch_size = 512
    batches = [text[i:i+batch_size] for i in range(0, len(text), batch_size)]

    # predict
    predictions = {}
    for batch, index in enumerate(batches):
        result = classificator(batch, padding=True)
        top_results = [(c2l.int2str(int(res['label'].removeprefix("LABEL_"))), res['score']) for res in result[0]]
        for label, score in top_results:
            if label not in predictions:
                predictions[label] = 0
            predictions[label] += score

    print(predictions)
