import re
from typing import Dict, List


def obtain_table_strings(sql_string: str) -> List[str]:

    pattern = (
        r"\`((?:\{\{.*?\}\}|[\w-]+)\.(?:\{\{.*?\}\}|[\w-]+)\.(?:\{\{.*?\}\}|[\w-]+))\`"
    )
    tables = re.findall(pattern, sql_string)

    return tables


def render_table_string(config: Dict[str, str], table_string: str) -> str:

    flipped_config = dict()

    for k, v in config.items():
        try:
            flipped_config[v] = k
        except TypeError:
            continue

    split_table_string = table_string.split(".")

    if table_string.startswith("{{ var.value."):
        project = ".".join(split_table_string[:-2])
        dataset, table = split_table_string[-2:]
    else:
        project, dataset, table = split_table_string

    if dataset.startswith("{{ params["):
        rendered_dataset = dataset
    else:
        rendered_dataset = "{{ params['" + flipped_config[dataset] + "'] }}"

    if table.startswith("{{ params["):
        rendered_table = table
    else:
        rendered_table = "{{ params['" + flipped_config[table] + "'] }}"

    rendered_string = f"{project}.{rendered_dataset}.{rendered_table}"

    return rendered_string


def render_sql_string_with_mapping_dict(sql_string, mapping: Dict[str, str]) -> str:

    for key, value in mapping.items():
        sql_string = sql_string.replace(key, value)

    return sql_string


def overwrite_sql_file_with_rendered_sql_string(
    path: str, rendered_sql_string: str
) -> None:
    with open(path, "w") as file:
        file.write(rendered_sql_string)
