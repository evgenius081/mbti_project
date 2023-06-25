import random
import os

source_filename = "dataset.csv"
dest_filename = "dataset_oversampled.csv"
types = ["INTJ", "INTP", "ENTJ", "ENTP", "INFJ", "INFP", "ENFJ", "ENFP", "ISTJ", "ISFJ", "ESTJ", "ESFJ",
                     "ISTP", "ISFP", "ESTP", "ESFP"]
types_count = {"INTJ": 0, "INTP": 0, "ENTJ": 0, "ENTP": 0, "INFJ": 0, "INFP": 0, "ENFJ": 0, "ENFP": 0,
               "ISTJ": 0, "ISFJ": 0, "ESTJ": 0, "ESFJ": 0, "ISTP": 0, "ISFP": 0, "ESTP": 0, "ESFP": 0}


def separate_file():
    source = open(source_filename, "r", encoding="UTF8")
    files = {}
    for mbti_type in types:
        files[mbti_type] = open(f"{mbti_type}_oversampling", "w", encoding="UTF8")

    source.readline()
    for line in source:
        parts = line.split(",\"")
        types_count[parts[0]] += 1
        files[parts[0]].write(line)

    for mbti_type in types:
        files[mbti_type].close()
    source.close()


def oversample_type(mbti_type):
    f = open(f"{mbti_type}_oversampling", "r", encoding="UTF8")
    texts = []

    for line in f:
        texts.append(line)

    for i in range(max(types_count.values()) - types_count[mbti_type]):
        id_to_duplicate = random.randint(0, len(texts) - 1)
        texts.append(texts[id_to_duplicate])

    f.close()

    dest = open(dest_filename, "a", encoding="UTF8")

    for line in texts:
        dest.write(line)

    dest.close()


separate_file()
dest = open(dest_filename, "w", encoding="UTF8")
dest.write("type,posts")
dest.close()
for mbti_type in types:
    oversample_type(mbti_type)
for mbti_type in types:
    os.remove(f"{mbti_type}_oversampling")



