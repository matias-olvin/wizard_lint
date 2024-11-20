from wizard_lint.render import render_table_string, obtain_table_strings


# test obtain_table_strings
def test_obtain_table_strings_single():
    sql_string = "SELECT * FROM project.dataset.table"
    assert obtain_table_strings(sql_string) == ["project.dataset.table"]

def test_obtain_table_strings_multiple():
    sql_string = "SELECT * FROM project.dataset.table1 JOIN project.dataset.table2 ON table1.id = table2.id"
    assert obtain_table_strings(sql_string) == ["project.dataset.table1", "project.dataset.table2"]

def test_obtain_table_strings_no_match():
    sql_string = "SELECT * FROM table"
    assert obtain_table_strings(sql_string) == []

def test_obtain_table_strings_mixed():
    sql_string = "SELECT * FROM project.dataset.table1, dataset.table2 WHERE project.dataset.table3.id = table2.id"
    assert obtain_table_strings(sql_string) == ["project.dataset.table1", "project.dataset.table3"]

def test_obtain_table_strings_with_airflow_vars_and_no_tables():
    sql_string = "SELECT * FROM table WHERE column = '{{ var.value.variable_name }}'"
    assert obtain_table_strings(sql_string) == []

# test render_table_string

table_string = "project.dataset.table"

def test_render_table_string_basic():
    config = {
        "dataset_param": "dataset",
        "table_param": "table",
    }
    assert render_table_string(config=config, table_string=table_string) == "project.{{ params['dataset_param'] }}.{{ params['table_param'] }}"
    
def test_render_table_string_with_different_config():
    config = {
        "ds_param": "dataset",
        "tbl_param": "table",
    }
    assert render_table_string(config=config, table_string=table_string) == "project.{{ params['ds_param'] }}.{{ params['tbl_param'] }}"

def test_render_table_string_with_missing_config():
    config = {
        "dataset_param": "dataset",
    }
    try:
        render_table_string(config=config, table_string=table_string)
        assert False, "Expected KeyError"
    except KeyError:
        pass

def test_render_table_string_with_extra_config():
    config = {
        "dataset_param": "dataset",
        "table_param": "table",
        "extra_param": "extra",
    }
    assert render_table_string(config=config, table_string=table_string) == "project.{{ params['dataset_param'] }}.{{ params['table_param'] }}"

def test_render_table_string_with_empty_config():
    config = {}
    try:
        render_table_string(config=config, table_string=table_string)
        assert False, "Expected KeyError"
    except KeyError:
        pass

def test_render_table_string_with_invalid_table_string():
    config = {
        "dataset_param": "dataset",
        "table_param": "table",
    }
    invalid_table_string = "project.dataset"
    try:
        render_table_string(config=config, table_string=invalid_table_string)
        assert False, "Expected ValueError"
    except ValueError:
        pass
