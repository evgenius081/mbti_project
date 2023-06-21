# MBTIfy
## Backend
You need to download one of the models [here](https://drive.google.com/drive/folders/1x5rG8NtXbRai7eUY4y-jtc7zlbiJK7ss?usp=sharing), each new version is more precise than previous one. The folder with the model must be named `model` and placed to the folder `Backend/BERT`. 

You also need to add file ``config.ini`` to the `Background` folder, which contents following data:
```ini
[AUTH_INFO]
client_id = <Reddit API client id>
client_secret = <Reddit API client secret>
user_agent = test
```
After that, depending on operating system, run in terminal in paretn folder 
```cmd
python main.py
``` 
or
```cmd
python3 main.py
```
or
```cmd
py main.py
``` 

## Frontend startup
In `Frontend` folder run 
```cmd
npm install
```
Then, in `Frontend` folder run 
```cmd
npm start
```
