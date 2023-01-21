import praw
from configparser import ConfigParser


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
        self.authors = []
        self.authors_number = 0
        self.authors_with_types = []
        self.banned_words = ["https://", "[removed]"]
        self.symbol_mapper = [["*", ""], ["\\", " "], ["|", ""], ["\n", " "], ["#", ""], ["\"", ""], ["  ", " "]]
        self.read_authors = []
        self.texts_limit = 500000
        self.max_limit_for_author = 30
        self.lacking_types = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.text_count = 0
        self.stats = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0],
                      [0, 0], [0, 0], [0, 0], [0, 0]]
        self.type_limits = []

    def get_posts_of_type(self, mbti_type):
        for author in self.authors_with_types:
            if author.split(":")[0] == mbti_type:
                self.get_user_posts(author.split(":")[1], mbti_type)
                self.get_user_comments(author.split(":")[1], mbti_type)

    def get_user_posts(self, username, mbti_type):
        submissions = self.reddit.redditor(username).submissions.new(limit=self.type_limits[self.types.index(mbti_type)])
        self.write_text(username, mbti_type, submissions, "post")

    def get_user_comments(self, username, mbti_type):
        comments = self.reddit.redditor(username).comments.new(limit=self.type_limits[self.types.index(mbti_type)])
        self.write_text(username, mbti_type, comments, "comment")

    def write_text(self, username, mbti_type, texts, text_type):
        f = open("texts_with_types.txt", "a", encoding="UTF8")
        for text in texts:
            if self.text_count < self.texts_limit:
                if text_type == "post":
                    txt = self.map_symbols(text.selftext)
                    if self.check_text(txt):
                        self.text_count += 1
                        f.write(username+"|"+mbti_type+"|"+txt+"\n")
                elif text_type == "comment":
                    txt = self.map_symbols(text.body)
                    if self.check_text(txt):
                        self.text_count += 1
                        f.write(username+"|"+mbti_type+"|"+txt+"\n")
            else:
                break
        f.close()

    def unify_authors(self):
        self.read_authors_from_file()
        new_authors = []
        new_authors_with_types = []
        for author in self.authors:
            if author not in new_authors:
                new_authors.append(author)
                new_authors_with_types.append(self.authors_with_types[self.authors.index(author)])
        self.authors = new_authors
        self.authors_with_types = new_authors_with_types

    def write_authors_to_file(self):
        f = open("authors_and_types.txt", "w", encoding="UTF8")
        for author in self.authors_with_types:
            f.write(author+"\n")
        f.close()

    def map_symbols(self, text):
        new_text = text
        for pair in self.symbol_mapper:
            new_text = new_text.replace(pair[0], pair[1])
        return new_text

    def get_users_texts(self):
        for author_and_type in self.authors_with_types:
            author = author_and_type.split(":")[1].replace("\n", "")
            mbti = author_and_type.split(":")[0]
            if author not in self.read_authors:
                try:
                    self.get_user_comments(author, mbti)
                    if self.text_count > self.texts_limit:
                        break
                    self.get_user_posts(author, mbti)
                    if self.text_count > self.texts_limit:
                        break
                    print(f"Ended writing for user {author} with type {mbti}")
                except:
                    print(f"Error occure with author {author}")

        print(f"Finished writing {self.text_count} texts.")

    def check_text(self, text):
        for banned_word in self.banned_words:
            if banned_word in text:
                return False
        if text == "" or len(text) < 30:
            return False
        return True

    def read_authors_from_file(self):
        f = open("authors_and_types.txt", "r", encoding="UTF8")
        self.authors = []
        self.authors_with_types = []
        counter = 0
        for line in f:
            self.authors.append(line.split(":")[1].replace("\n", ""))
            self.authors_with_types.append(line.replace("\n", ""))
            counter += 1
        self.authors_number = counter
        f.close()

    def read_read_authors_from_file(self):
        f = open("texts_with_types.txt", "r", encoding="UTF8")
        for line in f:
            txt = line.split("|")[0].replace("\n", "")
            if txt not in self.read_authors:
                self.read_authors.append(txt)
        f.close()

    def check_type(self, text):
        for mbti_type in self.types:
            if mbti_type in str(text).replace(" ", ""):
                return self.types.index(mbti_type)
        return -1

    def get_users_with_flairs_from_comments(self, subreddit_name):
        subreddit = self.reddit.subreddit(subreddit_name)
        counter = 0
        self.read_authors_from_file()
        f = open("authors_and_types.txt", "a")
        for comment in subreddit.comments(limit=500000):
            id = self.check_type(comment.author_flair_text)
            if id != -1:
                if str(comment.author) not in self.authors:
                    counter += 1
                    print(str(self.types[id]) + ":" + str(comment.author))
                    self.authors.append(comment.author)
                    self.authors_with_types.append(self.types[id]+":"+str(comment.author)+"\n")
                    f.write(self.types[id]+":"+str(comment.author)+"\n")
        self.authors_number += counter
        f.close()

    def clear_file_with_texts(self):
        f = open("texts_with_types.txt", "r", encoding="UTF8")
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

        f = open("texts_with_types.txt", "w", encoding="UTF8")
        for text in texts:
            f.write(text)
        f.close()

    def count_type_limits(self):
        self.count_author_stat()
        for stat in self.stats:
            self.type_limits.append(max([i[0] for i in self.stats]) * self.max_limit_for_author / stat[0])

    def count_text_stat(self):
        f = open("texts_with_types.txt", "r", encoding="UTF8")
        for line in f:
            self.stats[self.types.index(line.split("|")[1])][1] += 1
        f.close()

    def count_author_stat(self):
        f = open("authors_and_types.txt", "r", encoding="UTF8")
        for line in f:
            self.stats[self.types.index(line.split(":")[0])][0] += 1
        f.close()

    def display_author_text_stat(self):
        self.count_text_stat()
        self.count_author_stat()
        print("Type    user    texts")
        for stat in self.stats:
            print(self.types[self.stats.index(stat)] + "    " + str(round(stat[0] * 100/sum([i[0] for i in self.stats]), 2))
                  + "%      " + str(round(stat[1] * 100/sum([i[1] for i in self.stats]), 2)) + "%")

