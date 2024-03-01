import re
from typing import List


class SQLParser:
    def __init__(self, config_dict: dict) -> None:
        self.config_dict = config_dict
        self.missing_keys_set = set()
        self.unhashable_keys = set()
        self.files_changed = 0

    def _replace_project(self, project_string: str) -> str:
        if (
            project_string == "storage-dev-olvin-com"
            or project_string == "storage-prod-olvin-com"
        ):
            return "{{ var.value.env_project }}"
        elif project_string == "sns-vendor-olvin-poc":
            return "{{ var.value.sns_project }}"
        else:
            raise ValueError(f"Project: {project_string} not recognised")

    def _return_re_match_unique_before_and_after_list(
        self, pattern: str, sql_string: str
    ) -> List[dict]:

        unique_table_references_set = set()

        matches = re.findall(pattern=pattern, string=sql_string)

        for project_dataset_table in matches:
            project, dataset, table = project_dataset_table

            table_ref_string = f"{project}.{dataset}.{table}"

            unique_table_references_set.add(table_ref_string)

        unique_before_and_after_list = [
            {"before": before, "after": None} for before in unique_table_references_set
        ]

        return unique_before_and_after_list

    def _reverse_config_dict(self, config_dict: dict) -> dict:

        reversed_dict = dict()

        for key, value in config_dict.items():
            try:
                reversed_dict[value] = key
            except TypeError:
                self.unhashable_keys.add(key)

        return reversed_dict

    def _check_exisiting_jinja_templating(self, ref_string: str):
        if ref_string.startswith("{{") and ref_string.endswith("}}"):
            return True
        else:
            return False

    def _replace_vals_for_keys(self, reversed_dict: dict, table_ref_string: str):

        project, dataset, table = table_ref_string.split(".")

        var_project = self._replace_project(project)

        try:

            if self._check_exisiting_jinja_templating(dataset):
                param_key_dataset = dataset
            else:
                param_key_dataset = f"{{{{ params['{reversed_dict[dataset]}'] }}}}"
        except KeyError:
            self.missing_keys_set.add(dataset)
            param_key_dataset = dataset

        try:
            if self._check_exisiting_jinja_templating(table):
                param_key_table = table
            else:
                param_key_table = f"{{{{ params['{reversed_dict[table]}'] }}}}"
        except KeyError:
            self.missing_keys_set.add(table)
            param_key_table = table

        return f"{var_project}.{param_key_dataset}.{param_key_table}"

    def _return_rendered_sql_string(
        self, rendered_before_and_after_list: List[dict], sql_string: str
    ):
        for ba_dict in rendered_before_and_after_list:
            sql_string = sql_string.replace(ba_dict["before"], ba_dict["after"])

        return sql_string

    def add_jinja_templating_to_sql_string(self, sql_string: str):
        config = self.config_dict

        re_pattern = "\`(.*)\.(.*)\.(.*)\`"

        unique_before_and_after_list = (
            self._return_re_match_unique_before_and_after_list(re_pattern, sql_string)
        )

        reverse_config_dict = self._reverse_config_dict(config)

        rendered_before_and_after_list = list()

        for unique_table_ref in unique_before_and_after_list:
            before = unique_table_ref["before"]

            after = self._replace_vals_for_keys(
                reversed_dict=reverse_config_dict, table_ref_string=before
            )

            unique_table_ref["after"] = after

            rendered_before_and_after_list.append(unique_table_ref)

        missing_keys = self.missing_keys_set

        if len(missing_keys) != 0:
            print(f"Missing the following keys: {missing_keys}. File left unchanged")

        rendered_sql_string = self._return_rendered_sql_string(
            rendered_before_and_after_list=rendered_before_and_after_list,
            sql_string=sql_string,
        )

        self.files_changed += 1

        print(rendered_sql_string)
