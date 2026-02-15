import csv
import json
import os
import requests
from datetime import datetime

DATASET_ID = "pwn4-m3yp"
BASE_URL = f"https://data.cdc.gov/resource/{DATASET_ID}.json"

NEW_CASES_FIELD = "new_cases"

#creating a int converter 
def to_int(x):
    if x is None:
        return 0
    try:
        return int(float(x))
    except:
        return 0

def month_name(year,month):
    return datetime(year, month, 1).strftime("%B")


def main():
    states_pop = {}
    with open("data5500_mycode/hw5/states.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            state = row[0].strip()
            pop = int(row[1].strip())
            states_pop[state] = pop
    
    highest = None
    lowest = None

    for state, population in states_pop.items():
        params = {
            "$where": f"state= '{state}' And end_date >= '2020-01-01' AND end_date <= '2023-12-31'",
            "$order": "end_date ASC",
            "$limit": 50000
        }
        response = requests.get(BASE_URL, params = params, timeout=30)
        response.raise_for_status()
        data = response.json()

        with open(f"data5500_mycode/hw5/{state}.json", "w", encoding="utf-8") as out:
            json.dump(data, out, indent=2)
        
        if not data:
            print(f"{state}, No data")

        dates = []
        weekly_cases = []

        for row in data:
            end_date_str = row.get("end_date")
            if not end_date_str:
                continue

            date_part = end_date_str.split("T")[0]
            d = datetime.strptime(date_part, "%Y-%m-%d").date()
            c = to_int(row.get(NEW_CASES_FIELD))

            dates.append(d)
            weekly_cases.append(c)

        if not weekly_cases:
            print(f"{state}, No weekly data.")
        
        avg_weekly = sum(weekly_cases) / len(weekly_cases)
        max_weekly = max(weekly_cases)
        max_index = weekly_cases.index(max_weekly)
        max_date = dates[max_index]


        monthly_totals = {}
        for d, c in zip(dates, weekly_cases):
            key = (d.year, d.month)
            monthly_totals[key] = monthly_totals.get(key,0) + c

        best_key = max(monthly_totals, key=lambda k: monthly_totals[k])
        best_year, best_month = best_key
        best_monthly_total = monthly_totals[best_key]

        best_month_str = f"{month_name(best_year, best_month)}"

        best_pct = (best_monthly_total / population) * 100

        
        print(f"State name: {state}")
        print(f"Average Number of new cases: {avg_weekly:.2f}")
        print(f"Date with the highest new cases: {max_date} ({max_weekly})")
        print(f"Date with highest Percentage per population: {best_pct:.2f}% (Population: {population})")
        
        stats = {
            "state": state,
            "best_pct": best_pct,
            "best_month_str": best_month_str,
            "best_month_total": best_monthly_total,
            "population": population
        }

        if highest is None or stats["best_pct"] > highest["best_pct"]:
            highest = stats
        if lowest is None or stats["best_pct"] < highest["best_pct"]:
            lowest = stats

        print("State with highest percentage during its highest month:")
        print(
            f"{highest['state']} - {highest['best_pct']:.2f}% in {highest['best_month_str']} "
        )

        print("State with lowest percentage during its highest month:")
        print(
            f"{lowest['state']} - {lowest['best_pct']:.2f}% in {lowest['best_month_str']} "
        )

main()