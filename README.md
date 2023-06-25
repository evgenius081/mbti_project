# MBTIfy
## About the project
The aim of this project is to create a REST API web application (using Python at backend and React JS at frontend) that will analyze users' Reddit (or other social network in the future) accounts or single texts written by these users to predict, which personality type do they have. As a personality type model MBTI was chosen, as it's the most popular type and there is a lot of information about it on the Internet. The Myers-Briggs Type Indicator (**MBTI**) is a psychological tool designed to assess personality preferences and categorize individuals into specific personality types. It was developed by Isabel Myers and Katharine Briggs, based on the work of Carl Jung.

The MBTI measures personality across four dichotomies:

1. **Extraversion** (E) vs. **Introversion** (I): Determines whether individuals are more energized by external stimulation and interaction (extraversion) or by internal thoughts and reflection (introversion).

2. **Sensing** (S) vs. **Intuition** (N): Focuses on how individuals gather information. Sensing individuals rely on their five senses and prefer concrete facts and details, while intuitive individuals are more focused on patterns, possibilities, and abstract concepts.

3. **Thinking** (T) vs. **Feeling** (F): Examines how individuals make decisions. Thinking individuals tend to base decisions on logical analysis and objective considerations, while feeling individuals prioritize personal values and consider the impact on others' feelings.

4. **Judging** (J) vs. **Perceiving** (P): Describes how individuals approach the outside world. Judging individuals prefer structure, organization, and closure, while perceiving individuals are more flexible, adaptable, and open to new information.

These four dichotomies combine to create 16 different personality types, such as ISTJ (Introverted, Sensing, Thinking, Judging), ENFP (Extraverted, Intuitive, Feeling, Perceiving), and so on.

It's important to note that the MBTI is a self-reported assessment and is based on preferences rather than fixed traits. It provides insights into how individuals perceive and interact with the world, but it is not intended to predict behavior or measure intelligence. And another notable information is that most people during these self-reports do not answer questions in the assesment totally honestly, and in fact the results of this test show who this person wants to be or who he thinks he is rather than who he really is. That's why **dataset is not 100% reliable**, but it is the best we could gather.

