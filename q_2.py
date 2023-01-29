import group_representation
import util

if __name__ == '__main__':
    dir_path = "data/data1"
    jsons = util.load_jsons(dir_path)
    for json_data in jsons:
        user_data = util.extract_user(json_data)
        credibility_model.calc_user_weight(user_data)
