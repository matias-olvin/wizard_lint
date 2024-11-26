from typing import Dict, List, Set

from jinja2 import Template


def unrender_sql_string_using_jinja(config: Dict[str, str], sql_string: str) -> str:

    template = Template(sql_string)

    rendered_sql_string = template.render(config)

    return rendered_sql_string


def obtain_missing_params_in_table_strings(config: Dict[str, str], table_strings: List[str]) -> Set[str]:
    
    flipped_config = dict()

    for k, v in config.items():
        try:
            flipped_config[v] = k
        except TypeError:
            continue
    
    missing_params = set()

    for table_string in table_strings:

        split_table_string = table_string.split(".")

        if table_string.startswith("{{ var.value."):
            dataset, table = split_table_string[-2:]
        else:
            _, dataset, table = split_table_string

        if dataset not in flipped_config and not dataset.startswith("{{ params["):
            missing_params.add(dataset)

        if table not in flipped_config and not table.startswith("{{ params["):
            missing_params.add(table)

    return missing_params