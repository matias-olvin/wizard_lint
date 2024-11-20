from typing import List
import re

def obtain_table_strings(sql_string: str) -> List[str]:
    
    pattern = r'\b\w+\.(?!value\.)\w+\.\w+\b'
    tables = re.findall(pattern, sql_string)
    
    return tables

def render_table_string() -> str:
    return "{{ params['project_param'] }}.{{ params['dataset_param'] }}.{{ params['table_param'] }}"