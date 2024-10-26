import re

from constants import REGEX_PATTERN_VALIDATION, REGEX_PATTERN_SUBSTITUTION, ALPHABET, LENGTH_KEY


def validate_cipher_text(cipher_text: str) -> bool:
    if re.match(REGEX_PATTERN_VALIDATION, cipher_text):
        return True
    return False


def clean_cipher_text(cipher_text: str) -> str:
    return re.sub(REGEX_PATTERN_SUBSTITUTION, '', cipher_text).upper()


def validate_key(key: str) -> bool:
    return True if len(key) >= LENGTH_KEY else False


def encrypt_plain_text(plain_text: str, key: str) -> str:
    cleansed_plain_text: str = clean_cipher_text(plain_text)
    length_plain_text: int = len(cleansed_plain_text)
    length_key: int = len(key)
    encrypted_text: str = ""
    for letter_index in range(length_plain_text):
        # # Adjustment - encrypt with spaces
        # if cleansed_plain_text[letter_index] == ' ':
        #     encrypted_text += ' '

        # # Adjustment - encrypt both letters + digits
        # decrypted_text_char_index: int = ALPHABET_DIGITS.index(cleansed_plain_text[letter_index])
        # key_char_index: int = ALPHABET_DIGITS.index(key[letter_index % length_key].upper())
        # new_char_index: int = (decrypted_text_char_index + key_char_index) % len(ALPHABET_DIGITS)
        # encrypted_text += ALPHABET_DIGITS[new_char_index]

        if cleansed_plain_text[letter_index].isalpha():
            decrypted_text_char_index: int = ALPHABET.index(cleansed_plain_text[letter_index])
            key_char_index: int = ALPHABET.index(key[letter_index % length_key].upper())
            new_char_index: int = (decrypted_text_char_index + key_char_index) % len(ALPHABET)
            encrypted_text += ALPHABET[new_char_index]
        else:
            encrypted_text += cleansed_plain_text[letter_index]
    return encrypted_text


def decrypt_cipher_text(cipher_text: str, key: str) -> str:
    cleansed_cipher_test: str = clean_cipher_text(cipher_text)
    length_cipher_text: int = len(cleansed_cipher_test)
    length_key: int = len(key)
    decrypted_text: str = ""
    for letter_index in range(length_cipher_text):
        # # Adjustment - decrypt with spaces
        # if cleansed_cipher_test[letter_index] == ' ':
        #     decrypted_text += ' '

        # # Adjustment - decrypt both letters + digits
        # decrypted_text_char_index: int = ALPHABET_DIGITS.index(cleansed_cipher_test[letter_index])
        # key_char_index: int = ALPHABET_DIGITS.index(key[letter_index % length_key].upper())
        # new_char_index: int = (decrypted_text_char_index - key_char_index + len(ALPHABET_DIGITS)) % len(ALPHABET_DIGITS)
        # decrypted_text += ALPHABET_DIGITS[new_char_index]

        if cleansed_cipher_test[letter_index].isalpha():
            plain_text_char_index: int = ALPHABET.index(cleansed_cipher_test[letter_index])
            key_char_index: int = ALPHABET.index(key[letter_index % length_key].upper())
            new_char_index: int = (plain_text_char_index - key_char_index + len(ALPHABET)) % len(ALPHABET)
            decrypted_text += ALPHABET[new_char_index]
        else:
            decrypted_text += cleansed_cipher_test[letter_index]

    return decrypted_text