from transformers import pipeline
from datasets import ClassLabel

c2l = ClassLabel(names=[
                     "INTJ", "INTP", "ENTJ", "ENTP", 
                     "INFJ", "INFP", "ENFJ", "ENFP",
                     "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                     "ISTP", "ISFP", "ESTP", "ESFP"])

classificator = pipeline("text-classification", model="./BERT/model", tokenizer="distilbert-base-uncased", framework="pt",
                         top_k=16)


def predict_for_texts(texts, verbose = False):
    predictions = {}
    batch_size = 512
    batches = [texts[i:i + batch_size] for i in range(0, len(texts), batch_size)]

    for batch in batches:
        result = classificator(batch, padding=True)
        top_results = [(c2l.int2str(int(res['label'].removeprefix("LABEL_"))), res['score']) for res in result[0]]
        for label, score in top_results:
            if label not in predictions:
                predictions[label] = 0
            predictions[label] += score
    sorted_tuple = sorted(predictions.items(), key=lambda item: item[1], reverse=True)[0]
    return sorted_tuple[0]

