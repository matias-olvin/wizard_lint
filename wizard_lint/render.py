from typing import List

def obtain_table_strings() -> List[str]:
    return ["project.dataset.table"]

def render_table_string() -> str:
    return "{{ params['project_param'] }}.{{ params['dataset_param'] }}.{{ params['table_param'] }}"