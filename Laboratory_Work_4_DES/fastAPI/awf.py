from Laboratory_Work_4_DES.fastAPI.constants import PC_1, IP, PC_2
from Laboratory_Work_4_DES.fastAPI.main import initial_permutation_key, split_key, compile_keys, permute_key, \
    permute_message, split_message

plain_text: str = "0123456789ABCDEF"
plain_text: str = "0123456789ABCDEF"
print(f"Received Message: {plain_text}")
key: str = "133457799BBCDFF1"
print(f"Received Key: {key}")

binary_string = bin(int(plain_text, 16))[2:].zfill(len(plain_text) * 4)
print(f"Convert Message from Hexadecimal to Binary : {binary_string}")

binary_key = bin(int(key, 16))[2:].zfill(len(key) * 4)
print(f"Convert Key from Hexadecimal to Binary : {binary_key}")

L, R = split_message(binary_string)
print(f"Split Message into L and R : {L}, {R}")

permuted_key: str = initial_permutation_key(binary_key)
print(f"Initial Permutation of Key : {permuted_key}")
print(f"PC-1 :\n{PC_1}")

C_0, D_0 = split_key(permuted_key)
print(f"Split Key into C_0 and D_0 : {C_0}, {D_0}")

keys: list[str] = compile_keys(C_0, D_0, 16)
print(f"Compile Keys :\n{"\n".join(f"Key {key_nr} : {key}" for key_nr, key in enumerate(keys, start=1))}")

permuted_keys: list[str] = [permute_key(key) for key in keys]
print(f"Permuted Keys :\n{"\n".join(f"Key {key_nr} : {key}" for key_nr, key in enumerate(keys, start=1))}")
print(f"PC-2 :\n{PC_2}")

permuted_message: str = permute_message(binary_string)
print(f"Initial Permutation of Message : {permuted_message}")
print(f"IP :\n{IP}")

L_0, R_0 = split_message(permuted_message)
print(f"Split Permuted Message into L_0 and R_0 : {L_0}, {R_0}")