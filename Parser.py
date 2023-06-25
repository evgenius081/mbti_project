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
        self.types = ["ISTJ", "ISFJ", "INFJ", "INTJ", "ISTP", "ISFP", "INFP", "INTP", "ESTP", "ESFP", "ENFP", "ENTP", "ESTJ", "ESFJ", "ENFJ", "ENTJ"]
        self.author_filename = "authors.txt"
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
        submissions = self.reddit.redditor(username).submissions.new(limit=self.type_limits[self.types.index(mbti_type)])
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
                        f.write(str(self.authors_and_ids[username])+"|"+mbti_type+"|"+txt+"\n")
                elif text_type == "comment":
                    txt = self.map_symbols(text.body)
                    if self.check_text(txt):
                        self.text_count += 1
                        f.write(str(self.authors_and_ids[username])+"|"+mbti_type+"|"+txt+"\n")
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
            f.write(author+"\n")
        f.close()

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
                author = list(self.authors_and_ids.keys())[list(self.authors_and_ids.values()).index(line.split("|")[0])]
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
                    self.authors_with_ids_and_types.append(self.types[id]+"|"+str(comment.author)+"\n")
                    f.write(str(self.authors_number) + "|" + self.types[id]+"|"+str(comment.author)+"\n")
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
        f.close()

    def count_author_stat(self):
        f = open(self.author_filename, "r", encoding="UTF8")
        for line in f:
            self.stats[self.types.index(line.split("|")[1])][0] += 1
        f.close()

    def display_author_text_stat(self):
        self.count_text_stat()
        self.count_author_stat()
        print("Type    user    texts")
        for stat in self.stats:
            print(self.types[self.stats.index(stat)] + "    " + str(round(stat[0] * 100/sum([i[0] for i in self.stats]), 2))
                  + "%      " + str(round(stat[1] * 100/sum([i[1] for i in self.stats]), 2)) + "%")

