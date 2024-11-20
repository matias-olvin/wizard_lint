from wizard_lint.retrieve import obtain_file_paths_from_directory, obtain_sql_string_from_file_path


def main():

    # obtain file paths from input directory
    file_paths = obtain_file_paths_from_directory("placeholder")

    # obtain sql from file paths obtained above
    sql_strings = [obtain_sql_string_from_file_path(path) for path in file_paths]

    print(sql_strings)

if __name__=="__main__":
    main()