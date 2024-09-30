# Laboratory Work nr.1
# Task: Caesar Cipher
# Student: Gusev Roman
# Group: FAF-222


def permute_alphabet(alphabet: list[str], shift_key: int) -> list[str]:
    permuted_alphabet: list[str] = []
    for i in range(len(alphabet)):
        if i + shift_key < len(alphabet) - 1:
            letter = alphabet[i + shift_key]
        else:
            letter = alphabet[(i + shift_key) % len(alphabet)]
        permuted_alphabet.insert(i, letter)
    return permuted_alphabet

def encrypt_single_key(message: str, shift_key: int, alphabet: list[str]) -> str:
    print("\nEncryption")
    print("Original message: ", message)
    print("Shift key: ", shift_key)
    print("Original Alphabet: ", alphabet)

    encrypted_message: str = ""
    encrypted_alphabet: list[str] = permute_alphabet(alphabet, shift_key)

    print("Encrypted alphabet: ", encrypted_alphabet)

    original_message_list: list[str] = list(message)
    for i in range(len(original_message_list)):
        if original_message_list[i] in alphabet:
            encrypted_message += encrypted_alphabet[alphabet.index(original_message_list[i])]
    return encrypted_message


def decrypt_single_key(encrypted_message: str, shift_key: int, alphabet: list[str]) -> str:
    print("\nDecryption")
    print("Encrypted message: ", encrypted_message)
    print("Shift key: ", shift_key)
    print("Original Alphabet: ", alphabet)

    decrypted_message: str = ""
    encrypted_alphabet: list[str] = permute_alphabet(alphabet, shift_key)

    print("Encrypted alphabet: ", encrypted_alphabet)

    encrypted_message_list: list[str] = list(encrypted_message)
    for i in range(len(encrypted_message_list)):
        if encrypted_message_list[i] in alphabet:
            decrypted_message += alphabet[encrypted_alphabet.index(encrypted_message_list[i])]
    return decrypted_message


def encrypt_double_key(message: str, shift_key_1: int, keyword_key_2: str, alphabet: list[str]) -> str:
    print("\nEncryption using double key")
    print("Original message: ", message)
    print("Shift key 1: ", shift_key_1)
    print("Keyword key 2: ", keyword_key_2)
    print("Original Alphabet: ", alphabet)

    encrypted_message: str = ""
    first_part: list[str] = list(("".join(sorted(set(keyword_key_2), key=keyword_key_2.index))).upper())
    second_part: list[str] = [letter for letter in alphabet if letter not in first_part]
    encrypted_alphabet: list[str] = first_part + second_part

    # permute_alphabet(encrypted_alphabet, shift_key_1)
    encrypted_alphabet = permute_alphabet(encrypted_alphabet, shift_key_1)

    print("Encrypted alphabet: ", encrypted_alphabet)

    original_message_list: list[str] = list(message)
    for i in range(len(original_message_list)):
        if original_message_list[i] in alphabet:
            encrypted_message += encrypted_alphabet[alphabet.index(original_message_list[i])]
    return encrypted_message

def decrypt_double_key(message: str, shift_key_1: int, keyword_key_2: str, alphabet: list[str]) -> str:
    print("\nDecryption using double key")
    print("Encrypted message: ", message)
    print("Shift key 1: ", shift_key_1)
    print("Keyword key 2: ", keyword_key_2)
    print("Original Alphabet: ", alphabet)

    decrypted_message: str = ""
    first_part: list[str] = list(("".join(sorted(set(keyword_key_2), key=keyword_key_2.index))).upper())
    second_part: list[str] = [letter for letter in alphabet if letter not in first_part]
    encrypted_alphabet: list[str] = first_part + second_part

    encrypted_alphabet = permute_alphabet(encrypted_alphabet, shift_key_1)


    print("Encrypted alphabet: ", encrypted_alphabet)

    original_message_list: list[str] = list(message)
    for i in range(len(original_message_list)):
        if original_message_list[i] in encrypted_alphabet:
            decrypted_message += alphabet[encrypted_alphabet.index(original_message_list[i])]
    return decrypted_message

english_alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alphabet_list: list[str] = list(english_alphabet)
shift_key: int = 0

