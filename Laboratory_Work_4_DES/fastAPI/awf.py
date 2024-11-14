from constants import PC_1, IP, E_BIT_SELECTION, IP_INVERSE, P_BOX
from main import initial_permutation_key, split_key, compile_keys, \
    permute_message, split_message, compile_message_portions, S_BOX_R

print("STEP 0: PREREQUISITES")
# 85E813540F0AB405
plain_text: str = "0123456789ABCDEF"
print(f"Received Message: {plain_text}")
key: str = "133457799BBCDFF1"
print(f"Received Key: {key}")

if len(plain_text) % 16 != 0:
    plain_text += "0" * (16 - len(plain_text) % 16)
print(f"Message Padded : {plain_text}")

final_cipher_text: str = ""
start: int = 0
while start + len(key) <= len(plain_text):
    portion: str = plain_text[start:start + len(key)]

    binary_string = bin(int(portion, 16))[2:].zfill(len(portion) * 4)
    print(f"Convert Message from Hexadecimal to Binary : {binary_string}")

    binary_key = bin(int(key, 16))[2:].zfill(len(key) * 4)
    print(f"Convert Key from Hexadecimal to Binary : {binary_key}")

    L, R = split_message(binary_string)
    print(f"Split Message into L and R : {L}, {R}")

    permuted_key: str = initial_permutation_key(binary_key)
    print(f"Initial Permutation of Key : {permuted_key}")
    print(f"PC_1 : {PC_1}")

    C_0, D_0 = split_key(permuted_key)
    print(f"Split Key into C_0 and D_0 : {C_0}, {D_0}")

    permuted_keys: list[str] = compile_keys(C_0, D_0, 16, is_left_shift=True)

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

    hexadecimal_string = hex(int(final_permutation, 2))[2:].upper().zfill(len(final_permutation) // 4)
    print(f"Convert Message from Binary to Hexadecimal : {hexadecimal_string}")
    final_cipher_text += hexadecimal_string
    start += len(key)

print(f"Final Cipher Text : {final_cipher_text}")


# TODO MY TASK:
# round_i = 16
# L_i_1 = messages_list[(round_i - 1) - 1][0]
# S_BOXED_R_i_1 = S_BOX_R(messages_list[(round_i - 1) - 1][1], permuted_keys[round_i - 1])
#
# print("L_i-1: ", L_i_1)
# print("f_i: ", S_BOXED_R_i_1)
# print("TRUE R_i: ", R_16)
#
# function_f_i = permute_message(S_BOXED_R_i_1, P_BOX)
# print("Permuted f_i: ", function_f_i)
#
# R_i = bin(int(L_i_1, 2) ^ int(function_f_i, 2))[2:].zfill(len(L_i_1))
# print("R_i: ", R_i)

