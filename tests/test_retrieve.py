from wizard_lint.retrieve import obtain_sql_string_from_file_path, obtain_file_paths_from_directory

def test_obtain_sql_string_from_file_path():

    path = "./sql_folder/test_sql_open.sql"
    assert obtain_sql_string_from_file_path(path) == "SELECT * FROM `project.dataset.table`"

def test_obtain_file_paths_from_directory():
    assert obtain_file_paths_from_directory() == ["./sql_folder/dummy.sql"]