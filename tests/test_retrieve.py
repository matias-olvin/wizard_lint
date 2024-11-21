from wizard_lint.retrieve import obtain_sql_string_from_file_path, obtain_file_paths_from_directory, obtain_config_yaml
import yaml


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

# test obtain_config_yaml

def test_obtain_config_yaml(tmp_path):
    # Setup
    config_file = tmp_path / "config.yaml"
    config_content = {
        "database": "test_db",
        "user": "test_user",
        "password": "test_password"
    }
    config_file.write_text(yaml.dump(config_content))

    # Test
    result_config = obtain_config_yaml(str(config_file))

    assert result_config == config_content

def test_obtain_config_yaml_empty_file(tmp_path):
    # Setup
    config_file = tmp_path / "empty_config.yaml"
    config_file.write_text("")

    # Test
    result_config = obtain_config_yaml(str(config_file))

    assert result_config == {}

def test_obtain_config_yaml_invalid_yaml(tmp_path):
    # Setup
    config_file = tmp_path / "invalid_config.yaml"
    config_file.write_text("invalid: [unclosed list")

    # Test
    try:
        obtain_config_yaml(str(config_file))
        assert False, "Expected a yaml.YAMLError to be raised"
    except yaml.YAMLError:
        pass

# test obtain_sql_string_from_file_path

def test_obtain_sql_string_from_file_path(tmp_path):
    # Setup
    sql_file = tmp_path / "test.sql"
    sql_content = "SELECT * FROM test_table;"
    sql_file.write_text(sql_content)

    # Test
    result_sql_string = obtain_sql_string_from_file_path(str(sql_file))

    assert result_sql_string == sql_content

def test_obtain_sql_string_from_file_path_empty_file(tmp_path):
    # Setup
    sql_file = tmp_path / "empty.sql"
    sql_file.write_text("")

    # Test
    result_sql_string = obtain_sql_string_from_file_path(str(sql_file))

    assert result_sql_string == ""

def test_obtain_sql_string_from_file_path_non_existent_file(tmp_path):
    # Setup
    sql_file = tmp_path / "non_existent.sql"

    # Test
    try:
        obtain_sql_string_from_file_path(str(sql_file))
        assert False, "Expected a FileNotFoundError to be raised"
    except FileNotFoundError:
        pass