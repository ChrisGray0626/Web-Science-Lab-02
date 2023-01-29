import json
import os


def load_jsons(dir_path):
    jsons = []
    for file in os.listdir(dir_path):
        if file.endswith(".json"):
            jsons.append(json.load(open(os.path.join(dir_path, file), encoding='UTF-8')))
    return jsons


def load_txt(file_path):
    lines = []
    with open(file_path, 'r', encoding='UTF-8') as f:
        for line in f.readlines():
            # Remove blank space
            if '\n' == line:
                continue
            # Remove line break
            line = line.strip('\n')
            lines.append(line)

    return lines


def extract_text(json_data):
    truncated = json_data["truncated"]
    if truncated:
        text = json_data["extended_tweet"]["full_text"]
    else:
        text = json_data["text"]

    return text


def extract_user(json_data):
    user = json_data["user"]

    return user
