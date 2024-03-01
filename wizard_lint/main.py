from file_retriever import obtain_args, return_sql_paths, return_sql_string_from_path_list, return_dict_from_config_yaml_path
from sql_parser import SQLParser

def main():
    # obtain paths
    file_path, config_path = obtain_args()

    # pass file path to be render from sql to string
    sql_files = return_sql_paths(file_path=file_path)

    sql_strings = return_sql_string_from_path_list(sql_files)

    config_dict = return_dict_from_config_yaml_path(file_path=config_path)

    parser = SQLParser(config_dict=config_dict)

    for sql_string in sql_strings:
        parser.add_jinja_templating_to_sql_string(sql_string=sql_string)

if __name__ == '__main__':
    main()
