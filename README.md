# MBTI project training
This is code for training Bidirectional Encoder Representations from Transformers (**BERT**) machine learning model. Model was trained using Python programming language and torch library.

Requirments:
- Python 3.11
- datasets library (v2.11.0) 
- numpy library (v1.24.2)
- transformers (v4.27.4)

Torch version is not listed here and will be discussed below.

## Startup
1. download this repo or run `git clone --branch bert https://github.com/evgenius081/mbti_project.git` in terminal
2. run `pip install -r requirements.txt` in terminal
3. visit [this page](https://pytorch.org/get-started/locally/) and choose the install command according to your OS (this will allow you to train this model on GPU, which is much fuster and sefier than training it on CPU, which can occasionally melt your processor), and than run this command in terminal
4. copy dataset file gathered from [parser](https://github.com/evgenius081/mbti_project/tree/parser) transformed to `csv` format having first line `type,posts` and following lines like `<author's MBTI type>,"<post>"` to this folder (you cand find our files [here](https://drive.google.com/drive/folders/1XPZkt6eF4KoGBNX1r19i4dBoOwW7YUy2))
5. (optional) if dataset is not balanced, run `oversampling.py` or `undersampling.py` using your installed python interpreter (according to your OS) od IDE according to your will (assuming your dataset is named `dataset.csv`).
6. change line 12 to your dataset filename
   ```python
   dataset_file = "<dataset filename>"
   ```
7. run `learn.py` using your installed python interpreter (according to your OS) od IDE.

## Results
After learning is finished and `model` folder is created, you can perform predictions using this model using `predict.py` file. Here are results of the testing models trained on different datasets:
![image](https://github.com/evgenius081/mbti_project/assets/56554114/5fb91ca5-ee8b-4d03-ad8e-a68eb0b793cd)

### Explaination:
These charts mean tha percentage of correctly predicted letters (for example 75 on oversampling 'F' means that among 100% F's in test dataset 75% were predicted correctly).

MBTI model has 4 pairs of letters (E&I, N&S, F&T, J&P), forming 16 personality types. In each pair, these charts need to be of a close heights (difference of 20% is acceptable, of 80% - is not), because the high difference between them means that model is overtrained and will practically always predict only one letter from the pair. That is why unbalanced dataset is not suitable for prediction, because it will practically always predict INTJ type. It means that train dataset must be balanced. There are 2 types of dataset balancing:
- oversampling (random duplicating of texts of lacking types)
- undersampling (random deleting of texts of redundant types)

There is also second parameter of model's correctness besides equality of charts - height of these charts, or how correct are model's prediction. Assumig all of the above, we can claim that from listed dataset types (unbalanced, oversampled and undersampled) oversampled is the best.
