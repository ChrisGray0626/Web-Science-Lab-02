import math
import string
import numpy as np
import util


def extract_text(json_data):
    truncated = json_data["truncated"]
    if truncated:
        text = json_data["extended_tweet"]["full_text"]
    else:
        text = json_data["text"]

    return text


def clean_text(text):
    for ch in text:
        if f"'{ch}'" == ascii(ch):
            pass
        else:
            text = text.replace(ch, " ")

    return text


def clean_token(token):
    # Exclude #, @, $
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


def streaming():
    stop_word_file_path = "stopwordFile.txt"
    stop_words = util.load_txt(stop_word_file_path)
    dir_path = "data"
    jsons = util.load_jsons(dir_path)
    token_weights = {}
    for i, json_data in enumerate(jsons):
        text = extract_text(json_data)
        # Split text into tokens
        raw_tokens = text.split(" ")
        tokens = []
        for raw_token in raw_tokens:
            token = clean_token(raw_token)
            if token is None:
                continue
            # Remove stop words
            if token.lower() not in stop_words:
                tokens.append(token)
        tokens = set(tokens)
        token_sum = len(tokens)
        for token in tokens:
            if token not in token_weights:
                token_weights[token] = 1 / math.sqrt(token_sum) / (i + 2)
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
    return token_weights


if __name__ == '__main__':
    stream_weights = streaming()
