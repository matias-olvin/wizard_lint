from wizard_lint.render import render_table_string, obtain_table_strings

table_name_str = "project.dataset.table"

config = {
    "project_param": "project",
    "dataset_param": "dataset",
    "table_param": "table",
}


def test_render_table_string():
    assert render_table_string() == "{{ params['project_param'] }}.{{ params['dataset_param'] }}.{{ params['table_param'] }}"

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
