from Parser import Parser


def main():
    parser = Parser()
    subreddits = ["mbti", "mbtimemes", "ISTJ", "ISTJmemes", "isfj", "ISFJmemes", "infj", "INFJmemes", "istp", "ISTPmemes",
                  "isfp", "ISFPmemes", "infp", "INFPmemes", "INTP", "INTPmemes", "estp", "ESTPmusic", "ENFP", "ENFPmemes",
                  "ESFP", "ESFPmemes", "ESTJ", "ESTJmemes", "ESFJ", "ESFJmemes", "enfj", "ENFJmemes", "entj", "ENTJmemes",
                  "intj", "INTJmemes", "entp", "ENTPmemes"]
    for subreddit in subreddits:
        parser.get_users_with_flairs_from_comments(subreddit)
    parser.unify_authors()
    parser.write_authors_to_file()
    parser.clear_file_with_texts()
    parser.read_authors_from_file()
    parser.read_read_authors_from_file()
    parser.count_type_limits()
    parser.get_users_texts()
    parser.clear_file_with_texts()


if __name__ == '__main__':
    main()
