#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import logging
import matplotlib.pyplot as plt
from argparse import ArgumentParser
from pathlib import Path
from loguru import logger
from enum import IntEnum
from typing import List

class ExitCode(IntEnum):
    """
    Exit code of scripts.
    """

    SUCCESS = 0
    FILE_NOT_EXISTS = 1


def parse_arguments():
    """
    Function used to parse arguments passed to script.
    """
    parser = ArgumentParser(
        prog="spending",
        description="Load spending from csv value, print grafical representation.",
    )
    parser.add_argument(
        "file_name",
        type=str,
        help="Path to csv file that stores spending input information.",
    )
    return parser.parse_args()


def calculate_sum(data, category):
    filter_data = data[(data["category"] == f"{category}")]
    logging.debug(filter_data)
    return filter_data["value"].sum()


def calculate_categories_sum(file_name):
    raw_data = pd.read_csv(file_name)
    categories = raw_data['category'].drop_duplicates().to_list()
    sum_data = pd.DataFrame({"value": []})

    for category in categories:
        sum_cons = calculate_sum(raw_data, category)
        sum_data.loc[f"{category}"] = {"value": sum_cons}
        
    sum_of_categories = sum_data["value"].sum()
    sum_data.loc["total"] = {"value": sum_of_categories}
    return sum_data


def main():
    args = parse_arguments()

    file_name: Path = Path(args.file_name)

    if not file_name.exists():
        logger.error(f"File '{file_name}' doesn't exist")
        exit(ExitCode.FILE_NOT_EXISTS)

    data = calculate_categories_sum(file_name)
    
    logger.info(f"data:\n{data}")
    axes = data.plot(y="value", kind="bar")
    axes.set_xlabel("categories")
    axes.set_ylabel("spending [PLN]")
    axes.grid(visible=True, linestyle="-", which="major", axis="y")
    
    for index, value in enumerate(data["value"]):
        plt.text(index - 0.5, value +10, f"{round(value, 2):>8}")
    
    plt.show()

    exit(ExitCode.SUCCESS)


if __name__ == "__main__":
    main()
