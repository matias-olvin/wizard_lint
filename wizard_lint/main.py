from file_retriever import (obtain_args, return_dict_from_config_yaml_path,
                            return_sql_paths, return_sql_string_from_path_list)
from sql_parser import SQLParser


def main():
    # obtain paths
    file_path, config_path = obtain_args()

    parser = SQLParser(config_file_path=config_path, file_path=file_path)

    parser.add_jinja_templating_to_sql_string()

if __name__ == "__main__":
    main()
