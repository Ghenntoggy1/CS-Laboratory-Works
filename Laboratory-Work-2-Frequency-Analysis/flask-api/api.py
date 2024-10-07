from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, Response
import json
import re
from collections import Counter

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def clean_text(cipher_text: str) -> str:
    cipher_text: str = re.sub(r'\n', '', cipher_text)
    cipher_text_processed: str = re.sub(r'[^a-zA-Z]', '', cipher_text.upper())
    return cipher_text_processed


def read_cipher_text(cipher_text: str) -> dict[str, float]:
    cipher_text_processed: str = clean_text(cipher_text)
    number_of_characters: Counter = Counter(cipher_text_processed)
    total_sum = sum(number_of_characters.values())
    res_percentage = {key: (value / total_sum) * 100 for key, value in number_of_characters.items()}
    return res_percentage


@app.route('/api/process-cipher-text', methods=['POST'])
@cross_origin()
def print_cipher_text() -> tuple[Response, int] | str:
    data = request.json
    if 'fileContent' not in data:
        return jsonify({"error": "No file content provided"}), 400

    cipher_text = data['fileContent']
    number_of_characters = read_cipher_text(cipher_text)
    # data_plot = Data_Plot(number_of_characters)
    # data_plot.plot_data()

    sorted_data: dict[str, float] = dict(sorted(number_of_characters.items(), key=lambda item: item[1], reverse=True))
    number_of_characters_json: str = json.dumps(sorted_data, indent=4)

    return number_of_characters_json


@app.route('/api/modify-letters', methods=['POST'])
@cross_origin()
def modify_letters() -> tuple[Response, int] | str:
    data = request.json
    if 'fileContent' not in data:
        return jsonify({"error": "No file content provided"}), 400

    cipher_text = data['fileContent']
    user_selection = data['userIntercept']
    deciphered_text = cipher_text.upper()
    print(user_selection)
    for key, value in user_selection.items():
        if value == '':
            continue
        deciphered_text: str = deciphered_text.replace(key.upper(), value.lower())
    return deciphered_text


@app.route('/api/find-graphs', methods=['POST'])
@cross_origin()
def find_graphs() -> tuple[Response, int] | str:
    data = request.json

    if 'fileContent' not in data:
        return jsonify({"error": "No file content provided"}), 400

    cipher_text = data['fileContent']
    cipher_text_processed: str = clean_text(cipher_text)
    count_letters = data['countLetters']
    offset = count_letters - 1
    graphs = [cipher_text_processed[i:i + count_letters] for i in range(0, len(cipher_text_processed) - offset)]
    graph_count = Counter(graphs)
    most_common_graphs = graph_count.most_common(data['countGraphs'])
    result = [{"graph": graph, "count": count} for graph, count in most_common_graphs]
    result_json = json.dumps(result, indent=4)
    print(result_json)
    return result_json
