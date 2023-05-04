import os
import pickle
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from keras.utils import pad_sequences
from keras.models import load_model


MODELS_DIR = "models"

DIMENSIONS = ["IE", "NS", "FT", "PJ"]
MAX_POST_LENGTH = 40

def predict_rnn(text):
    final = ""

    lemmatizer = WordNetLemmatizer()
    stop_words = stopwords.words("english")

    def lemmatize(x):
        temp = []
        x = x.lower()
        x = " ".join(
            [
                lemmatizer.lemmatize(word)
                for word in x.split(" ")
                if (word not in stop_words)
            ]
        )
        temp.append(x)
        return np.array(temp)

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

        predictions = model.predict(preprocess(text))
        prediction = float(sum(predictions) / len(predictions))
        print(DIMENSIONS[k])
        print(prediction)
        if prediction >= 0.5:
            final += DIMENSIONS[k][1]
        else:
            final += DIMENSIONS[k][0]

    return final