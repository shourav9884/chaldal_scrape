import json

cats = []

def get_categories_from_json():
    with open('jsons/categories.json', 'r') as file:
        return json.load(file)

cats = get_categories_from_json()
