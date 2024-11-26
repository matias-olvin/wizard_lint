import argparse

from render import (obtain_table_strings,
                    overwrite_sql_file_with_rendered_sql_string,
                    render_sql_string_with_mapping_dict, render_table_string)
from retrieve import (obtain_config_yaml, obtain_file_paths_from_directory,
                      obtain_sql_string_from_file_path)
from rich import print


def main():

    # obtain args from command line
    parser = argparse.ArgumentParser(description="Process some SQL files.")
    parser.add_argument("config_path", type=str, help="Path to the config YAML file")
    parser.add_argument(
        "sql_folder_path", type=str, help="Path to the folder containing SQL files"
    )

    args = parser.parse_args()

    config_path = args.config_path
    sql_folder_path = args.sql_folder_path

    # load config file from path
    config = obtain_config_yaml(config_path)

    # obtain file paths from input directory
    file_paths = obtain_file_paths_from_directory(sql_folder_path)

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
            print(
                f"[cyan]{n + 1}[/cyan] [bold white]{path}[/bold white] [bold yellow]left untouched[/bold yellow]"
            )
        else:
            print(
                f"[cyan]{n + 1}[/cyan] [bold white]{path} rendered[/bold white] [bold green]successfully[/bold green]"
            )

            overwrite_sql_file_with_rendered_sql_string(path, rendered_sql_string)


if __name__ == "__main__":
    main()
