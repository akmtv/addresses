import numpy as np
import pandas as pd
import re


from utils import *


def clean_data(row):
    alpha_replacer = replace_to_alpha(row)
    data = [i.strip() for i in alpha_replacer.split(',')]
    country_code = get_country(data)
    if country_code in data:
        data.remove(country_code)
    city = city_cleaner(data)
    place = data.pop() if data else None
    other = "".join(data) if data else None
    return np.array([other, place, city, country_code], dtype=object)


def proccess_data(data):
    data['address'] = data['address'].str.replace(';', ',')
    data[['other','place', 'city', 'country']] = data.apply(
        lambda row: clean_data(row[0]), result_type='expand', axis=1
    )
    return data


def main():
    chunk_list = []
    addresses = pd.read_csv('data/addresses.csv', chunksize=10000)

    for chunk in addresses:
        data = proccess_data(chunk)
        chunk_list.append(data)

    dataframe = pd.concat(chunk_list)
    dataframe.drop_duplicates()
    
    dataframe = dataframe.drop(['address'], axis=1)
    dataframe.drop_duplicates(subset=['place', 'city', 'country'], inplace=True)
    dataframe.drop_duplicates(subset=['place', 'city'], inplace=True)
    dataframe.drop_duplicates(subset=['place', 'country'], inplace=True)
    dataframe.drop_duplicates(subset=['place', 'other'], inplace=True)
    dataframe.drop_duplicates(subset=['place'], inplace=True)
    dataframe = dataframe.drop(['other'], axis=1)

    dataframe.to_csv('results.csv', index=False)
    

if __name__ == '__main__':
    main()