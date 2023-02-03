import newsworthiness_score
import util


def extract_text(df):
    texts = df.iloc[:, 1].values.tolist()

    return texts


if __name__ == '__main__':
    HQ_file_path = "data/data2/hqfile.csv"
    HQ_texts = extract_text(util.load_csv(HQ_file_path))
    LQ_file_path = "data/data2/lqfile.csv"
    LQ_texts = extract_text(util.load_csv(LQ_file_path))
    BG_file_path = "data/data2/bgfile.csv"
    BG_texts = extract_text(util.load_csv(BG_file_path))
    data_dir_path = "data/data1"
    jsons = util.load_jsons(data_dir_path)
    data = {}
    for json_data in jsons:
        text = util.extract_text(json_data)
        id = util.extract_id(json_data)
        data[id] = text
    scores = newsworthiness_score.calc_newsworthiness_score(HQ_texts, LQ_texts, BG_texts, data)
    for id, score in scores.items():
        print("Newsworthiness for tweet", id, str(score))
