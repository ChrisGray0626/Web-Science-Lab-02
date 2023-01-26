import math
import string
import numpy as np
import util


def text_clean(text):
    for ch in text:
        if f"'{ch}'" == ascii(ch):
            pass
        else:
            text = text.replace(ch, " ")

    return text


def token_clean(token):
    if token.startswith('#') or token.startswith('@') or token.startswith('$'):
        token = token.replace(":", "")
        token = token.replace(".", "")
        token = token.replace(",", "")
        return token
    # Remove URL
    if token.startswith('http') or token.startswith('&amp'):
        return None
    # Remove blank break
    token = token.replace('\n', "")
    # Remove punctuation
    exclude = set(string.punctuation)
    token = ''.join(ch for ch in token if ch not in exclude)
    # Remove NULL
    if len(token) == 0:
        return None

    return token


if __name__ == '__main__':
    stop_word_file_path = "stopwordFile.txt"
    stop_words = util.load_txt(stop_word_file_path)

    dir_path = "data"
    jsons = util.load_jsons(dir_path)
    token_weights = {}
    text_sum = len(jsons)
    for i, json_data in enumerate(jsons):
        truncated = json_data["truncated"]
        if truncated:
            text = json_data["extended_tweet"]["full_text"]
        else:
            text = json_data["text"]
        # print("text: ", json_data["id"], text)
        text = text_clean(text)

        raw_tokens = text.split(" ")
        tokens = []
        for raw_token in raw_tokens:
            token = token_clean(raw_token)
            if token is None:
                continue
            # Remove stop words
            if token.lower() not in stop_words:
                tokens.append(token)
        # print("tokens: ", tokens)
        # Assign weights to tokens
        tokens = set(tokens)
        token_sum = len(tokens)
        for token in tokens:
            if token not in token_weights:
                token_weights[token] = 1 / token_sum
            else:
                token_weights[token] *= (i + 1) / (i + 2)
                token_weights[token] += 1 / math.sqrt(token_sum) / (i + 2)
        # Normalize weights
        magnitude = 0
        for value in token_weights.values():
            magnitude += value ** 2
        magnitude = math.sqrt(magnitude)
        for key in token_weights.keys():
            token_weights[key] /= magnitude
    print("token_weights: ", token_weights)


