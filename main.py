from wizard_lint.retrieve import obtain_file_paths_from_directory, obtain_sql_string_from_file_path, obtain_config_yaml
from wizard_lint.render import obtain_table_strings, render_table_string


def main():

    config = obtain_config_yaml("./config.yaml")

    # obtain file paths from input directory
    file_paths = obtain_file_paths_from_directory("./sql_folder")

    # obtain sql from file paths obtained above
    sql_strings = [obtain_sql_string_from_file_path(path) for path in file_paths]

    for sql_string in sql_strings:
        table_strings = obtain_table_strings(sql_string)

        rendered_table_strings_mapping = {table_string: render_table_string(config, table_string) for table_string in table_strings}

        print(rendered_table_strings_mapping)

if __name__=="__main__":
    main()