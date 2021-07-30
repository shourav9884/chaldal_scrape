import json
import time

import requests

import chaldal_cats
product_set = set()
def process_cats(cats):

    for cat in cats:
        cat['slug'] = cat['slug'].split('https://chaldal.com/')[1]
        if cat.get('has_child', False):
            process_cats(cat['children'])
    return cats
def process_response(cat, response):
    accepted_keys = ['bengaliName', 'longDesc', 'name', 'nameWithoutSubText', 'picturesUrls', 'price', 'corpPrice', 'objectID']
    products = []
    for hit in response.get('hits', []):
        p_dict = {}
        p_dict['category'] = cat
        for key in accepted_keys:
            p_dict[key] = hit.get(key, None)
        product_set.add(p_dict['objectID'])
        products.append(p_dict)
    return products

cat_set = set()

def get_products(cat):
    url = "https://catalog.chaldal.com/searchOld"
    body = {"apiKey": "e964fc2d51064efa97e94db7c64bf3d044279d4ed0ad4bdd9dce89fecc9156f0", "storeId": 1,
            "warehouseId": {"case": "None"}, "pageSize": 100, "currentPageIndex": 0, "metropolitanAreaId": 1,
            "query": "", "productVariantId": -1, "canSeeOutOfStock": "false", "filters": ["categories%3D{}".format(cat['id'])]}
    response = requests.post(url=url, json=body).json()
    response = process_response(cat, response)
    with open('jsons/{}__products.json'.format(cat['slug']), 'w+') as file:
        print(cat['slug'])
        cat_set.add(cat['slug'])
        json.dump(response, file, indent=4)
    # print(response)

# get_products({"id": "238"})
def get_all_products(cats):
    for cat in cats:
        if cat.get('has_child', False):
            get_all_products(cat['children'])
        else:
            get_products(cat)
now = time.time()
get_all_products(process_cats(chaldal_cats.cats))

print("Categories: {}".format(len(cat_set)))
print("Products: {}".format(len(product_set)))
delta = time.time() - now
print("Took {} seconds".format(delta))




