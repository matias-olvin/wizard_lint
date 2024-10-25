from typing import List



def obtain_sql_string_from_file_path(path: str) -> str:

    with open(path, 'r') as file:
        sql_string = file.read()

        return sql_string

def obtain_file_paths_from_directory() -> List[str]:
    return ["./sql_folder/dummy.sql"]

