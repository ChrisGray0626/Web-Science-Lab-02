import numpy as np

import group_representation
import util


def calc_newsworthiness_score(HQ_texts, LQ_texts, BG_texts, data):
    HQ_token_weights, tfthq = calc_weight(HQ_texts)
    LQ_token_weights, tftlq = calc_weight(LQ_texts)
    BG_token_weights, tftbg = calc_weight(BG_texts)
    SHQ = calc_ratio(HQ_token_weights, tfthq, BG_token_weights, tftbg)
    SLQ = calc_ratio(LQ_token_weights, tftlq, BG_token_weights, tftbg)

    stop_word_file_path = "data/stopwordFile.txt"
    stop_words = util.load_txt(stop_word_file_path)
    scores = {}
    for id, text in data.items():
        # Clean text
        text = group_representation.clean_text(text)
        # Split text into tokens
        raw_tokens = text.split(" ")

        Sigma_SHQt = 1
        Sigma_SLQt = 1
        for raw_token in raw_tokens:
            # Clean tokens
            token = group_representation.clean_token(raw_token, stop_words)
            if token is not None:
                if token in SHQ:
                    Sigma_SHQt += SHQ[token]
                if token in SLQ:
                    Sigma_SLQt += SLQ[token]
        news_score = np.log2(Sigma_SHQt / Sigma_SLQt)
        scores[id] = news_score

    return scores


def parse_text(text):
    text = text.replace("[", "")
    text = text.replace("]", "")
    text = text.replace("\"", "")
    words = text.split(",")

    return words


def calc_weight(texts):
    token_weights = {}
    total_word_num = 0

    for text in texts:
        words = parse_text(text)

        for word in words:
            if word not in token_weights:
                token_weights[word] = 1
            else:
                token_weights[word] += 1

            total_word_num += 1

    return token_weights, total_word_num


def calc_ratio(dict1, ttl1, dict2, ttl2):
    res = {}
    keys_1 = list(dict1.keys())
    keys_2 = list(dict2.keys())
    keys_1.extend(keys_2)
    keys_res = list(set(keys_1))

    for token in keys_res:
        if token in dict1:
            tft1 = dict1[token] + 1
        else:
            tft1 = 1

        if token in dict2:
            tft2 = dict2[token] + 1
        else:
            tft2 = 1

        res[token] = tft1 / ttl1 / (tft2 / ttl2)

        if res[token] < 2:
            res[token] = 0

    return res
