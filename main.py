from wizard_lint.retrieve import obtain_file_paths_from_directory, obtain_sql_string_from_file_path, obtain_config_yaml
from wizard_lint.render import obtain_table_strings, render_table_string, render_sql_string_with_mapping_dict


def main():

    config = obtain_config_yaml("./config.yaml")

    # obtain file paths from input directory
    file_paths = obtain_file_paths_from_directory("./sql_folder")

    # obtain sql from file paths obtained above
    sql_strings = [obtain_sql_string_from_file_path(path) for path in file_paths]

    rendered_sql_strings = list()

    for sql_string in sql_strings:
        table_strings = obtain_table_strings(sql_string)

        rendered_table_strings_mapping = {table_string: render_table_string(config, table_string) for table_string in table_strings}

        rendered_sql_string = render_sql_string_with_mapping_dict(sql_string, rendered_table_strings_mapping)

        rendered_sql_strings.append(rendered_sql_string)

if __name__=="__main__":
    main()