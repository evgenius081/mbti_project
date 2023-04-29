from joblib import load
from preprocess import prep_data
from pathlib import Path
import time
import os

###############################################################################
#            FUNCTION TO COMBINE THE RESULTS OF THE 4 MODELS                  #
###############################################################################


def trace_back(combined):
    type_list = [
        {"0": "I", "1": "E"},
        {"0": "N", "1": "S"},
        {"0": "F", "1": "T"},
        {"0": "P", "1": "J"},
    ]
    result = []
    for num in combined:
        s = ""
        for i in range(len(num)):
            s += type_list[i][num[i]]
        result.append(s)
    return result


def combine_classes(y_pred1, y_pred2, y_pred3, y_pred4):
    combined = []
    for i in range(len(y_pred1)):
        combined.append(
            str(y_pred1[i]) + str(y_pred2[i]) + str(y_pred3[i]) + str(y_pred4[i])
        )
    result = trace_back(combined)
    return result[0]


###############################################################################
#                           MODEL PREDICTIONS                                 #
###############################################################################


def predict(s):

    X = prep_data(s)

    # loading the 4 models
    EorI_model = load(os.path.join("models", "clf_is_Extrovert.joblib"))
    SorN_model = load(os.path.join("models", "clf_is_Sensing.joblib"))
    TorF_model = load(os.path.join("models", "clf_is_Thinking.joblib"))
    JorP_model = load(os.path.join("models", "clf_is_Judging.joblib"))

    # predicting
    EorI_pred = EorI_model.predict(X)
    SorN_pred = SorN_model.predict(X)
    TorF_pred = TorF_model.predict(X)
    JorP_pred = JorP_model.predict(X)

    # combining the predictions from the 4 models
    result = combine_classes(EorI_pred, SorN_pred, TorF_pred, JorP_pred)

    return result


###############################################################################
#                                   MAIN                                      #
###############################################################################

if __name__ == "__main__":
    t = time.time()


    # base dataset path. You should place directories containing textes to be predicted.
    dataset_path = str(Path.home())+ '/dataset/'

    def collect_entries_for(directory_name: str):
        return [os.path.join(dirname, filename) \
                for dirname, _, filenames in os.walk(dataset_path + directory_name) \
                 for filename in filenames if filename != '.DS_Store']


    journals_texts = collect_entries_for('journals')

    stanbar_texts = collect_entries_for('stanbar')

    # Derek Sivers's texts, he has a lot of texts and is known as INTJ
    sivers_texts = collect_entries_for('sivers')

    # Tim Ferris's texts, he has a lot of texts and is known as INTJ
    ferris_texts = collect_entries_for('ferriss')


    for file in ferris_texts:
        print(file)
        lines = [line for line in [line.strip() for line in open(file).readlines()] if line]
        text = " ".join(lines)


#         if len(text) > 1024:
#             print(f"The text in {file} has been truncated by {len(text)-1024} chars ({(len(text)-1024)/len(text)} %)")
#             truncated = text[:1024]
#         else:
#             truncated = text
        # prediction = predict(truncated)

        prediction = predict(text)
        print(file, prediction)
        print("-----------------------------------------------------")




    print(f"Preprocessing Time: {time.time() - t} seconds")
