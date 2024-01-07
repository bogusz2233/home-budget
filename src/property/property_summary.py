#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import property_csv as property
import glob
import matplotlib.pyplot as plt

def _read_csv_data() -> dict:
    CSV_EXTENSTION : str = ".csv"
    files = glob.glob(f"*{CSV_EXTENSTION}")
    data = {}
    files = sorted(files)
    for file in files:
        summary = property.calculate_sum(file)
        name_file = file.removesuffix(CSV_EXTENSTION)
        data[name_file] = summary
    return data

def _category_points(data, name):
    x = []
    y = []
    for key, value in data.items():
        x.append(key)
        y.append(value[name])

    return x,y

def _sum_point(data, categories_list) :
    x = []
    y = []
    for key, value in data.items():
        x.append(key)
        values_list = []
        for category in categories_list:
            values_list.append(value[category])
        sum_all_properties=sum(values_list)
        y.append(sum_all_properties)
        print(f"{key}: {sum_all_properties:0.2f} PLN")
    
    return [x,y]

def main():
    data = _read_csv_data()
    fig, ax = plt.subplots(1)

    categories_list = ["cash", "saving account", "bonds", "deposit", "shares etf"]

    for category in categories_list:
        names, values = _category_points(data, category)
        ax.plot(names, values)

    name, values = _sum_point(data, categories_list)
    ax.plot(names, values, linewidth=3)
    ax.legend(categories_list + ["Sum"])
    ax.grid(visible=True)

    plt.savefig(fname = "summary.svg", format="svg")

if __name__ == "__main__":
    main()