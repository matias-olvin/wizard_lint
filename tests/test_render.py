from wizard_lint.render import render_table_string, obtain_table_strings

table_name_str = "project.dataset.table"

config = {
    "project_param": "project",
    "dataset_param": "dataset",
    "table_param": "table",
}


def test_render_table_string():
    assert render_table_string() == "{{ params['project_param'] }}.{{ params['dataset_param'] }}.{{ params['table_param'] }}"

def test_obtain_table_strings():
    assert obtain_table_strings() == ["project.dataset.table"]