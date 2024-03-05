import os
import re
from typing import List

import yaml
from rich.console import Console
from rich.text import Text


class SQLParser:
    def __init__(self, config_file_path: str, file_path: str) -> None:
        self.file_path = file_path
        self.config_file_path = config_file_path
        self.missing_keys_set = set()
        self.unhashable_keys = set()
        self.files_changed = 0
        self.total_number_of_files = 0

    def _return_dict_from_config_yaml_path(self, file_path: str) -> dict:
        with open(file_path, "r") as file:
            return dict(yaml.safe_load(file))

    def _return_sql_string_from_path_list(
        self, file_path_list: List[str]
    ) -> List[List[str]]:
        """Return the sql strings in a list"""
        sql_string_and_path_list = list()

        for path in file_path_list:
            with open(path, "r") as file:
                sql_string = file.read()

            sql_string_and_path_list.append([sql_string, path])

        return sql_string_and_path_list

    def _return_sql_paths(self, file_path: str) -> List[str]:
        if file_path.endswith(".sql"):
            self.total_number_of_files = 1
            return [file_path]
        else:
            sql_files = []
            for root, _, files in os.walk(file_path):
                for file in files:
                    if file.endswith(".sql"):
                        sql_files.append(os.path.join(root, file))

            self.total_number_of_files = len(sql_files)

            return sql_files

    def _return_config_dict_and_sql_strings(self) -> tuple[dict, list]:
        # pass file path to be render from sql to string
        file_path = self.file_path
        config_path = self.config_file_path

        sql_files = self._return_sql_paths(file_path)

        sql_strings_and_paths = self._return_sql_string_from_path_list(sql_files)

        config_dict = self._return_dict_from_config_yaml_path(config_path)

        return config_dict, sql_strings_and_paths

    def _replace_project(self, project_string: str) -> str:
        if (
            project_string == "storage-dev-olvin-com"
            or project_string == "storage-prod-olvin-com"
        ):
            return "{{ var.value.env_project }}"
        elif project_string == "sns-vendor-olvin-poc":
            return "{{ var.value.sns_project }}"
        elif project_string == "{{ var.value.env_project }}":
            return project_string
        elif project_string == "{{ var.value.sns_project }}":
            return project_string
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

        # project, dataset, table = table_ref_string.split(".")[:-2]
        table_ref_string
        matches = re.findall(pattern="(.*)\.(.*)\.(.*)", string=table_ref_string)

        project, dataset, table = matches[0]

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

    def _create_or_replace_sql_file(self, file_path: str, content: str):
        with open(file_path, "w") as file:
            file.write(content)

    def _check_for_file_change(self, rendered_before_and_after_list: list[dict]) -> bool:
        
        changed = False

        for ba_dict in rendered_before_and_after_list:
            before = ba_dict["before"]
            after = ba_dict["after"]
            if before != after:
                changed = True
                break
            
        return changed

    def add_jinja_templating_to_sql_string(self):

        config_dict, sql_string_and_path_list = (
            self._return_config_dict_and_sql_strings()
        )

        for sql_string, path in sql_string_and_path_list:

            re_pattern = "\`(.*)\.(.*)\.(.*)\`"

            unique_before_and_after_list = (
                self._return_re_match_unique_before_and_after_list(
                    re_pattern, sql_string
                )
            )

            reverse_config_dict = self._reverse_config_dict(config_dict)

            rendered_before_and_after_list = list()

            for unique_table_ref in unique_before_and_after_list:
                before = unique_table_ref["before"]

                after = self._replace_vals_for_keys(
                    reversed_dict=reverse_config_dict, table_ref_string=before
                )

                unique_table_ref["after"] = after

                rendered_before_and_after_list.append(unique_table_ref)

            missing_keys = self.missing_keys_set

            check_for_changes = self._check_for_file_change(rendered_before_and_after_list=rendered_before_and_after_list)

            if len(missing_keys) != 0:
                print(
                    f"Missing the following keys: {missing_keys}: {path} left unchanged"
                )
            elif not check_for_changes:
                print(f"{path} left unchanged")
            else:
                rendered_sql_string = self._return_rendered_sql_string(
                    rendered_before_and_after_list=rendered_before_and_after_list,
                    sql_string=sql_string,
                )

                # path = path.replace(".sql", "_test.sql")

                self._create_or_replace_sql_file(path, rendered_sql_string)

                self.files_changed += 1

        self._summary()

    def _summary(self):
        tot_files = self.total_number_of_files
        f_changed = self.files_changed

        # Create a Console instance
        console = Console()

        # # Create a Text instance
        text = f"[bold cyan]Number of files changed[/bold cyan]: [bold red]{f_changed}[/bold red]\n[bold magenta]Number of files left untouched[/bold magenta]: [white]{tot_files - f_changed}[/white]"

        console.print(text)
