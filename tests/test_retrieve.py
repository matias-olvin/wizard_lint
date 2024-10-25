from wizard_lint.retrieve import obtain_sql_string_from_file_path, obtain_file_paths_from_directory

def test_obtain_sql_string_from_file_path():

    path = "./sql_folder/test_sql_open.sql"
    assert obtain_sql_string_from_file_path(path) == "SELECT * FROM `project.dataset.table`"

def test_obtain_file_paths_from_directory(tmp_path):
    # Setup
    sql_folder = tmp_path / "sql_folder"
    sql_folder.mkdir()
    (sql_folder / "test1.sql").write_text("SELECT * FROM table1;")
    (sql_folder / "test2.sql").write_text("SELECT * FROM table2;")
    (sql_folder / "test.txt").write_text("This is a text file.")

    # Test
    expected_paths = {str(sql_folder / "test1.sql"), str(sql_folder / "test2.sql")}
    result_paths = set(obtain_file_paths_from_directory(str(sql_folder)))

    assert result_paths == expected_paths

def test_obtain_file_paths_from_directory_single_file(tmp_path):
    # Setup
    sql_folder = tmp_path / "sql_folder"
    sql_folder.mkdir()
    sql_file = sql_folder / "single_test.sql"
    sql_file.write_text("SELECT * FROM single_table;")

    # Test
    expected_paths = [str(sql_file)]
    result_paths = obtain_file_paths_from_directory(str(sql_file))

    assert result_paths == expected_paths

