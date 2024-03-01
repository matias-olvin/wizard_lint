import argparse
import os
from typing import List

import yaml


def return_dict_from_config_yaml_path(file_path: str) -> dict:
    with open(file_path, "r") as file:
        return dict(yaml.safe_load(file))


def return_sql_string_from_path_list(file_path_list: List[str]) -> List[str]:

    sql_strings = list()

    for path in file_path_list:
        with open(path, "r") as file:
            sql_string = file.read()

        sql_strings.append(sql_string)

    return sql_strings


def return_sql_paths(file_path: str) -> List[str]:
    if file_path.endswith(".sql"):
        return [file_path]
    else:
        sql_files = []
        for root, _, files in os.walk(file_path):
            for file in files:
                if file.endswith(".sql"):
                    sql_files.append(os.path.join(root, file))
        return sql_files


def obtain_args() -> List[str]:
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description="Process two files or directories.")

    # Add positional arguments for the paths
    parser.add_argument(
        "file", metavar="file", type=str, help="Give folder/specific path to SQL file"
    )
    parser.add_argument("config", metavar="config", type=str, help="Path to config")

    # Parse the arguments
    args = parser.parse_args()

    # Print the provided paths
    print("File path provided by the user:", args.file)
    print("config.yaml path provided by the user:", args.config)

    return [args.file, args.config]
