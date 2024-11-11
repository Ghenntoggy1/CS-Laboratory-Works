import numpy
from fastapi import FastAPI, status
from pydantic import BaseModel
from numpy import mod

from constants import PC_1, PC_2


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
    key: str = request_body.key

    binary_string = bin(int(plain_text, 16))[2:].zfill(len(plain_text) * 4)
    L, R = split_message(binary_string)

    permuted_key: str = initial_permutation_key(key)
    C_0, D_0 = split_key(permuted_key)

    keys: list[str] = compile_keys(C_0, D_0, 16)

    permuted_keys: list[str] = [permute_key(key) for key in keys]


def compile_keys(C_0: str, D_0: str, round: int = 16) -> list[str]:
    keys: list[str] = [C_0+D_0]
    round = min(max(round, 1), 16)
    for i in range(0, round):
        left_shift = 1 if i + 1 in [1, 2, 9, 16] else 2
        C_i = C_0[left_shift:] + C_0[:left_shift]
        D_i = D_0[left_shift:] + D_0[:left_shift]
        C_0, D_0 = C_i, D_i
        keys.append(C_i + D_i)
    return keys[1:]

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