EXPORT DATA OPTIONS(
    uri = 'gs://pby-process-p-gcs-euwe1-sheets/google_sheets_input/ingestion_date=2024-11-06/smc_ground_truth_volume_dataset_new_brands_table/*.csv.gz',
    FORMAT = 'CSV',
    overwrite = TRUE,
    header = TRUE,
    compression = 'GZIP'
) AS
WITH
    -- Store in a CTE table all sub categories we do have
    median_visits_per_sub_category_excluding_missing AS (
        SELECT DISTINCT
            (sub_category),
            median_category_visits,
            category_median_visits_range,
            NULL AS median_brand_visits
        FROM
            `storage-prod-olvin-com.smc_ground_truth_volume_model.prior_brand_visits`
        WHERE
            sub_category IS NOT NULL
    ),
    median_missing AS (
        SELECT
            * EXCEPT (updated_at)
        FROM
            `storage-prod-olvin-com.smc_ground_truth_volume_model.categories_to_append`
        WHERE
            updated_at >= CAST("2024-11-06" AS DATE)
    )
    -- We left join brand info with median_visits using sub_category 
    -- If subcategory does not exist in current_prior_brand_visits or in categories_to_append, we set default values
SELECT
    b.name,
    b.pid,
    b.sub_category,
    COALESCE(
        median.median_category_visits,
        median_missing.median_category_visits,
        10000
    ) AS median_category_visits,
    COALESCE(
        median.category_median_visits_range,
        median_missing.category_median_visits_range,
        10
    ) AS category_median_visits_range,
    median.median_brand_visits
FROM
    `storage-prod-olvin-com.smc_ground_truth_volume_model.missing_brands` b
    LEFT JOIN median_visits_per_sub_category_excluding_missing median USING (sub_category)
    LEFT JOIN median_missing median_missing USING (sub_category);