## Parser for dataset
Code and description of dataset creator can be found [here](https://github.com/evgenius081/mbti_project/tree/parser).

## Model training
Results of tests with different models:
![image](https://github.com/evgenius081/mbti_project/assets/56554114/330e62cb-a44e-4194-b9fd-2406dbe8beff)
Results of tests with smaller test dataset, because ChatGPT is not free:
![image](https://github.com/evgenius081/mbti_project/assets/56554114/6e86bdf3-40a0-4981-bd22-51e5fbac1fcc)

After trying several machine learning models, we claimed that BERT model was the most successfull, that is why we recommend you to use it as a model for the further work. Code and description of BERT trainig can be found [here](https://github.com/evgenius081/mbti_project/tree/bert).


## Backend
Backend of this application is written using Python programming language. It uses BERT model, trained in previous step on balanced oversampled dataset, as a predictioning model, parser, created in previous steps, and Flask as REST API framework. Flask handles requests, than uses parser (if Redditor username provided) to get posts and comments written by this user and than all these texts are passed through predictor, which predicts personality type and than provides results to the requestor. 

Requirements:
- Python 3.11
- datasets (v2.11.0)
- Flask (v2.3.2)
- Flask_Cors (v3.0.10)
- praw (v7.7.0)
- prawcore (v2.3.0)

It also uses `pytorch` for predictioning purposes, it will be discussed below.

### Startup (folder - `Backend`)
1. download this repo or run in terminal
   ```cmd
   git clone https://github.com/evgenius081/mbti_project.git
   ```
2. place folder `model` gained from model training into the `BERT` folder or download one of the models [here](https://drive.google.com/drive/folders/1x5rG8NtXbRai7eUY4y-jtc7zlbiJK7ss?usp=sharing) (each new version is more precise than previous one) and name the unzipped folder `model` and place it to the `BERT` folder. 
3. create file ``config.ini`` to the `Backend` folder, which contents the following data:
```ini
[AUTH_INFO]
client_id = <Reddit API client id>
client_secret = <Reddit API client secret>
user_agent = test
```
4. run in terminal
   ```cmd
   pip install -r requirements.txt
   ```
5. visit [this page](https://pytorch.org/get-started/locally/) and choose the install command according to your OS (this will allow you to train this model on GPU, which is much fuster and sefier than training it on CPU, which can occasionally melt your processor), and than run this command in terminal
6. run main.py using your installed python interpreter (according to your OS) od IDE.

### API refference
Backend handles 2 types of requests:
- GET `http://localhost:5000/user?username=<Redditor username>` which predicts personality type using username

  Response:
  ```json
  {
    "IE": [<some_number>, <some_number>],
    "JP": [<some_number>, <some_number>],
    "NS": [<some_number>, <some_number>],
    "TF": [<some_number>, <some_number>]
  }
  ```
  Each number means how many times predicted that this user has the following letter in his MBTI type
- POST `http://localhost:5000/text` with following `Body`:
  ```json
  {"text": "<text to predict by>"}
  ```
  which predicts personality type basing on single text. Response is the same as in previous.

## Frontend
Frontend is written in Javascript using React framework. It provides a user with:
- brief information about the project
  ![image](https://github.com/evgenius081/mbti_project/assets/56554114/40321d08-dcac-4b07-a10c-7d8962d580aa)

- possibility to provide username of Redditor to know his personality type
  ![image](https://github.com/evgenius081/mbti_project/assets/56554114/1e66d24f-4777-46fd-8f76-0aa809d8efef)

- possibility to provide text to know author's personality type
  ![image](https://github.com/evgenius081/mbti_project/assets/56554114/430c1aea-15f9-4a1c-bcc7-3743b66c20c4)

- information about probabilities about his type and description for the most certain type
  ![image](https://github.com/evgenius081/mbti_project/assets/56554114/b89cfb2f-23bc-45f2-9581-17678028a1cc)

  These color lines show the distribution between opposities in each pair, for example this person in rather INFP, because response from the backend is the following:
  ```json
  {
    "IE": [654, 369],
    "JP": [404, 619],
    "NS": [560, 463],
    "TF": [372, 651]
  }
  ```
- information about our team
  ![image](https://github.com/evgenius081/mbti_project/assets/56554114/c51cbf6d-2291-4c92-92fc-67cae3bc0786)


Requirements:
- Node.js (v18.15.0)
- bootstrap (v5.2.3)
- react (v18.2.0)
- react-bootstrap (v2.7.4)
- react-dom (v18.2.0)
- react-router-dom (v6.10.0)
- react-scripts (v5.0.1)
- reactstrap (v9.1.9)
- dotenv (v16.0.3)
- web-vitals (v2.1.4)
- mui/material (v5.12.3)
- emotion/styled (v11.11.0)
- emotion/react (v11.11.0)

### Startup (folder - `Frontend`)
1. download this repo or run in terminal
  ```cmd
  git clone https://github.com/evgenius081/mbti_project.git
  ```
2. run in terminal
  ```cmd
  npm install
  ```
3. run in terminal
  ```cmd
  npm start
  ```

## Results
Summarizing the work done, our group created a working application using Python and JS as programming languages, BERT, React and Reddit API as main technologies. The model trained on gathered data is pretty successfull:
![image](https://github.com/evgenius081/mbti_project/assets/56554114/5fb91ca5-ee8b-4d03-ad8e-a68eb0b793cd)

In the final project version oversampled dataset was used, which average rate was **71.9%**, which is a pretty good result, assuming that dataset cannot be 100% trusted as it was trained on peoples' self-estimates. Although we claim that this project was rather successfull, we understand that it is far from ideal and needs future development, which may include, for example, more reliable training dataset and more powerful machine learning model.
