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