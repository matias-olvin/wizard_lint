CREATE OR REPLACE TABLE
    `storage-prod-olvin-com.postgres_final.SGCenterRaw`
    --  `storage-prod-olvin-com.postgres.SGCenterRaw`
    --  `storage-prod-olvin-com.postgres_final.SGCenterRaw`
    AS
SELECT
    a.*,
FROM
    `storage-prod-olvin-com.sg_places.malls_base` a
    LEFT JOIN (
            (
                SELECT
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
    )