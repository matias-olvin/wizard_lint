from typing import List, Dict
import os
import yaml



def obtain_sql_string_from_file_path(path: str) -> str:

    with open(path, 'r') as file:
        sql_string = file.read()

        return sql_string

def obtain_file_paths_from_directory(path: str) -> List[str]:
    
    if os.path.isfile(path) and path.endswith(".sql"):
        return [path]
    
    file_paths = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith(".sql"):
                file_paths.append(os.path.join(root, file))

    return file_paths

def obtain_config_yaml(path: str) -> Dict[str, str]:
    with open(path, 'r') as file:
        config = yaml.safe_load(file)

    if not config:
        return {}

    return config
