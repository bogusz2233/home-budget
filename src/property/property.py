#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import pandas as pd

def get_types(data):
    filtered_data = data.drop_duplicates(subset=["type"])["type"]
    logging.debug(filtered_data)
    return filtered_data

def calculate_sum(data, type):
    filtered_data = data[(data["type"] == f"{type}")]
    logging.debug(filtered_data)
    return filtered_data["amount"].sum()

def calculate_types_sum(file_name : str):
    raw_data = pd.read_csv(file_name)
    types = get_types(raw_data)

    sum_data = pd.DataFrame({"amount":[]})

    for type in types:
        sum = calculate_sum(raw_data, type)
        sum_data.loc[f"{type}"] = {"amount":sum}
    
    return sum_data

def main():
    logging.basicConfig(level=logging.DEBUG)

    file_name : str = "2023_04_23.csv"
    data = calculate_types_sum(file_name)
    print(data)

    property_sum = data["amount"].sum()
    print(f"Property sum: {property_sum:0.2f} PLN")
    return 0

if __name__ == "__main__":
    main()