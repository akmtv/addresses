import json
import re


with open('countries_alphas.json') as alphas:
    countries_alphas = json.load(alphas)


def get_alpha_code(row):
    if row[-1] in countries_alphas:
        country_code = countries_alphas[row.pop()]
        return country_code
    return None


def city_cleaner(row):
    if len(row) <= 1:
        return None
    city = row.pop()
    return re.sub(r'([0-9-]+\b)|([A-Z]+[0-9-]+\b)', '', city)