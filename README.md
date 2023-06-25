# MBTI project parser
Parser getting posts and comments from users of Reddit social network with known MBTI type. Posts and comments (texts) are parsed from suberddits (Reddit communities) connected with MBTI, where users set flairs with thier MBTI type. After that, having the list of users with set flairs, we can parse all the texts written by these users (not only in subreddits connected with MBTI). These way we get a dataset for machine learning purposes.
> **_NOTE:_** Developing this project, we assumed that these flairs are reliable, although they are not due to human nature to estimate themselves in a wrong way.

Texts are filtered by length (30 symbols min by default), texts must not have links and not be deleted. Texts will also be written without line breaks and reddit markdown.

## Getting started

Project requirments:
- Python 3.11
- praw library (v7.7.0) - library for Reddit API
- Client app for Reddit (see [here](https://praw.readthedocs.io/en/stable/getting_started/quick_start.html) how to create it)

## Startup
1. download this repo or run `git clone --branch parser https://github.com/evgenius081/mbti_project.git` in terminal
2. run `pip install -r requirements.txt` in terminal
3. create file `config.ini` and place there following code

  ```ini
  [AUTH_INFO]
  client_id = <your reddit client id>
  client_secret = <your reddit client secret>
  user_agent = test
  [AMOUNTS]
  texts_limit = <max number of texts e.g. 200000>
  max_limit_for_author = <average max texts number for each MBTI type e.g. 30>
  comment_look_through_limit = <how many comments to look through in subreddits, e.g. 500000>
  min_text_length = <min length of texts to be taken e.g. 30>
  ```

4. run `main.py` using your installed python interpreter (according to your OS) od IDE.

As a result after ~10 hours (for examplary settings in config.ini file) you will get `authors.txt`, `texts.txt` files and stats for taken users and texts. In authors.txt authors of comments can be found as `User ID|MBTI type|User nickname`. In texts there are texts written by these users as `User ID|MBTI type|Text`.
