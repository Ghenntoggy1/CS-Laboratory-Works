from Laboratory_Work_4_DES.fastAPI.constants import PC_1, IP, PC_2, E_BIT_SELECTION, IP_INVERSE
from Laboratory_Work_4_DES.fastAPI.main import initial_permutation_key, split_key, compile_keys, permute_key, \
    permute_message, split_message, function_f, compile_message_portions

print("STEP 0: PREREQUISITES")
plain_text: str = "0123456789ABCDEF"
print(f"Received Message: {plain_text}")
key: str = "133457799BBCDFF1"
print(f"Received Key: {key}")

print("STEP 1: CONVERT HEXADECIMAL TO BINARY")
binary_string = bin(int(plain_text, 16))[2:].zfill(len(plain_text) * 4)
print(f"Convert Message from Hexadecimal to Binary : {binary_string}")
binary_key = bin(int(key, 16))[2:].zfill(len(key) * 4)
print(f"Convert Key from Hexadecimal to Binary : {binary_key}")

print("STEP 2: SPLIT MESSAGE")
L, R = split_message(binary_string)
print(f"Split Message into L and R : {L}, {R}")

print("STEP 3: INITIAL PERMUTATION OF KEY")
permuted_key: str = initial_permutation_key(binary_key)
print(f"Initial Permutation of Key : {permuted_key}")
print(f"PC-1 :\n{PC_1}")

print("STEP 4: SPLIT KEY")
C_0, D_0 = split_key(permuted_key)
print(f"Split Key into C_0 and D_0 : {C_0}, {D_0}")

print("STEP 5: COMPILE ROUND KEYS")
permuted_keys: list[str] = compile_keys(C_0, D_0, 16)
# print(f"Compile Keys :\n{"\n".join(f"Key {key_nr} : {key}" for key_nr, key in enumerate(permuted_keys, start=1))}")

# print("STEP 6: PERMUTE KEYS")
# permuted_keys: list[str] = [permute_key(key) for key in keys]
# print(f"Permuted Keys :\n{"\n".join(f"Key {key_nr} : {key}" for key_nr, key in enumerate(permuted_keys, start=1))}")
# print(f"PC-2 :\n{PC_2}")

print("STEP 7: INITIAL PERMUTATION OF MESSAGE")
permuted_message: str = permute_message(binary_string, IP)
print(f"Initial Permutation of Message : {permuted_message}")
print(f"IP :\n{IP}")

print("STEP 8: SPLIT MESSAGE")
L_0, R_0 = split_message(permuted_message)
print(f"Split Permuted Message into L_0 and R_0 : {L_0}, {R_0}")
expanded_R = permute_message(R_0, E_BIT_SELECTION)

print("STEP 9: EXPAND R_0")
print(f"Expanded R_0 : {expanded_R}")
print(f"E-Bit Selection :\n{E_BIT_SELECTION}")

# print("STEP 10: FUNCTION F")
# print(f"f(R_(n-1), K_n) = {function_f(R_0, permuted_keys[0])}")

print("STEP 10: COMPILE MESSAGE PORTIONS")
messages_list = compile_message_portions(L_0, R_0, permuted_keys, 16)

print(f"Message Portions:\n{"\n".join(f"L_{message_nr} : {L}, R_{message_nr} : {R}" for message_nr, (L, R) in enumerate(messages_list, start=1))}")

print("STEP 11: REVERSE MESSAGE")
L_16, R_16 = messages_list[-1]
reversed_message = R_16 + L_16
print(f"Reversed Message : {reversed_message}")

print("STEP 12: FINAL PERMUTATION")
final_permutation = permute_message(reversed_message, IP_INVERSE)
print(f"Final Permutation : {final_permutation}")
print(f"IP-1 :\n{IP_INVERSE}")

print("STEP 13: CONVERT BINARY TO HEXADECIMAL")
hexadecimal_string = hex(int(final_permutation, 2))[2:].upper()
print(f"Convert Message from Binary to Hexadecimal : {hexadecimal_string}")