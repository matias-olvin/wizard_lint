from typing import List


def obtain_sql_string_from_file_path() -> str:
    return "SELECT * FROM project.dataset.table"

def obtain_file_paths_from_directory() -> List[str]:
    return ["./sql_folder/dummy.sql"]

