import json
import re
import sys

all_countries = {}

try:
    with open('countries_alphas.json') as alphas:
        all_countries = json.load(alphas)
except (FileNotFoundError, ValueError) as err:
    sys.exit(f"JSON File not found or it has a wrong format")


def replace_to_alpha(row):
    for k, v in all_countries.items():
        if k in row:
            alpha = row.replace(k, v)
            return alpha
    return row


def get_country(row):
    if len(row[-1]) > 2:
        return None
    return row.pop()


def city_cleaner(data):
    if len(data) <= 1:
        return None
    keywords = ['University', 'Department', '@']
    for key in keywords:
        if key in data[-1]:
            return None
    for i in ['D.C.', 'D.F.', '']:
        if i == data[-1].strip():
            data.remove(i)
    city = data.pop()
    regex = re.sub(r'\b[A-Z\d\s]*\d[A-Z\d\s]*\b', '', city)
    second_regex = re.sub(r'(D.C.)|(D.F.)|(D.C)|(D.F)', '', regex)
    return second_regex.replace('-', '').strip()
