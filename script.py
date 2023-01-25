import util


def text_clean(text):
    # Remove ASCII
    for ch in text:
        if f"'{ch}'" == ascii(ch):
            pass
        else:
            text = text.replace(ch, " ")
    # Remove blank break
    text = text.replace('\n', "")

    return text


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

    raw_tokens = text.split(" ")
    tokens = []
    # Remove stop words
    for raw_token in raw_tokens:
        # Ignore case
        raw_token = raw_token.lower()
        if raw_token in stop_words:
            continue
        token = text_clean(raw_token)
        if token != raw_token:
            print("raw_token: ", raw_token)
            print("token: ", token)
        tokens.append(token)
