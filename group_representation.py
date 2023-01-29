import math
import string

import util


def calc_representation(texts):
    # Load stop words
    stop_word_file_path = "data/stopwordFile.txt"
    stop_words = util.load_txt(stop_word_file_path)
    # Calculate token weights
    token_weights = {}
    for i, text in enumerate(texts):
        # Clean text
        text = clean_text(text)
        # Split text into tokens
        raw_tokens = text.split(" ")
        tokens = []
        # Clean tokens
        for raw_token in raw_tokens:
            token = clean_token(raw_token, stop_words)
            if token is not None:
                tokens.append(token)
        # Update token weights
        token_weights |= calc_token_weights(tokens, token_weights, i)
    return token_weights


def clean_text(text):
    for ch in text:
        if f"'{ch}'" == ascii(ch):
            pass
        else:
            text = text.replace(ch, " ")
    # Remove blank break
    text = text.replace('\n', " ")
    return text


def clean_token(token, stop_words):
    # Remove NULL
    if len(token) == 0:
        return None
    # Exclude #, @, $
    if token.startswith('#') or token.startswith('@') or token.startswith('$'):
        token = token.replace(":", "")
        token = token.replace(".", "")
        token = token.replace(",", "")
        return token
    # Remove URL
    if token.startswith('http') or token.startswith('&amp'):
        return None
    # Remove punctuation
    exclude = set(string.punctuation)
    token = ''.join(ch for ch in token if ch not in exclude)
    # Remove stop words
    if token.lower() in stop_words:
        return None

    return token


def calc_token_weights(tokens, token_weights, i):
    tokens = set(tokens)
    token_count = len(tokens)
    for token in tokens:
        if token not in token_weights:
            token_weights[token] = 1 / math.sqrt(token_count) / (i + 2)
        else:
            token_weights[token] *= (i + 1) / (i + 2)
            token_weights[token] += 1 / math.sqrt(token_count) / (i + 2)
    # Normalize weights
    magnitude = 0
    for value in token_weights.values():
        magnitude += value ** 2
    magnitude = math.sqrt(magnitude)
    for key in token_weights.keys():
        token_weights[key] /= magnitude

    return token_weights
