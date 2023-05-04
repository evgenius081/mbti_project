import os.path
import os
import pickle
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from keras.utils import pad_sequences
from keras.models import load_model

MODELS_DIR = "models"

DIMENSIONS = ["IE", "NS", "FT", "PJ"]
MODELS = [load_model(
            os.path.join(MODELS_DIR, "rnn_model_IE.h5")
        ),
    load_model(
        os.path.join(MODELS_DIR, "rnn_model_NS.h5")
    ),
    load_model(
            os.path.join(MODELS_DIR, "rnn_model_FT.h5")
        ),
    load_model(
            os.path.join(MODELS_DIR, "rnn_model_PJ.h5")
        )
]

TOKENIZER = []
with open(
        os.path.join(MODELS_DIR, "rnn_tokenizer_IE.pkl"), "rb"
) as f:
    tok = pickle.load(f)
    TOKENIZER.append(tok)
with open(
        os.path.join(MODELS_DIR, "rnn_tokenizer_NS.pkl"), "rb"
) as f:
    tok = pickle.load(f)
    TOKENIZER.append(tok)
with open(
        os.path.join(MODELS_DIR, "rnn_tokenizer_FT.pkl"), "rb"
) as f:
    tok = pickle.load(f)
    TOKENIZER.append(tok)
with open(
        os.path.join(MODELS_DIR, "rnn_tokenizer_PJ.pkl"), "rb"
) as f:
    tok = pickle.load(f)
    TOKENIZER.append(tok)

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
        # model = load_model(
        #     os.path.join(MODELS_DIR, "rnn_model_{}.h5".format(DIMENSIONS[k]))
        # )
        model = MODELS[k]
        tokenizer = None
        # with open(
        #     os.path.join(MODELS_DIR, "rnn_tokenizer_{}.pkl".format(DIMENSIONS[k])), "rb"
        # ) as f:
        #     tokenizer = pickle.load(f)
        tokenizer = TOKENIZER[k]

        def preprocess(x):
            lemmatized = lemmatize(x)
            tokenized = tokenizer.texts_to_sequences(lemmatized)
            return pad_sequences(tokenized, maxlen=MAX_POST_LENGTH)

        predictions = model.predict(preprocess(text))
        prediction = float(sum(predictions) / len(predictions))
        # print(DIMENSIONS[k])
        # print(prediction)
        if prediction >= 0.5:
            final += DIMENSIONS[k][1]
        else:
            final += DIMENSIONS[k][0]

    return final

def check(str_to_check, expected_result):
    index = 0
    for i in range(len(expected_result)):
        if expected_result[i] == str_to_check[i]:
            index += 1
    return index

def get_progress():
    progress_file = open("../data/progress.txt", "r", encoding="UTF8")
    percentage = [0, 0, 0, 0, 0]
    count = 0
    for line in progress_file:
        count += 1
        percentage[int(line.replace("\n", ""))] += 1
    progress_file.close()
    return count, percentage

def get_predict():
    with open("../data/tests_test.txt", "r", encoding="UTF8") as test_file:
        with open("../data/progress.txt", "a", encoding="UTF8") as progress_file:
            (already_count, percentage) = get_progress()
            count = 0
            prev_percent = 0
            for line in test_file:
                if count < already_count:
                    count += 1
                    continue
                try:
                    parts = line.split("|")
                    expected = parts[1]
                    result = predict_rnn(parts[2].replace("\n", ""))
                    count += 1
                    index = check(result, expected)
                    progress_file.write(f"{index}\n")
                    percentage[index] += 1
                    if prev_percent < int(count * 100 / 102496):
                        prev_percent = int(count * 100 / 102496)
                        print(f"{prev_percent}%")
                except Exception:
                    pass

            return count, percentage

(count_sum, percentages) = get_predict()

for part in percentages:
    print(f"{round(part/count_sum * 100, 2)}%")