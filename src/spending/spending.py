#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import logging
import matplotlib.pyplot as plt

def get_categories(data):
    filter_data = data.drop_duplicates(subset=['category'])
    return filter_data['category']

def calculate_sum(data, category):
    filter_data = data[(data["category"] == f"{category}")]
    logging.debug(filter_data)
    return filter_data["value"].sum()

def calculate_categories_sum(file_name):
    raw_data = pd.read_csv(file_name)
    categories = get_categories(raw_data)

    sum_data = pd.DataFrame({"value":[]})

    for category in categories:
        sum_cons = calculate_sum(raw_data, category)
        sum_data.loc[f"{category}"] = {"value":sum_cons}

    return sum_data


def main():
    file_name : str = "2023_12.csv"

    data = calculate_categories_sum(file_name)
    print(data)
    axes = data.plot(y="value", kind='bar')
    axes.set_xlabel("categories")
    axes.set_ylabel("spending [PLN]")
    axes.grid(visible=True,  linestyle='-', which="major", axis="y")
    plt.show()
    return 0

if __name__ == "__main__":
    main()