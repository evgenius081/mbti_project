import string


def clean_text(text):
    words = text.split()
    words = [i.lower() for i in words]
    words = [i for i in words if not "http" in i]
    words = " ".join(words)
    words = words.translate(words.maketrans('', '', string.punctuation))
    return words

