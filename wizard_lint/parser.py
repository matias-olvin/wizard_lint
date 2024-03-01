import re


class SQLParser():
    def __init__(self, config_dict: dict) -> None:
        self.config_dict = config_dict

    def _replace_project(project_string: str) -> str:
        if project_string == "storage-dev-olvin-com" or project_string == "storage-prod-olvin-com":
            return "{{ var.value.env_project }}"
        elif project_string == "sns-vendor-olvin-poc":
            return "{{ var.value.sns_project }}"
        else:
            raise ValueError(f"Project: {project_string} not recognised")
        
    def _check_exisiting_jinja_templating(table_reference_string: str):
        pass

    def _return_re_match_list(self, pattern: str, sql_string: str) -> list:

        matches = re.findall(pattern=pattern, string=sql_string)

        return matches

    def _reverse_config_dict(config_dict: dict) -> dict:
        
        reversed_dict = {value: key for key, value in config_dict.items()}

        return reversed_dict

    def add_jinja_templating_to_sql_string(self, sql_string: str):
        config = self.config_dict

        re_pattern = "\`(.*)\.(.*)\.(.*)\`"
        
        matches = self._return_re_match_list(re_pattern, sql_string)

        for project_dataset_table in matches:
            project, dataset, table = project_dataset_table

            print("here", project, dataset, table)

        # reverse config dict

        # First obtain table reference

parser = SQLParser(config_dict={"key": "value"})

sql_string = """
CREATE OR REPLACE TABLE
    `storage-prod-olvin-com.postgres_final.SGCenterRaw`
    --  `storage-prod-olvin-com.postgres.SGCenterRaw`
    --  `storage-prod-olvin-com.postgres_final.SGCenterRaw`
    AS
SELECT
    a.*,
    IFNULL(active_places_count, 0) AS active_places_count,
    IF(IFNULL(active_places_count, 0) > 0, TRUE, FALSE) AS monthly_visits_availability,
    IF(
        IFNULL(high_granularity_count, 0) > 0,
        TRUE,
        FALSE
    ) AS patterns_availability
FROM
    `storage-prod-olvin-com.sg_places.malls_base` a
    LEFT JOIN (
        SELECT
            fk_parents,
            COUNTIF(activity IN ('active', 'limited_data')) AS active_places_count,
            COUNTIF(activity = 'active') AS high_granularity_count
        FROM
            (
                SELECT
                    pid,
                    fk_parents,
                    activity
                FROM
                    `storage-prod-olvin-com.postgres_final.SGPlaceRaw`
                    -- `storage-prod-olvin-com.postgres.SGPlaceRaw`
                    -- `storage-prod-olvin-com.postgres_final.SGPlaceRaw`
                    INNER JOIN `storage-prod-olvin-com.postgres_final.SGPlaceActivity`
                    -- `storage-prod-olvin-com.postgres.SGPlaceActivity`
                    -- `storage-prod-olvin-com.postgres_final.SGPlaceActivity`
                    ON pid = fk_sgplaces
            )
        GROUP BY
            fk_parents
    ) ON a.pid = fk_parents
"""


parser.add_jinja_templating_to_sql_string(sql_string=sql_string)
    
