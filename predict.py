import os
import re
import string
from transformers import pipeline
from datasets import ClassLabel
import os
from pathlib import Path
from utils import clean_text

c2l = ClassLabel(names=[
                     "INTJ", "INTP", "ENTJ", "ENTP", 
                     "INFJ", "INFP", "ENFJ", "ENFP",
                     "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                     "ISTP", "ISFP", "ESTP", "ESFP"])

classificator = pipeline("text-classification", model="./model", tokenizer="distilbert-base-uncased", framework="pt", top_k=16)

# base data path. You should place directories containing textes to be predicted.
dataset_path = "../BERT/data/tests_test.txt"

def collect_entries_for(directory_name: str):
    return [os.path.join(dirname, filename) \
            for dirname, _, filenames in os.walk(dataset_path + directory_name) \
             for filename in filenames]


def predict_for_texts(texts, verbose = False):
    # predict
    predictions = {}
    result = classificator(texts, padding=True)
    top_results = [(c2l.int2str(int(res['label'].removeprefix("LABEL_"))), res['score']) for res in result[0]]
    for label, score in top_results:
        if label not in predictions:
            predictions[label] = 0
        predictions[label] += score
    sorted_tuple = sorted(predictions.items(), key=lambda item: item[1], reverse=True)[0]
    return sorted_tuple[0]

