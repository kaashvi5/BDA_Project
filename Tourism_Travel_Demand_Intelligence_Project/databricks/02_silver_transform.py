
# Databricks notebook source

# 02 — Silver Transform
# Clean, standardize, enrich, and save Silver tables.

from pyspark.sql import functions as F

# Catalog and schema configuration
CATALOG = "workspace"
SCHEMA = "tourism_analytics"
TABLE_BASE = f"{CATALOG}.{SCHEMA}"

# Read the Bronze Delta tables
visits_raw = spark.table(f"{TABLE_BASE}.bronze_tourism_visits")
weather_raw = spark.table(f"{TABLE_BASE}.bronze_weather")
destinations_raw = spark.table(f"{TABLE_BASE}.bronze_destinations")

# Source column mappings
COLUMN_MAP = {
    "visits": {
        "date": "date",
        "state": "state",
        "destination": "destination",
        "visitor_type": "visitor_type",
        "visitor_count": "visitor_count"
    },
    "weather": {
        "date": "date",
        "state": "state",
        "temp_max": "temp_max_c",
        "temp_min": "temp_min_c",
        "precipitation": "precipitation_mm"
    },
    "destinations": {
        "destination": "destination",
        "state": "state",
        "latitude": "latitude",
        "longitude": "longitude",
        "category": "category"
    }
}


# Check that the required source columns exist
def require_columns(df, mapping, label):
    missing = [
        source_col
        for source_col in mapping.values()
        if source_col not in df.columns
    ]

    if missing:
        raise ValueError(
            f"{label}: missing columns {missing}. "
            f"Available columns: {df.columns}. Update COLUMN_MAP."
        )


# --------------------------------------------------
# 1. Clean tourism visits
# --------------------------------------------------

v = COLUMN_MAP["visits"]
require_columns(visits_raw, v, "visits")

visits = (
    visits_raw.select(
        F.to_date(F.col(v["date"])).alias("visit_date"),
        F.initcap(F.trim(F.col(v["state"]).cast("string"))).alias("state"),
        F.trim(F.col(v["destination"]).cast("string")).alias("destination"),
        F.initcap(
            F.trim(F.col(v["visitor_type"]).cast("string"))
        ).alias("visitor_type"),
        F.col(v["visitor_count"]).cast("long").alias("visitor_count")
    )
    .filter(
        F.col("visit_date").isNotNull() &
        F.col("state").isNotNull() &
        F.col("destination").isNotNull() &
        F.col("visitor_count").isNotNull() &
        (F.col("visitor_count") >= 0)
    )
    .dropDuplicates([
        "visit_date", "state", "destination", "visitor_type"
    ])
)


# --------------------------------------------------
# 2. Clean weather data
# --------------------------------------------------

w = COLUMN_MAP["weather"]
require_columns(weather_raw, w, "weather")

weather = (
    weather_raw.select(
        F.to_date(F.col(w["date"])).alias("weather_date"),
        F.initcap(F.trim(F.col(w["state"]).cast("string"))).alias("state"),
        F.col(w["temp_max"]).cast("double").alias("temp_max_c"),
        F.col(w["temp_min"]).cast("double").alias("temp_min_c"),
        F.col(w["precipitation"]).cast("double").alias("precipitation_mm")
    )
    .filter(
        F.col("weather_date").isNotNull() &
        F.col("state").isNotNull()
    )
    .dropDuplicates(["weather_date", "state"])
)


# --------------------------------------------------
# 3. Clean destination data
# --------------------------------------------------

d = COLUMN_MAP["destinations"]
require_columns(destinations_raw, d, "destinations")

destinations = (
    destinations_raw.select(
        F.trim(F.col(d["destination"]).cast("string")).alias("destination"),
        F.initcap(F.trim(F.col(d["state"]).cast("string"))).alias("state"),
        F.col(d["latitude"]).cast("double").alias("latitude"),
        F.col(d["longitude"]).cast("double").alias("longitude"),
        F.initcap(
            F.trim(F.col(d["category"]).cast("string"))
        ).alias("category")
    )
    .filter(
        F.col("destination").isNotNull() &
        F.col("state").isNotNull()
    )
    .dropDuplicates(["destination", "state"])
)


# --------------------------------------------------
# 4. Add date-based tourism columns
# --------------------------------------------------

visits = (
    visits
    .withColumn("year", F.year("visit_date"))
    .withColumn("month", F.month("visit_date"))
    .withColumn("month_name", F.date_format("visit_date", "MMMM"))
    .withColumn("quarter", F.quarter("visit_date"))
)


# --------------------------------------------------
# 5. Enrich visits with destination information
# --------------------------------------------------

visits_enriched = visits.join(
    destinations,
    ["destination", "state"],
    "left"
)


# --------------------------------------------------
# 6. Prepare weather data for joining
# Rename state to weather_state to avoid duplicate columns
# --------------------------------------------------

weather_for_join = weather.select(
    F.col("weather_date"),
    F.col("state").alias("weather_state"),
    F.col("temp_max_c"),
    F.col("temp_min_c"),
    F.col("precipitation_mm")
)


# Join tourism visits with weather data
silver = (
    visits_enriched
    .join(
        weather_for_join,
        (
            (visits_enriched.visit_date == weather_for_join.weather_date) &
            (visits_enriched.state == weather_for_join.weather_state)
        ),
        "left"
    )
    .drop("weather_date", "weather_state")
    .withColumn("_processed_at", F.current_timestamp())
)


# --------------------------------------------------
# 7. Save Silver Delta tables
# --------------------------------------------------

(
    silver.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{TABLE_BASE}.silver_tourism")
)

(
    destinations.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable(f"{TABLE_BASE}.silver_destinations")
)


# --------------------------------------------------
# 8. Display results and validation
# --------------------------------------------------

print("Silver tourism rows:", silver.count())

display(
    silver.orderBy(
        "visit_date", "state", "destination"
    ).limit(20)
)

display(
    silver.select(
        F.count("*").alias("rows"),
        F.countDistinct("state").alias("states"),
        F.countDistinct("destination").alias("destinations"),
        F.min("visit_date").alias("start_date"),
        F.max("visit_date").alias("end_date"),
        F.sum(
            F.col("visitor_count").isNull().cast("int")
        ).alias("missing_visitors"),
        F.sum(
            F.col("temp_max_c").isNull().cast("int")
        ).alias("missing_weather")
    )
)

print("Silver transformation completed successfully!")
