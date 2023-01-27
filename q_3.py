import math
import string
import numpy as np
import util
import json


def weights_calc(file_path):
    lines = util.load_txt(file_path)
    token_weights = {}
    total_word_num = 0
    for i, line in enumerate(lines[1:]):
        line = (line.split(",", 1)[1])
        words = []
        word = ""
        for j in range(len(line)-1):
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


def ratio_calc(dict1, ttl1, dict2, ttl2):
    dict_res = {}
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
        dict_res[token] = tft1 / ttl1 / (tft2 / ttl2)
        if dict_res[token] < 2:
            dict_res[token] = 0
    return dict_res


if __name__ == '__main__':
    HQ_file_path = "./data2/hqfile.csv"
    HQ_token_weights, tfthq = weights_calc(HQ_file_path)
    LQ_file_path = "./data2/lqfile.csv"
    LQ_token_weights, tftlq = weights_calc(LQ_file_path)
    BG_file_path = "./data2/bgfile.csv"
    BG_token_weights, tftbg = weights_calc(BG_file_path)
    SHQ = ratio_calc(HQ_token_weights, tfthq, BG_token_weights, tftbg)
    SLQ = ratio_calc(LQ_token_weights, tftlq, BG_token_weights, tftbg)
