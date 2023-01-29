import group_representation
import util

if __name__ == '__main__':
    data_dir_path = "data/data1"
    jsons = util.load_jsons(data_dir_path)
    texts = []
    for json_data in jsons:
        text = util.extract_text(json_data)
        texts.append(text)
    token_weights = group_representation.calc_representation(texts)
    print(token_weights)
