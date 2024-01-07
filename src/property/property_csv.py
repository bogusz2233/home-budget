#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import csv

def _read_csv_read(file_name :str) -> dict:
    csv_dic = []
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            csv_dic.append(row)
    return csv_dic

def __get_keys(csv_data):
    keys =[]
    for row in csv_data:
        row_keys = row.keys()
        for key in row_keys:
            keys.append(key)
    return list(dict.fromkeys(keys))

def _get_types(csv_data:dict) -> list:
    types = []
    for row in csv_data:
        types.append(row["type"])
    return list(dict.fromkeys(types))

def __calculate_sum(csv_data, type) -> int:
    filtered_list = []
    for row in csv_data:
        if row["type"] == type:
            filtered_list.append(float(row["amount"]))
    return sum(filtered_list)

def calculate_sum(file_name : str) -> dict:
    csv_dic = _read_csv_read(file_name)
    csv_types = _get_types(csv_dic)

    types_dic = {}
    for type in csv_types:
        sum = __calculate_sum(csv_dic, type)
        types_dic[type] = sum
    return types_dic

def main():
    file_name : str = "2023_07_08.csv"
    
    csv_dic = _read_csv_read(file_name)
    csv_types = _get_types(csv_dic)

    result = calculate_sum(file_name)
    print(result)
    return 0

if __name__ == "__main__":
    main()