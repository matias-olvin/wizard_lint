# Documentation for the `app/wizard_lint` module

## Overview
The `wizard_lint` module is designed to add Jinja templating to SQL code. It provides functionality to parse SQL files, apply Jinja templating, and overwrite the original SQL files with the rendered SQL strings. The module includes various components for handling file operations, SQL parsing, and rendering.

## Components

### `app/wizard_lint/src/render.py`
- **Functions:**
    - `obtain_table_strings(sql_string: str) -> List[str]`: Extracts table strings from the given SQL string.
    - `overwrite_sql_file_with_rendered_sql_string(file_path: str, rendered_sql_string: str)`: Overwrites the SQL file at the specified path with the rendered SQL string.
    - `render_sql_string_with_mapping_dict(sql_string: str, mapping: Dict[str, str]) -> str`: Renders the SQL string using the provided mapping dictionary.
    - `render_table_string(config: Dict[str, str], table_string: str) -> str`: Renders a table string using the provided configuration.

### `app/wizard_lint/src/retrieve.py`
- **Functions:**
    - `obtain_config_yaml(path: str) -> Dict[str, str]`: Loads and returns the configuration from the specified YAML file.
    - `obtain_file_paths_from_directory(directory_path: str) -> List[str]`: Retrieves all file paths from the specified directory.
    - `obtain_sql_string_from_file_path(file_path: str) -> str`: Reads and returns the SQL string from the specified file path.

### `app/wizard_lint/src/main.py`
- **Main Function:**
    - `main()`: The entry point of the application. It processes command-line arguments to obtain the configuration file path and the SQL folder path. It then loads the configuration, retrieves SQL file paths, parses and renders SQL strings, and overwrites the original SQL files with the rendered SQL strings.

### `app/wizard_lint/tests/test_render.py`
- **Test Functions:**
    - `test_overwrite_sql_file_with_rendered_sql_string_empty_file(tmp_path)`: Tests overwriting an empty SQL file with a rendered SQL string.
    - `test_overwrite_sql_file_with_rendered_sql_string_basic(tmp_path)`: Tests overwriting a SQL file with initial content with a rendered SQL string.
    - `test_render_sql_string_with_mapping_dict_with_airflow_vars()`: Tests rendering an SQL string with a mapping dictionary containing Airflow variables.
    - Additional test functions for various scenarios related to obtaining table strings and rendering table strings.

### `setup.py`
- **Setup Configuration:**
    - Defines the package metadata, dependencies, and additional requirements for development.

### `app/wizard_lint/__init__.py` and `app/wizard_lint/src/__init__.py`
- **Initialization:**
    - Imports and exposes the main functions and classes from the `render` and `retrieve` modules.

## Usage
To use the `wizard_lint` module, run the `main.py` script with the appropriate command-line arguments: