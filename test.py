import newsworthiness_score
import util

HQ_file_path = "data/data2/hqfile.csv"
data = util.load_csv(HQ_file_path)
texts = data.iloc[:, 1].values.tolist()
for text in texts:
    words = newsworthiness_score.parse_text(text)
    print(words)
    # print(text)
