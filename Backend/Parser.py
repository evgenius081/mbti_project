import random

import praw
from configparser import ConfigParser
from pathlib import Path


class Parser:
    def __init__(self):
        config_object = ConfigParser()
        config_object.read("config.ini")
        user_info = config_object["AUTH_INFO"]
        self.reddit = praw.Reddit(
            client_id=user_info["client_id"],
            client_secret=user_info["client_secret"],
            user_agent=user_info["user_agent"],
        )
        self.types = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP",
                      "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
        self.author_filename = "authors.txt"
        self.text_filename_csv = "texts.csv"
        self.text_filename = "texts.txt"
        self.banned_words = ["https://", "[removed]"]
        self.symbol_mapper = [["*", ""], ["\\", " "], ["|", ""], ["\n", " "], ["#", ""], ["\"", ""], ["  ", " "]]
        amounts = config_object["AMOUNTS"]
        self.texts_limit = amounts["texts_limit"]
        self.max_limit_for_author = amounts["max_limit_for_author"]
        self.comment_look_through_limit = amounts["comment_look_through_limit"]
        self.min_text_length = amounts["min_text_length"]
        self.authors = []
        self.authors_number = 0
        self.authors_with_ids_and_types = []
        self.authors_and_ids = {}
        self.read_authors = []
        self.lacking_types = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.text_count = 0
        self.stats = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                      [0, 0], [0, 0], [0, 0], [0, 0]]
        self.type_limits = []
        path_a = Path(self.author_filename)
        path_t = Path(self.text_filename)
        if not path_t.is_file():
            f1 = open(self.text_filename, "x", encoding="UTF8")
            f1.close()
        if not path_a.is_file():
            f2 = open(self.author_filename, "x", encoding="UTF8")
            f2.close()

    def get_users_texts(self):
        for author_and_type in self.authors_with_ids_and_types:
            author = author_and_type.split("|")[2]
            mbti = author_and_type.split("|")[1]
            if author not in self.read_authors:
                try:
                    self.get_user_comments(author, mbti)
                    if self.text_count > int(self.texts_limit):
                        break
                    self.get_user_posts(author, mbti)
                    if self.text_count > int(self.texts_limit):
                        break
                    print(f"Ended writing for user {author} with type {mbti}")
                except Exception as e:
                    print(f"Error occurred with author {author}: {str(e)}")

        print(f"Finished writing {self.text_count} texts.")

    def get_user_posts(self, username, mbti_type):
        submissions = self.reddit.redditor(username).submissions.new(
            limit=self.type_limits[self.types.index(mbti_type)])
        self.write_text(username, mbti_type, submissions, "post")

    def get_user_comments(self, username, mbti_type):
        comments = self.reddit.redditor(username).comments.new(limit=self.type_limits[self.types.index(mbti_type)])
        self.write_text(username, mbti_type, comments, "comment")

    def write_text(self, username, mbti_type, texts, text_type):
        f = open(self.text_filename, "a", encoding="UTF8")
        for text in texts:
            if self.text_count < int(self.texts_limit):
                if text_type == "post":
                    txt = self.map_symbols(text.selftext)
                    if self.check_text(txt):
                        self.text_count += 1
                        f.write(str(self.authors_and_ids[username]) + "|" + mbti_type + "|" + txt + "\n")
                elif text_type == "comment":
                    txt = self.map_symbols(text.body)
                    if self.check_text(txt):
                        self.text_count += 1
                        f.write(str(self.authors_and_ids[username]) + "|" + mbti_type + "|" + txt + "\n")
            else:
                break
        f.close()

    def unify_authors(self):
        self.read_authors_from_file()
        new_authors = []
        new_authors_with_ids_and_types = []
        new_authors_number = 0
        for author in self.authors:
            if author not in new_authors:
                new_authors.append(author)
                new_authors_with_ids_and_types.append(self.authors_with_ids_and_types[self.authors.index(author)])
                new_authors_number += 1
        self.authors = new_authors
        self.authors_with_ids_and_types = new_authors_with_ids_and_types
        self.authors_number = new_authors_number

    def write_authors_to_file(self):
        f = open(self.author_filename, "w", encoding="UTF8")
        for author in self.authors_with_ids_and_types:
            f.write(author + "\n")
        f.close()

    def oversample(self, arr, count):
        diff = count - len(arr)
        for i in range(diff):
            arr.append(arr[random.randint(0, len(arr) - 1)])
        print(len(arr))
        return arr

    def check_if_not_in_dataset(self, str_to_check):
        f = open("test.csv", "r", encoding="UTF8")

        for line in f:
            if line.split("|")[2].replace("\n", "").replace("\"", "") == str_to_check:
                return True

        f.close()
        return False

    def get_type(self, type_to_find):
        f = open(self.text_filename, "r", encoding="UTF8")
        arr = []

        for line in f:
            if line.split("|")[1] == type_to_find and not self.check_if_not_in_dataset(
                    line.split("|")[2].replace("\n", "").replace("\"", "")):
                arr.append(line.split("|")[2].replace("\n", "").replace("\"", ""))

        f.close()
        return arr

    def get_balanced_dataset(self):
        f1 = open(self.text_filename, "r", encoding="UTF8")
        f2 = open("balanced_dataset_2.csv", "w", encoding="UTF8")
        f2.write("type,posts\n")

        types = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for line in f1:
            types[self.types.index(line.split("|")[1])] += 1
        f1.close()

        for i in range(16):
            print(f"{self.types[i]}: {types[i]}")

        max_type_count = max(types) - 100

        for mbti_type in self.types:
            arr = self.oversample(self.get_type(mbti_type), max_type_count)

            for line in arr:
                f2.write(f"{mbti_type},\"{line}\"\n")

        f2.close()

    def map_symbols(self, text):
        new_text = text
        for pair in self.symbol_mapper:
            new_text = new_text.replace(pair[0], pair[1])
        return new_text

    def check_text(self, text):
        for banned_word in self.banned_words:
            if banned_word in text:
                return False
        if text == "" or len(text) < int(self.min_text_length):
            return False
        return True

    def read_authors_from_file(self):
        f = open(self.author_filename, "r", encoding="UTF8")
        self.authors = []
        self.authors_with_ids_and_types = []
        counter = 0
        for line in f:
            self.authors.append(line.split("|")[2].replace("\n", ""))
            self.authors_and_ids[line.split("|")[2].replace("\n", "")] = line.split("|")[0]
            self.authors_with_ids_and_types.append(line.replace("\n", ""))
            counter += 1
        self.authors_number = counter
        f.close()

    def read_read_authors_from_file(self):
        f = open(self.text_filename, "r", encoding="UTF8")
        for line in f:
            if len(line) > 4:
                author = list(self.authors_and_ids.keys())[
                    list(self.authors_and_ids.values()).index(line.split("|")[0])]
                if author not in self.read_authors:
                    self.read_authors.append(author)
        f.close()

    def check_type(self, text):
        for mbti_type in self.types:
            if mbti_type in str(text).replace(" ", ""):
                return self.types.index(mbti_type)
        return -1

    def get_users_with_flairs_from_comments(self, subreddit_name):
        subreddit = self.reddit.subreddit(subreddit_name)
        self.read_authors_from_file()
        f = open(self.author_filename, "a")
        for comment in subreddit.comments(limit=self.comment_look_through_limit):
            id = self.check_type(comment.author_flair_text)
            if id != -1:
                if str(comment.author) not in self.authors:
                    self.authors_number += 1
                    print(str(self.types[id]) + "|" + str(comment.author))
                    self.authors.append(comment.author)
                    self.authors_with_ids_and_types.append(self.types[id] + "|" + str(comment.author) + "\n")
                    f.write(str(self.authors_number) + "|" + self.types[id] + "|" + str(comment.author) + "\n")
        f.close()

    def clear_file_with_texts(self):
        f = open(self.text_filename, "r", encoding="UTF8")
        texts = []
        counter = 0
        for line in f:
            if "|" not in str(line) or line == "\n":
                texts[counter - 1] = texts[counter - 1].replace("\n", " ")
                new_line = str(line).replace("\n", "")
                texts[counter - 1] += new_line + "\n"
            else:
                texts.append(line)
                counter += 1
        f.close()

        f = open(self.text_filename, "w", encoding="UTF8")
        for text in texts:
            f.write(text)
        f.close()

    def count_type_limits(self):
        self.count_author_stat()
        for stat in self.stats:
            self.type_limits.append(max([i[0] for i in self.stats]) * int(self.max_limit_for_author) / stat[0])

    def count_text_stat(self):
        f = open(self.text_filename, "r", encoding="UTF8")
        for line in f:
            self.stats[self.types.index(line.split("|")[1])][1] += 1
            self.text_count += 1
        f.close()

    def count_author_stat(self):
        f = open(self.author_filename, "r", encoding="UTF8")
        for line in f:
            self.stats[self.types.index(line.split("|")[2].replace("\n", ""))][0] += 1
        f.close()

    def display_author_text_stat(self):
        self.count_text_stat()
        self.count_author_stat()
        print("Type    user    texts")
        for stat in self.stats:
            print(self.types[self.stats.index(stat)] + "    " + str(
                round(stat[0] * 100 / sum([i[0] for i in self.stats]), 2))
                  + "%      " + str(round(stat[1] * 100 / sum([i[1] for i in self.stats]), 2)) + "%")
        print(f"Text count: {self.text_count}")

    def to_csv(self, filename):
        src = open(filename, "r", encoding="UTF8")
        dst = open(filename.replace("txt", "csv"), "w", encoding="UTF8")

        dst.write("type,posts\n")
        current_author_id = ""

        for line in src:
            parts = line.split("|")
            if current_author_id != parts[0]:
                if current_author_id != "":
                    dst.write("'\"\n")
                current_author_id = parts[0]
                dst.write(parts[1] + ",\"'" + parts[2].replace("\n", ""))
            else:
                dst.write("|||" + parts[2].replace("\n", ""))

        dst.write("'\"\n")
        dst.close()
        src.close()

    def reformat(self, old_file):
        src = open(old_file, "r", encoding="UTF8")
        dst = open(self.text_filename, "w", encoding="UTF8")
        authors = open(self.author_filename, "w", encoding="UTF8")
        self.authors_number = 0
        prev_author = ""

        for line in src:
            parts = line.split("|")
            if parts[0] != prev_author:
                self.authors_number += 1
                prev_author = parts[0]
                authors.write(f"{self.authors_number}|{parts[0]}|{parts[1]}\n")
            dst.write(f"{self.authors_number}|{parts[1]}|{parts[2]}")

        src.close()
        dst.close()
        authors.close()

    def split_to_learn_and_test(self):
        learn = open("texts_learn.txt", "w", encoding="UTF8")
        test = open("tests_test.txt", "w", encoding="UTF8")
        src = open(self.text_filename, "r", encoding="UTF8")

        tests_numbers = self.count_test_data()
        limits = []
        for stat in self.stats:
            limits.append(stat[1] - tests_numbers[self.stats.index(stat)])

        for line in src:
            mbti_type = line.split("|")[1]
            if limits[self.types.index(mbti_type)] == 0:
                test.write(line)
            else:
                learn.write(line)
                limits[self.types.index(mbti_type)] -= 1

        src.close()
        learn.close()
        test.close()

    def count_test_data(self):
        for_test = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for k in range(23):
            for i in self.stats:
                perc = i[1] * 100 / sum([i[1] for i in self.stats])
                if perc > 6.25:
                    for_test[self.stats.index(i)] += int(i[1] * (perc - 6.25) / 100)
        number_of_test = sum(for_test)
        for stat in for_test:
            if stat == 0:
                for_test[for_test.index(stat)] = int((int(self.text_count * 0.2) - number_of_test) / 8)

        return for_test
