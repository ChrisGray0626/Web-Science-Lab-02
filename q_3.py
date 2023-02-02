import numpy as np

import util
import group_representation


# TODO Separate calc and load
def calc_weight(lines):
    token_weights = {}
    total_word_num = 0
    for i, line in enumerate(lines[1:]):
        line = (line.split(",", 1)[1])
        words = []
        word = ""
        for j in range(len(line) - 1):
            if line[j] == '\"':
                j += 1
                while line[j] != '\"':
                    word = word + line[j]
                    j += 1
                words.append(word)
                word = ""
        while '' in words:
            words.remove('')
        while '[' in words:
            words.remove('[')
        while ']' in words:
            words.remove(']')
        while ',' in words:
            words.remove(',')

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


if __name__ == '__main__':
    HQ_file_path = "data/data2/hqfile.csv"
    HQ_data = util.load_txt(HQ_file_path)
    HQ_token_weights, tfthq = calc_weight(HQ_data)
    LQ_file_path = "data/data2/lqfile.csv"
    LQ_data = util.load_txt(LQ_file_path)
    LQ_token_weights, tftlq = calc_weight(LQ_data)
    BG_file_path = "data/data2/bgfile.csv"
    BG_data = util.load_txt(BG_file_path)
    BG_token_weights, tftbg = calc_weight(BG_data)
    SHQ = calc_ratio(HQ_token_weights, tfthq, BG_token_weights, tftbg)
    SLQ = calc_ratio(LQ_token_weights, tftlq, BG_token_weights, tftbg)

    data_dir_path = "data/data1"
    jsons = util.load_jsons(data_dir_path)
    texts = []
    ids = []
    for json_data in jsons:
        text = util.extract_text(json_data)
        id = util.extract_id(json_data)
        texts.append(text)
        ids = util.extract_id(json_data)
    # Load stop words
    stop_word_file_path = "data/stopwordFile.txt"
    stop_words = util.load_txt(stop_word_file_path)
    for i, text in enumerate(texts):
        # Clean text
        text = group_representation.clean_text(text)
        # Split text into tokens
        raw_tokens = text.split(" ")
        news_score = 0
        Sigma_SHQt = 1
        Sigma_SLQt = 1
        # Clean tokens
        for raw_token in raw_tokens:
            token = group_representation.clean_token(raw_token, stop_words)
            if token is not None:
                if token in SHQ:
                    Sigma_SHQt += SHQ[token]
                if token in SLQ:
                    Sigma_SLQt += SLQ[token]
        news_score = np.log2(Sigma_SHQt / Sigma_SLQt)
        print("Newsworthiness for tweet " + ids[i] + ": " + str(news_score))
