from file_retriever import obtain_args
from sql_parser import SQLParser


def main():
    # obtain paths
    file_path, config_path = obtain_args()

    parser = SQLParser(config_file_path=config_path, file_path=file_path)

    parser.add_jinja_templating_to_sql_string()


if __name__ == "__main__":
    main()
