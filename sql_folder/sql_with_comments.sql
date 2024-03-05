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