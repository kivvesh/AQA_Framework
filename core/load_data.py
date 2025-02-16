import json
import csv


def load_json(path):
    with open(path, 'r', encoding='utf-8') as file:
        json_file = json.load(file)
    return json_file


def load_csv(path):
    with open(path, 'r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        list_obj = [obj for obj in csv_reader]
    return list_obj
