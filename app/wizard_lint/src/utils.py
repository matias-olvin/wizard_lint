from typing import Dict
from jinja2 import Template


def unrender_sql_string_using_jinja(config: Dict[str, str], sql_string: str) -> str:

    template = Template(sql_string)

    rendered_sql_string = template.render(config)

    return rendered_sql_string
