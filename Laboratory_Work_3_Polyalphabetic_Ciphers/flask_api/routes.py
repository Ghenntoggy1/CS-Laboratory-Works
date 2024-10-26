from flask import request, jsonify, Response, Blueprint

from constants import PERMITTED_CHARACTERS
from cipher_methods import validate_cipher_text, validate_key, encrypt_plain_text, decrypt_cipher_text

router = Blueprint("router", __name__)


@router.post("/api/encrypt")
def cipher() -> Response:
    request_data = request.json
    if not isinstance(request_data, dict):
        response: Response = jsonify({"message": "Invalid JSON format - should be a dictionary",
                                      "status_code": 400})
        response.status_code = 400
        return response

    raw_plain_text: str = request_data.get("plain_text")
    if raw_plain_text is None:
        response: Response = jsonify({"message": "No plain text provided",
                                      "status_code": 400})
        response.status_code = 400
        return response

    if not validate_cipher_text(raw_plain_text):
        response: Response = jsonify({"message": "Invalid characters",
                                      "permitted_characters": PERMITTED_CHARACTERS,
                                      "status_code": 400})
        response.status_code = 400
        return response

    key: str = request_data.get("key")
    if key is None:
        response: Response = jsonify({"message": "No key provided",
                                      "status_code": 400})
        response.status_code = 400
        return response

    if not validate_key(key):
        response: Response = jsonify({"message": "Invalid key length",
                                      "permitted_length": ">= 7",
                                      "status_code": 400})
        response.status_code = 400
        return response

    encrypted_text: str = encrypt_plain_text(raw_plain_text, key)
    response: Response = jsonify(
        {"message": "Successfully encrypted", "encrypted_text": encrypted_text, "status_code": 200})
    response.status_code = 200
    return response


@router.post("/api/decrypt")
def decipher() -> Response:
    request_data: dict = request.get_json()
    if not isinstance(request_data, dict):
        response: Response = jsonify({"message": "Invalid JSON format - should be a dictionary",
                                      "status_code": 400})
        response.status_code = 400
        return response

    raw_cipher_text: str = request_data.get("cipher_text")
    if raw_cipher_text is None:
        response: Response = jsonify({"message": "No cipher text provided",
                                      "status_code": 400})
        response.status_code = 400
        return response

    if not validate_cipher_text(raw_cipher_text):
        response: Response = jsonify({"message": "Invalid characters",
                                      "permitted_characters": PERMITTED_CHARACTERS,
                                      "status_code": 400})
        response.status_code = 400
        return response

    key: str = request_data.get("key")
    if key is None:
        response: Response = jsonify({"message": "No key provided",
                                      "status_code": 400})
        response.status_code = 400
        return response
    if not validate_key(key):
        response: Response = jsonify({"message": "Invalid key length",
                                      "permitted_length": ">= 7",
                                      "status_code": 400})
        response.status_code = 400
        return response

    decrypted_text: str = decrypt_cipher_text(raw_cipher_text, key)
    response: Response = jsonify(
        {"message": "Successfully decrypted", "decrypted_text": decrypted_text, "status_code": 200})
    response.status_code = 200
    return response
