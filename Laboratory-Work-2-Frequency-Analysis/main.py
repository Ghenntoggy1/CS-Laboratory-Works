import json
import re
from collections import Counter
import matplotlib.pyplot as plt


def plot_data(data: dict[str, int]) -> None:
    letters: list[str] = list(data.keys())
    frequencies: list[int] = list(data.values())
    plt.figure(figsize=(10, 5))
    plt.bar(letters, frequencies)
    plt.xlabel('Letters')
    plt.ylabel('Frequency')
    plt.title('Frequency of Letters in Cipher Text')
    plt.show()


if __name__ == '__main__':
    cipher_text_file = open('cipher-text.txt', 'r')
    cipher_text: str = cipher_text_file.read()
    cipher_text: str = re.sub(r'\n', '', cipher_text)
    cipher_text_file.close()
    cipher_text_processed: str = re.sub(r'[^a-zA-Z]', '', cipher_text.lower())
    print('Cipher text:\n', cipher_text)
    number_of_characters: Counter = Counter(cipher_text_processed)

    sorted_data: dict[str, int] = dict(sorted(number_of_characters.items(), key=lambda item: item[1], reverse=True))
    number_of_characters_json: str = json.dumps(sorted_data, indent=4)

    print('Serialized JSON:\n', number_of_characters_json)

    with open('character_counts.json', 'w') as json_file:
        json_file.write(number_of_characters_json)

    plot_data(number_of_characters)

