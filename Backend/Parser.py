import praw
from configparser import ConfigParser
from pathlib import Path

from prawcore import NotFound


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
        self.banned_words = ["https://", "[removed]"]
        self.symbol_mapper = [["*", ""], ["\\", " "], ["|", ""], ["\n", " "], ["#", ""], ["\"", ""], ["  ", " "],
                              ["'", ""]]

    def get_users_texts(self, author):
        try:
            return self.get_user_comments(author) + self.get_user_posts(author)
        except Exception as e:
             pass

    def get_user_posts(self, username):
        res_list = []
        submissions = self.reddit.redditor(username).submissions.new(limit=100000)
        for line in submissions:
            if line.selftext != "":
                res_list.append(self.map_symbols(line.selftext))
        return res_list

    def get_user_comments(self, username):
        res_list = []
        comments = self.reddit.redditor(username).comments.new(limit=100000)
        for line in comments:
            if line.body != "":
                res_list.append(self.map_symbols(line.body))
        return res_list

    def map_symbols(self, text):
        new_text = text
        for pair in self.symbol_mapper:
            new_text = new_text.replace(pair[0], pair[1])
        return new_text

    def user_exists(self, username):
        try:
            self.reddit.redditor(username).id
        except NotFound:
            return False
        return True
