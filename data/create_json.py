import pandas as pd
import os
import json
import random

path_food = './food'
path_sport = './sport'
all_files_food = os.listdir(path_food)
all_files_sport = os.listdir(path_sport)

offer_type_to_int = {'STANDARD': 0, 'SPECIAL_CREDIT': 1}


def create_json(path):
    data = pd.read_excel(os.path.join(path, 'data_cleaned.xls'))
    meta = pd.read_excel(os.path.join(path, 'meta.xls'))
    for _, row in data.iterrows():
        for _, row_meta in meta.iterrows():
            new_json = {
                'Item': str(row[0]).lower(),
                'Attributes': '' if row[1] != row[1] else row[1].lower(),
                'Price': int(row[2]),
                
                'Offer': row_meta[0],
                'Web': row_meta[1],
                'Cashback': 0 if row_meta[2] != row_meta[2] else int(row_meta[2]),
                'Period': 0 if row_meta[3] != row_meta[3] else int(row_meta[3]),
                'Offer_type': offer_type_to_int[row_meta[4]],
                'Advert_text': '' if row_meta[5] != row_meta[5] else row_meta[5].lower()
            }
            all_json.append(new_json)


all_json = []
for directory in all_files_food:
    if os.path.isdir(os.path.join(path_food, directory)):
        create_json(os.path.join(path_food, directory))
for directory in all_files_sport:
    if os.path.isdir(os.path.join(path_sport, directory)):
        create_json(os.path.join(path_sport, directory))


with open('../resources/ranking/preset.json', 'w', encoding='utf-8') as fout:
    json.dump(all_json, fout)


random.seed(1)
all_json_small = [f for f in all_json if random.random() < 0.1]
with open('../resources/ranking/preset_small.json', 'w', encoding='utf-8') as fout:
    json.dump(all_json_small, fout)