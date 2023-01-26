import credibility_model
import util

if __name__ == '__main__':
    dir_path = "data"
    jsons = util.load_jsons(dir_path)
    for json_data in jsons:
        credibility_model.cal_user_weight(json_data["user"])
