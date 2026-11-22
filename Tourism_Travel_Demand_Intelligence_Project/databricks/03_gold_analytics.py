# Databricks notebook source
# MAGIC %md
# MAGIC # 03 — Gold analytics tables
# MAGIC Aggregated tables for dashboarding and decision support.

from pyspark.sql import functions as F

CATALOG = "workspace"
SCHEMA = "tourism_analytics"
TABLE_BASE = f"{CATALOG}.{SCHEMA}"

silver = spark.table(f"{TABLE_BASE}.silver_tourism")

# Destination popularity and visitor KPIs
gold_destination = (silver.groupBy("state", "destination", "category")
    .agg(
        F.sum("visitor_count").alias("total_visitors"),
        F.avg("visitor_count").alias("avg_visitors_per_record"),
        F.max("visitor_count").alias("max_visitors_in_period"),
        F.countDistinct("visit_date").alias("days_reported"),
        F.avg("temp_max_c").alias("avg_max_temperature_c"),
        F.avg("precipitation_mm").alias("avg_precipitation_mm")
    ))

# Monthly seasonal trend
gold_monthly = (silver.groupBy("year", "month", "month_name")
    .agg(
        F.sum("visitor_count").alias("total_visitors"),
        F.countDistinct("destination").alias("destinations_reported"),
        F.avg("temp_max_c").alias("avg_max_temperature_c"),
        F.avg("precipitation_mm").alias("avg_precipitation_mm")
    ))

# Domestic vs foreign visitors
gold_visitor_type = (silver.groupBy("state", "destination", "year", "visitor_type")
    .agg(
        F.sum("visitor_count").alias("total_visitors"),
        F.avg("visitor_count").alias("avg_visitors_per_record")
    ))

# Weather and tourism at daily destination level
gold_weather = (silver.groupBy(
        "visit_date", "year", "month", "state", "destination"
    ).agg(
        F.sum("visitor_count").alias("total_visitors"),
        F.avg("temp_max_c").alias("temp_max_c"),
        F.avg("temp_min_c").alias("temp_min_c"),
        F.avg("precipitation_mm").alias("precipitation_mm")
    ))

# State overview
gold_state = (silver.groupBy("state")
    .agg(
        F.sum("visitor_count").alias("total_visitors"),
        F.countDistinct("destination").alias("destinations_count"),
        F.countDistinct("visit_date").alias("days_reported"),
        F.avg("visitor_count").alias("avg_visitors_per_record")
    ))

tables = {
    "gold_destination_popularity": gold_destination,
    "gold_monthly_trends": gold_monthly,
    "gold_visitor_type": gold_visitor_type,
    "gold_weather_tourism": gold_weather,
    "gold_state_overview": gold_state
}

for name, df in tables.items():
    (df.write.format("delta").mode("overwrite")
       .option("overwriteSchema", "true")
       .saveAsTable(f"{TABLE_BASE}.{name}"))
    print(name, "rows:", df.count())
    display(df.limit(10))
