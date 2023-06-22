from BERT.predict import *
from flask_cors import CORS, cross_origin
from Parser import Parser
from flask import Flask, jsonify, request
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/user', methods=["GET"])
@cross_origin()
def get_by_username():
    parser = Parser()
    if not parser.user_exists(request.args.get("username")):
        return "User not found", 400
    texts = parser.get_users_texts(request.args.get("username"))
    results = {"I": 0, "E": 0, "N": 0, "S": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    for text in texts:
        res = predict_for_texts(text)
        for letter in res:
            results[letter] += 1
    return jsonify({"IE": [results["I"], results["E"]], "NS": [results["N"], results["S"]],
                    "TF": [results["T"], results["F"]], "JP": [results["J"], results["P"]]})


@app.route('/text', methods=['POST'])
def get_by_text():
    results = {"I": 0, "E": 0, "N": 0, "S": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    res = predict_for_texts(request.get_json()["text"])
    for letter in res:
        results[letter] += 1
    return jsonify({"IE": [results["I"], results["E"]], "NS": [results["N"], results["S"]],
                    "TF": [results["T"], results["F"]], "JP": [results["J"], results["P"]]})


app.run()