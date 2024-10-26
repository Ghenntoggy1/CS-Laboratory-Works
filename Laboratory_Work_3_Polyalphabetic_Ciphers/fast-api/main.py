from flask_cors import CORS, cross_origin
from flask import Flask, request, jsonify, Response
import json
import re
from collections import Counter

from Constants import PERMITTED_CHARACTERS, REGEX_PATTERN_VALIDATION, REGEX_PATTERN_SUBSTITUTION


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

cipher_text = "Acesta este un text de test pentru cifrul polialfabetic de tip Vigenere. Conține litere mari și mici, precum și cifre. În plus, conține și caractere speciale, cum ar fi: !@#$%^&*()_+-=[]{}|;':,.<>/?`~AĂÎBCDEFGHIÎJKLMNOPQRSȘTȚUVWXYZaăîbcdefghiîjklmnopqrsștțuvwxyz0123456789"


def validate_cipher_text(cipher_text: str) -> bool:
    if re.match(REGEX_PATTERN_VALIDATION, cipher_text):
        return True
    return False


def clean_cipher_text(cipher_text: str) -> str:
    return re.sub(REGEX_PATTERN_SUBSTITUTION, '', cipher_text).upper()


def validate_key(key: str) -> bool:
    return True if len(key) >= 7 else False


@app.post("/api/decipher")
@cross_origin()
def decipher(cipher_text: str) -> str:
    request_data = request

    return ""


@app.post("/api/cipher")
@cross_origin()
def cipher(plain_text: str) -> str:
    request_data = request

    return ""
