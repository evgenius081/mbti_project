import os
import pickle
import numpy as np
from pathlib import Path
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from keras.utils import pad_sequences
from keras.models import load_model


MODELS_DIR = "models"
DATA_DIR = "../data"
DATASET_DIR = str(Path.home()) + '\\Downloads\\dataset\\'
STANBAR_ARTICLES_PATH = os.path.join(DATASET_DIR, "sivers")

DIMENSIONS = ["IE", "NS", "FT", "PJ"]
MODEL_BATCH_SIZE = 128
TOP_WORDS = 2500
MAX_POST_LENGTH = 40
EMBEDDING_VECTOR_LENGTH = 20


# base dataset path. You should place directories containing textes to be predicted.
dataset_path = str(Path.home()) + '\\Downloads\\dataset\\'

def collect_entries_for(directory_name: str):
    return [os.path.join(dirname, filename) \
            for dirname, _, filenames in os.walk(dataset_path + directory_name) \
                for filename in filenames if filename != '.DS_Store']


# journals_texts = collect_entries_for('journals')

# stanbar_texts = collect_entries_for('stanbar')

# Derek Sivers's texts, he has a lot of texts and is known as INTJ
# sivers_texts = collect_entries_for('sivers')

# Tim Ferris's texts, he has a lot of texts and is known as INTJ
# ferris_texts = collect_entries_for('ferriss')

# Oprah's texts, he has a lot of texts and is known as ENFJ
# oprah_texts = collect_entries_for('oprah')
names = ['thatcher', 'kant', 'weekend']

thatcher_texts = collect_entries_for(names[0])

kant = collect_entries_for(names[1])

weekend = collect_entries_for(names[2])

for idx, person_texts in enumerate([thatcher_texts, kant, weekend]):
    final = ""
    x_test = []

    for file in person_texts:
        print(file)
        lines = [line for line in [line.strip() for line in open(file, encoding='utf-8').readlines()] if line]
        x_test.extend(lines)

    print(f"Number of lines in dir {person_texts} is {len(x_test)}")

    types = [
        "INFJ",
        "ENTP",
        "INTP",
        "INTJ",
        "ENTJ",
        "ENFJ",
        "INFP",
        "ENFP",
        "ISFP",
        "ISTP",
        "ISFJ",
        "ISTJ",
        "ESTP",
        "ESFP",
        "ESTJ",
        "ESFJ",
    ]
    types = [x.lower() for x in types]
    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words("english")


    def lemmatize(x):
        lemmatized = []
        for post in x:
            temp = post.lower()
            for type_ in types:
                temp = temp.replace(" " + type_, "")
            temp = " ".join(
                [
                    lemmatizer.lemmatize(word)
                    for word in temp.split(" ")
                    if (word not in stop_words)
                ]
            )
            lemmatized.append(temp)
        return np.array(lemmatized)


    for k in range(len(DIMENSIONS)):
        model = load_model(
            os.path.join(MODELS_DIR, "rnn_model_{}.h5".format(DIMENSIONS[k]))
        )
        tokenizer = None
        with open(
            os.path.join(MODELS_DIR, "rnn_tokenizer_{}.pkl".format(DIMENSIONS[k])), "rb"
        ) as f:
            tokenizer = pickle.load(f)

        def preprocess(x):
            lemmatized = lemmatize(x)
            tokenized = tokenizer.texts_to_sequences(lemmatized)
            return pad_sequences(tokenized, maxlen=MAX_POST_LENGTH)

        predictions = model.predict(preprocess(x_test))
        prediction = float(sum(predictions) / len(predictions))
        # print(DIMENSIONS[k])
        # print(prediction)
        if prediction >= 0.5:
            final += DIMENSIONS[k][1]
        else:
            final += DIMENSIONS[k][0]

    # print("")
    # print("Final prediction: {}".format(final) + " for " + names[idx])
