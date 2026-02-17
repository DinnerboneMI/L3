Early leavers (Eurostat) Lithuania and EU

This project loads open data from Eurostat and analyzes the share of early leavers from education and training (age 18-24).

Data source:
Dataset: Eurostat `sdg_04_10`
API endpoint: https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/sdg_04_10

How to run:
pip install -r requirements.txt
python -m src.main

Output:
The program creates an output folde
latest_summary.xlsx - latest-year summary (LT and EU27, by sex)
lt_total_trend.xlsx - Lithuania time series + YoY change
trend_lt_vs_eu.png - trend plot (Lithuania vs EU27 + 9% target)