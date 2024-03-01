from typing import List

class SQLParser():
    def __init__(self, config_dict: dict) -> None:
        self.config_dict = config_dict

    def add_jinja_templating_to_sql_string(self, sql_string: str) -> str:
        config = self.config_dict

        