print("Task: Caesar Cipher\n")
while True:
    print("Choose the Task:")
    print("1. Task 1.1 - Encrypt/Decrypt message using Caesar Cipher with single key")
    print("2. Task 1.2 - Encrypt/Decrypt message using Caesar Cipher with 2 keys")
    print("3. Exit")
    while True:
        user_input_task: str = input("Enter the number of the task: ")
        if user_input_task == "1":
            while True:
                print("Choose the subtask:\n"
                      "1. Task 1.1.1 - Encrypt message using Caesar Cipher with single key\n"
                      "2. Task 1.1.2 - Decrypt message using Caesar Cipher with single key\n"
                      "3. Exit")
                user_input_subtask: str = input("Enter the number of the subtask: ")
                if user_input_subtask == "1":
                    print("Task 1.1.1 - Encrypt message using Caesar Cipher with single key")
                    user_input_message: str = input("Enter the message: ")
                    while True:
                        user_input_key: str = input("Enter the shift/key: ")
                        try:
                            shift_key: int = int(user_input_key)
                            if shift_key < 0:
                                print("Shift key must be a positive number.")
                                raise ValueError
                            break
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    encrypted_message: str = encrypt_single_key(user_input_message.upper().replace(" ", ""), shift_key,
                                                                alphabet_list)
                    print("Encrypted message: ", encrypted_message)
                    decrypted_message: str = decrypt_single_key(encrypted_message, shift_key, alphabet_list)
                    print("Decrypted message: ", decrypted_message)
                elif user_input_subtask == "2":
                    print("Task 1.1.2 - Decrypt message using Caesar Cipher with single key")
                    user_input_message: str = input("Enter the message: ")
                    while True:
                        user_input_key: str = input("Enter the shift/key: ")
                        try:
                            shift_key: int = int(user_input_key)
                            if shift_key < 0:
                                print("Shift key must be a positive number.")
                                raise ValueError
                            break
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    decrypted_message: str = decrypt_single_key(user_input_message.upper().replace(" ", ""), shift_key,
                                                                alphabet_list)
                    print("Decrypted message: ", decrypted_message)
                elif user_input_subtask == "3":
                    break
            break
        elif user_input_task == "2":
            print("Task 1.2 - Encrypt/Decrypt message using Caesar Cipher with 2 keys")
            while True:
                print("Choose the subtask:\n"
                      "1. Task 1.2.1 - Encrypt message using Caesar Cipher with double key\n"
                      "2. Task 1.2.2 - Decrypt message using Caesar Cipher with double key\n"
                      "3. Exit")
                user_input_subtask: str = input("Enter the number of the subtask: ")
                if user_input_subtask == "1":
                    print("Task 1.1.1 - Encrypt message using Caesar Cipher with double key")
                    user_input_message: str = input("Enter the message: ")
                    while True:
                        user_input_key: str = input("Enter the shift/key: ")
                        try:
                            shift_key: int = int(user_input_key)
                            if shift_key < 0:
                                print("Shift key must be a positive number.")
                                raise ValueError
                            break
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    while True:
                        user_input_keyword: str = input("Enter the keyword: ")
                        if not user_input_keyword.isalpha():
                            print("Keyword must contain only letters.")
                        if len(user_input_keyword) < 7:
                            print("Keyword must contain at least 7 letters.")
                        if user_input_keyword == "":
                            print("Keyword must not be empty.")
                        if " " in user_input_keyword:
                            print("Keyword must not contain spaces.")
                        else:
                            break
                    encrypted_message: str = encrypt_double_key(user_input_message.upper().replace(" ", ""), shift_key, user_input_keyword,
                                                                alphabet_list)
                    print("Encrypted message: ", encrypted_message)
                    decrypted_message: str = decrypt_double_key(encrypted_message, shift_key, user_input_keyword, alphabet_list)
                    print("Decrypted message: ", decrypted_message)
                elif user_input_subtask == "2":
                    print("Task 1.1.2 - Decrypt message using Caesar Cipher with single key")
                    user_input_message: str = input("Enter the message: ")
                    while True:
                        user_input_key: str = input("Enter the shift/key: ")
                        try:
                            shift_key: int = int(user_input_key)
                            if shift_key < 0:
                                print("Shift key must be a positive number.")
                                raise ValueError
                            break
                        except ValueError:
                            print("Invalid input. Please enter a number.")
                    while True:
                        user_input_keyword: str = input("Enter the keyword: ")
                        if not user_input_keyword.isalpha():
                            print("Keyword must contain only letters.")
                        if len(user_input_keyword) < 7:
                            print("Keyword must contain at least 7 letters.")
                        if user_input_keyword == "":
                            print("Keyword must not be empty.")
                        if " " in user_input_keyword:
                            print("Keyword must not contain spaces.")
                        else:
                            break
                    decrypted_message: str = decrypt_double_key(user_input_message.upper().replace(" ", ""), shift_key, user_input_keyword,
                                                                alphabet_list)
                    print("Decrypted message: ", decrypted_message)
                elif user_input_subtask == "3":
                    break
            break
        elif user_input_task == "3":
            print("Exit")
            exit(0)
        else:
            print("Invalid input. Please enter a number.")
