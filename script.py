import string

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
    for json_data in jsons:
        truncated = json_data["truncated"]
        if truncated:
            text = json_data["extended_tweet"]["full_text"]
        else:
            text = json_data["text"]
        print(text)
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
        print(tokens)
        break
