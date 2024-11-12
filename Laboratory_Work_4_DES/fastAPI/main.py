import numpy
import numpy as np
from fastapi import FastAPI, status
from numpy.ma.core import right_shift
from pydantic import BaseModel
from numpy import mod

from Laboratory_Work_4_DES.fastAPI.constants import list_of_S_BOXES, P_BOX, IP_INVERSE, S1_BOX
from constants import PC_1, PC_2, IP, E_BIT_SELECTION

app = FastAPI()

class RequestBody(BaseModel):
    message: str
    key: str

class Response(BaseModel):
    content: dict
    status_code: int

@app.get("/api/encrypt",
         response_model=Response,
         status_code=status.HTTP_200_OK
         )
def encrypt(request_body: RequestBody):
    if request_body.message == "" or request_body.key == "":
        return Response(
            content={"message": "Message or key is empty"},
            status_code=status.HTTP_400_BAD_REQUEST
            )
    plain_text: str = request_body.message
    print(f"Received Message: {plain_text}")
    key: str = request_body.key
    print(f"Received Key: {key}")

    binary_string = bin(int(plain_text, 16))[2:].zfill(len(plain_text) * 4)
    print(f"Convert Message from Hexadecimal to Binary : {binary_string}")

    L, R = split_message(binary_string)
    print(f"Split Message into L and R : {L}, {R}")

    permuted_key: str = initial_permutation_key(key)
    print(f"Initial Permutation of Key : {permuted_key}")
    print(f"PC_1 : {PC_1}")

    C_0, D_0 = split_key(permuted_key)
    print(f"Split Key into C_0 and D_0 : {C_0}, {D_0}")

    permuted_keys: list[str] = compile_keys(C_0, D_0, 16)

    permuted_message: str = permute_message(binary_string, IP)
    print(f"Initial Permutation of Message : {permuted_message}")

    L_0, R_0 = split_message(permuted_message)
    print(f"Split Message into L_0 and R_0 : {L_0}, {R_0}")

    expanded_R = permute_message(R_0, E_BIT_SELECTION)
    print(f"Permuted R_0 : {expanded_R}")
    print(f"E-Bit Selection :\n{E_BIT_SELECTION}")

    messages_list = compile_message_portions(L_0, R_0, permuted_keys, 16)
    print(f"Messages List : {"\n".join(f"Key {message_nr} : {message}" for message_nr, message in enumerate(messages_list, start=1))}")

    L_16, R_16 = messages_list[-1]
    reversed_message = R_16 + L_16
    print(f"Reversed Message : {reversed_message}")

    final_permutation = permute_message(reversed_message, IP_INVERSE)
    print(f"Final Permutation : {final_permutation}")
    print(f"IP-1 :\n{IP_INVERSE}")

    hexadecimal_string = hex(int(final_permutation, 2))[2:].upper()
    print(f"Convert Message from Binary to Hexadecimal : {hexadecimal_string}")

    return Response(
        content={"message": "Encryption Successful",
                 "encrypted_message": hexadecimal_string,
                 "status_code": status.HTTP_200_OK},
        status_code=status.HTTP_200_OK
    )

def compile_message_portions(L_0: str, R_0: str, permuted_keys: list[str], round: int = 16) -> list[tuple[str, str]]:
    message_portions: list[tuple[str, str]] = [(L_0, R_0)]
    round = min(max(round, 1), 16)
    for i in range(0, round):
        K_i = permuted_keys[i]
        L_i = R_0
        R_i = bin(int(L_0, 2) ^ int(function_f(R_0, K_i), 2))[2:].zfill(len(L_0))
        L_0, R_0 = L_i, R_i
        message_portions.append((L_i, R_i))

    return message_portions[1:]

def S_BOX_R(R_0: str, K_1: str) -> str:
    S_BOXED_R: str = ""

    expanded_R_0 = permute_message(R_0, E_BIT_SELECTION)
    print(f"Expanded R_0 : {expanded_R_0}")
    print(f"E-Bit Selection :\n{E_BIT_SELECTION}")

    expanded_XORed_R_0 = bin(int(expanded_R_0, 2) ^ int(K_1, 2))[2:].zfill(len(expanded_R_0))
    print(f"R_0 XOR K_1 = {expanded_XORed_R_0}")
    for block_nr, block_length in enumerate(range(0, len(expanded_XORed_R_0), 6), start=0):
        block = expanded_XORed_R_0[block_length:block_length + 6]
        print(f"Block {block_nr + 1} : {block}")
        row = int(block[0] + block[-1], 2)
        column = int(block[1:-1], 2)
        print(f"Row : {row}, Column : {column}")
        print(f"S{block_nr + 1}-Box :\n{list_of_S_BOXES[block_nr]}")
        print(f"S{block_nr + 1}-Box Value : {list_of_S_BOXES[block_nr][row][column]}")
        S_BOXED_R += bin(list_of_S_BOXES[block_nr][row][column])[2:].zfill(4)
    print(f"S-Boxed R : {S_BOXED_R}")
    return S_BOXED_R

def function_f(R_0: str, K_1: str) -> str:
    S_BOXED_R: str = S_BOX_R(R_0, K_1)
    permuted_S_BOXED_R = permute_message(S_BOXED_R, P_BOX)
    print(f"Result R : {permuted_S_BOXED_R}")
    print(f"P-Box :\n{P_BOX}")

    return permuted_S_BOXED_R

def compile_keys(C_0: str, D_0: str, round: int = 16, is_left_shift: bool = True) -> list[str]:
    keys: list[str] = [C_0+D_0]
    round = min(max(round, 1), 16)

    if is_left_shift:
        for i in range(0, round):
            left_shift = 1 if i + 1 in [1, 2, 9, 16] else 2
            C_i = C_0[left_shift:] + C_0[:left_shift]
            D_i = D_0[left_shift:] + D_0[:left_shift]
            C_0, D_0 = C_i, D_i
            keys.append(C_i + D_i)
    else:
        for i in range(0, round):
            if i == 0:
                keys.append(C_0 + D_0)
                continue
            # TODO: Check if right shift is correct
            right_shift = 1 if i + 1 in [2, 9, 16] else 2
            C_i = C_0[-right_shift:] + C_0[:-right_shift]
            # C_i = C_0[:right_shift] + C_0[right_shift:]
            D_i = D_0[-right_shift:] + D_0[:-right_shift]
            # D_i = D_0[:right_shift] + D_0[right_shift:]
            C_0, D_0 = C_i, D_i
            keys.append(C_i + D_i)
    permuted_keys: list[str] = [permute_key(key) for key in keys[1:]]
    print(f"Round Keys :\n{"\n".join(f"Key {key_nr} : {key}" for key_nr, key in enumerate(permuted_keys, start=1))}")
    return permuted_keys

def split_message(message: str) -> tuple[str, str]:
    return message[:len(message) // 2], message[len(message) // 2:]

def initial_permutation_key(key: str) -> str:
    # Permute using PC-1 Table, and remove parity bits
    permuted_key: str = "".join([key[index - 1] for index in PC_1.flatten() if mod(index, 8) != 0])
    return permuted_key

def permute_key(key: str) -> str:
    return "".join([key[index - 1] for index in PC_2.flatten()])

def split_key(key: str) -> tuple[str, str]:
    return key[:len(key) // 2], key[len(key) // 2:]

def permute_message(message: str, table: np.array) -> str:
    return "".join([message[index - 1] for index in table.flatten()])