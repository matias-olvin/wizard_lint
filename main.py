from rich import print

from wizard_lint.render import (obtain_table_strings,
                                overwrite_sql_file_with_rendered_sql_string,
                                render_sql_string_with_mapping_dict,
                                render_table_string)
from wizard_lint.retrieve import (obtain_config_yaml,
                                  obtain_file_paths_from_directory,
                                  obtain_sql_string_from_file_path)


def main():

    config = obtain_config_yaml("./config.yaml")

    # obtain file paths from input directory
    file_paths = obtain_file_paths_from_directory("./sql_folder")

    for n, path in enumerate(file_paths):

        sql_string = obtain_sql_string_from_file_path(path)

        table_strings = obtain_table_strings(sql_string)

        rendered_table_strings_mapping = {
            table_string: render_table_string(config, table_string)
            for table_string in table_strings
        }

        rendered_sql_string = render_sql_string_with_mapping_dict(
            sql_string, rendered_table_strings_mapping
        )

        if sql_string == rendered_sql_string:
            print(f"[cyan]{n + 1}[/cyan][white]{path}[/white] left untouched")
        else:
            print(
                f"[cyan]{n + 1}[/cyan][white]{path} rendered[/white] [green]successfully[/green]"
            )

            overwrite_sql_file_with_rendered_sql_string(path, rendered_sql_string)


if __name__ == "__main__":
    main()
