from wizard_lint.render import render_table_string, obtain_table_strings, render_sql_string_with_mapping_dict


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

# test render_sql_string_with_mapping_dict

def test_render_sql_string_with_mapping_dict_single():
    sql_string = "SELECT * FROM project.dataset.table"
    mapping = {
        "project.dataset.table": "project.{{ params['dataset_key'] }}.{{ params['table_key'] }}"
    }
    expected_result = "SELECT * FROM project.{{ params['dataset_key'] }}.{{ params['table_key'] }}"
    assert render_sql_string_with_mapping_dict(sql_string, mapping) == expected_result

def test_render_sql_string_with_mapping_dict_multiple():
    sql_string = "SELECT * FROM project.dataset.table1 JOIN project.dataset.table2 ON table1.id = table2.id"
    mapping = {
        "project.dataset.table1": "project.{{ params['dataset_key1'] }}.{{ params['table_key1'] }}",
        "project.dataset.table2": "project.{{ params['dataset_key2'] }}.{{ params['table_key2'] }}"
    }
    expected_result = "SELECT * FROM project.{{ params['dataset_key1'] }}.{{ params['table_key1'] }} JOIN project.{{ params['dataset_key2'] }}.{{ params['table_key2'] }} ON table1.id = table2.id"
    assert render_sql_string_with_mapping_dict(sql_string, mapping) == expected_result

def test_render_sql_string_with_mapping_dict_no_match():
    sql_string = "SELECT * FROM project.dataset.table"
    mapping = {
        "project.dataset.table1": "project.{{ params['dataset_key1'] }}.{{ params['table_key1'] }}"
    }
    expected_result = "SELECT * FROM project.dataset.table"
    assert render_sql_string_with_mapping_dict(sql_string, mapping) == expected_result

def test_render_sql_string_with_mapping_dict_partial_match():
    sql_string = "SELECT * FROM project.dataset.table1, project.dataset.table2"
    mapping = {
        "project.dataset.table1": "project.{{ params['dataset_key1'] }}.{{ params['table_key1'] }}"
    }
    expected_result = "SELECT * FROM project.{{ params['dataset_key1'] }}.{{ params['table_key1'] }}, project.dataset.table2"
    assert render_sql_string_with_mapping_dict(sql_string, mapping) == expected_result

def test_render_sql_string_with_mapping_dict_with_airflow_vars():
    sql_string = "SELECT * FROM project.dataset.table WHERE column = '{{ var.value.variable_name }}'"
    mapping = {
        "project.dataset.table": "project.{{ params['dataset_key'] }}.{{ params['table_key'] }}"
    }
    expected_result = "SELECT * FROM project.{{ params['dataset_key'] }}.{{ params['table_key'] }} WHERE column = '{{ var.value.variable_name }}'"
    assert render_sql_string_with_mapping_dict(sql_string, mapping) == expected_result