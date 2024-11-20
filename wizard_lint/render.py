from typing import List, Dict
import re

def obtain_table_strings(sql_string: str) -> List[str]:
    
    pattern = r'\b\w+\.(?!value\.)\w+\.\w+\b'
    tables = re.findall(pattern, sql_string)
    
    return tables

def render_table_string(config: Dict[str, str], table_string: str) -> str:

    flipped_config = {v: k for k, v in config.items()}

    project, dataset, table = table_string.split(".")

    rendered_dataset = "{{ params['" + flipped_config[dataset] + "'] }}"
    rendered_table = "{{ params['" + flipped_config[table] + "'] }}"

    rendered_string = f"{project}.{rendered_dataset}.{rendered_table}"

    return rendered_string