from file_retriever import obtain_args, return_sql_paths, return_sql_string_from_path_list, return_dict_from_config_yaml_path

def main():
    # obtain paths
    file_path, config_path = obtain_args()

    # pass file path to be render from sql to string
    sql_files = return_sql_paths(file_path=file_path)

    sql_strings = return_sql_string_from_path_list(sql_files)

    config_dict = return_dict_from_config_yaml_path(file_path=config_path)


if __name__ == '__main__':
    main()
