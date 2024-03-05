CREATE OR REPLACE TABLE
    `{{ var.value.env_project }}.{{ params['postgres_final_dataset'] }}.{{ params['sgcenterraw_table'] }}`
    --  `{{ var.value.env_project }}.{{ params['postgres_dataset'] }}.{{ params['sgcenterraw_table'] }}`
    --  `{{ var.value.env_project }}.{{ params['postgres_final_dataset'] }}.{{ params['sgcenterraw_table'] }}`
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
    `{{ var.value.env_project }}.{{ params['sg_places_table'] }}.{{ params['malls_base_table'] }}` a
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
                    `{{ var.value.env_project }}.{{ params['postgres_final_dataset'] }}.{{ params['sgplaceraw_table'] }}`
                    -- `{{ var.value.env_project }}.{{ params['postgres_dataset'] }}.{{ params['sgplaceraw_table'] }}`
                    -- `{{ var.value.env_project }}.{{ params['postgres_final_dataset'] }}.{{ params['sgplaceraw_table'] }}`
                    INNER JOIN `{{ var.value.env_project }}.{{ params['postgres_final_dataset'] }}.{{ params['sgplace_activity_table'] }}`
                    -- `{{ var.value.env_project }}.{{ params['postgres_dataset'] }}.{{ params['sgplace_activity_table'] }}`
                    -- `{{ var.value.env_project }}.{{ params['postgres_final_dataset'] }}.{{ params['sgplace_activity_table'] }}`
                    ON pid = fk_sgplaces
            )
        GROUP BY
            fk_parents
    ) ON a.pid = fk_parents