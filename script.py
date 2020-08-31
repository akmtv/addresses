import pandas as pd
import re

from utils import get_alpha_code, city_cleaner


def prepare_data(data):
    # remove exactly the same rows
    data = data.drop_duplicates()  
    # in some cases there is ; symbol insted of comma, so
    data['address'] = data['address'].str.replace(';', ',').str.split(',')
    # remove any whitespaces
    data['address'] = data['address'].apply(lambda row: list(map(str.strip, row)))
    return data


def clean(data):
    # Make Country column replacing name by alpha2 code
    data['Country'] = data['address'].apply(lambda row: get_alpha_code(row))
    # Make City column without address codes
    data['City'] = data['address'].apply(lambda row: city_cleaner(row))
    # Make Address column 
    data['Address'] = data['address'].apply(lambda row: row.pop())
    # Join other stuff to Additional column
    data['Additional'] = data['address'].str.join(',')

    data = data.drop(['address'], axis=1)
    data = data.drop_duplicates(subset=['Address'])
    data = data.drop_duplicates(subset=['Additional'])
    return data



def main():
    addresses = pd.read_csv('data/addresses.csv')
    data = prepare_data(addresses)
    cleaned_data = clean(data)
    cleaned_data.to_csv('final.csv', index=False)
    


if __name__ == '__main__':
    main()