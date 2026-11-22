# Power BI Dashboard Guide

Import the five Gold CSV exports from Databricks. Each export path is a folder; import the `part-*.csv` file inside it.

## Recommended model
Create a State dimension (unique state names) and Destination dimension (unique destination + state pairs). Relate them to Gold tables using the matching keys. Avoid many-to-many relationships where possible. A Date dimension can support monthly and daily filtering; use a proper month-start date for monthly data.

## Page 1 — Tourism Overview
- KPI cards: Total Visitors, States Covered, Destinations Covered.
- Bar chart: visitors by state.
- Line chart: monthly visitors.
- Slicers: Year, State, Visitor Type.

## Page 2 — Destination Intelligence
- Ranked bar chart: top destinations by visitors.
- Table: destination, state, total visitors, days reported.
- Map: latitude and longitude from destination metadata (if validated).

## Page 3 — Seasonal Travel Trends
- Line chart: visitors by month.
- Column chart: visitors by quarter.
- Month slicer and year slicer.
- Sort month names by month number.

## Page 4 — Domestic vs Foreign
- Stacked bar: domestic and foreign visitors by state/destination.
- Donut chart: visitor type share.
- Table: visitor type, year, destination, total visitors.

## Page 5 — Weather and Tourism
- Scatter chart: precipitation vs visitors.
- Scatter chart: maximum temperature vs visitors.
- Tooltip: destination, date, state.
- State and date filters.

## Presentation notes
- Add source, date coverage and refresh date to the report.
- Keep units and definitions visible.
- Weather correlation does not prove weather caused a change in tourism.
- If the official dataset is monthly or yearly, use a matching weather aggregation level before comparing.
- Do not use synthetic sample data for factual claims.
