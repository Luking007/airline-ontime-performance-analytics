"""
generate_dataset.py
--------------------
Simulates one year (2025) of U.S. domestic airline on-time performance data.

Schema is modeled on the real U.S. DOT / Bureau of Transportation Statistics
(BTS) "Airline On-Time Performance" dataset, so the column names and delay-
cause structure match what a hiring manager would recognize from the
industry-standard public dataset.

Design choices (documented so they're reproducible, not "magic numbers"):
- 6 major U.S. carriers, 10 hub airports, 30 base routes (60 directional).
- Each carrier has a fixed on-time "bias" so the dashboard has a real story
  to tell (some carriers are just better than others).
- Delays are seasonal and airport-specific (winter storms in ORD/BOS/JFK/DEN,
  summer thunderstorms in ATL/MIA/DFW/JFK), and worse on holiday weeks.
- Delay-cause minutes (Carrier/Weather/NAS/Security/LateAircraft) are only
  populated when ArrDelay >= 15 min, exactly like real BTS data.
- A small, deliberate set of data-quality issues is injected (missing
  values, inconsistent casing/whitespace, inconsistent Y/N formatting,
  duplicate rows) so the dataset supports a genuine Excel data-cleaning
  lesson instead of a fake one.

Run:
    python generate_dataset.py
Output:
    ../data/raw/flights_2025_raw.csv
"""

import random
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Reproducibility
# ---------------------------------------------------------------------------
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------
CARRIERS = {
    "DL": "Delta Air Lines",
    "AA": "American Airlines",
    "UA": "United Airlines",
    "WN": "Southwest Airlines",
    "B6": "JetBlue Airways",
    "AS": "Alaska Airlines",
}

# Minutes added/subtracted to every delay draw for that carrier.
# Negative = tends to run early/on-time. This is what creates a real
# "best vs. worst carrier" story for the dashboard.
CARRIER_DELAY_BIAS = {"DL": -4, "AS": -3, "WN": -1, "AA": 3, "UA": 4, "B6": 7}

AIRPORTS = {
    "ATL": "Atlanta", "ORD": "Chicago O'Hare", "DFW": "Dallas/Fort Worth",
    "DEN": "Denver", "JFK": "New York JFK", "LAX": "Los Angeles",
    "SFO": "San Francisco", "SEA": "Seattle", "MIA": "Miami", "BOS": "Boston",
}

# Airport -> set of months (1-12) where weather risk is elevated
WEATHER_RISK = {
    "ORD": {12, 1, 2, 3}, "BOS": {12, 1, 2}, "JFK": {12, 1, 2, 7, 8},
    "DEN": {12, 1, 2, 6}, "MIA": {6, 7, 8, 9}, "ATL": {6, 7, 8}, "DFW": {4, 5, 6},
}

HOLIDAY_WEEKS = [
    (datetime(2025, 11, 24), datetime(2025, 11, 30)),  # Thanksgiving
    (datetime(2025, 12, 20), datetime(2026, 1, 2)),    # Christmas/New Year
    (datetime(2025, 6, 30), datetime(2025, 7, 6)),      # July 4th
]

ROUTES = [  # (origin, dest, distance_miles) -- approximate, for realism only
    ("ATL", "JFK", 760), ("ATL", "ORD", 606), ("ATL", "DFW", 731), ("ATL", "MIA", 594),
    ("ATL", "LAX", 1946), ("ATL", "BOS", 946), ("ORD", "DFW", 802), ("ORD", "DEN", 888),
    ("ORD", "JFK", 740), ("ORD", "LAX", 1745), ("ORD", "SEA", 1721), ("DFW", "DEN", 641),
    ("DFW", "LAX", 1235), ("DFW", "MIA", 1121), ("DEN", "LAX", 862), ("DEN", "SFO", 967),
    ("DEN", "SEA", 1024), ("JFK", "LAX", 2475), ("JFK", "SFO", 2586), ("JFK", "MIA", 1090),
    ("JFK", "BOS", 187), ("LAX", "SFO", 337), ("LAX", "SEA", 954), ("LAX", "MIA", 2342),
    ("SFO", "SEA", 679), ("MIA", "BOS", 1258), ("ATL", "SEA", 2182), ("ATL", "SFO", 2139),
    ("DFW", "SEA", 1660), ("DEN", "MIA", 1709),
]

FLEET_BY_CARRIER = {
    "DL": ["B738", "B739", "A321", "A320"], "AA": ["B738", "A321", "A319"],
    "UA": ["B738", "B739", "A320"], "WN": ["B737", "B738"],
    "B6": ["A320", "A321", "E190"], "AS": ["B738", "A320", "B739"],
}

HOUR_WEIGHTS = {5: 2, 6: 5, 7: 8, 8: 9, 9: 7, 10: 6, 11: 6, 12: 6, 13: 6,
                14: 6, 15: 6, 16: 7, 17: 8, 18: 8, 19: 7, 20: 5, 21: 3, 22: 2}


def build_fleet():
    """Assign each carrier a pool of tail numbers, each pinned to one aircraft type."""
    fleet = {}
    for code in CARRIERS:
        for _ in range(15):
            tail = f"N{random.randint(100, 999)}{random.choice('ABCDEFGHJKLMNPQ')}{code[0]}"
            fleet[tail] = (code, random.choice(FLEET_BY_CARRIER[code]))
    return fleet


def is_holiday(d):
    return any(start <= d <= end for start, end in HOLIDAY_WEEKS)


def scheduled_times(flight_date, distance):
    """Build a realistic scheduled departure/arrival pair for a given date + distance."""
    hour = random.choices(list(HOUR_WEIGHTS.keys()), weights=list(HOUR_WEIGHTS.values()))[0]
    minute = random.choice(range(0, 60, 5))
    dep = flight_date.replace(hour=hour, minute=minute)
    block_minutes = max(55, distance * 0.14 + 35 + np.random.normal(0, 4))
    arr = dep + timedelta(minutes=block_minutes)
    return dep, arr


def draw_dep_delay(carrier, month, origin, hour, holiday):
    """Mixture model: mostly tight around on-time, with a right-tailed 'delay event' mode.

    Calibrated so the resulting overall on-time rate (<=15 min arrival delay)
    lands around 78-80%, matching real-world U.S. domestic airline performance.
    """
    if random.random() < 0.88:
        base = np.random.normal(-3, 5.5)
    else:
        base = 15 + np.random.exponential(28)

    bias = CARRIER_DELAY_BIAS[carrier]
    weather_bump = np.random.exponential(7) if month in WEATHER_RISK.get(origin, set()) else 0
    hour_bump = max(0, hour - 12) * 0.35         # later flights inherit more system delay
    holiday_bump = np.random.exponential(6) if holiday else 0

    return base + bias + weather_bump + hour_bump + holiday_bump


def allocate_delay_causes(arr_delay, month, origin, hour):
    """Split ArrDelay minutes across the 5 BTS delay-cause buckets (only when >=15 min)."""
    if arr_delay < 15:
        return (np.nan,) * 5

    weights = {
        "carrier": np.random.uniform(0.5, 1.5),
        "weather": np.random.uniform(2.0, 4.0) if month in WEATHER_RISK.get(origin, set()) else np.random.uniform(0.1, 0.6),
        "nas": np.random.uniform(0.8, 2.0) if origin in {"ORD", "JFK", "ATL"} else np.random.uniform(0.3, 1.0),
        "security": np.random.uniform(0.0, 0.15),
        "late_aircraft": np.random.uniform(1.5, 3.0) if hour >= 17 else np.random.uniform(0.3, 1.0),
    }
    total_w = sum(weights.values())
    mins = {k: round(arr_delay * (w / total_w)) for k, w in weights.items()}

    # fix rounding drift so the five causes sum back to arr_delay
    drift = round(arr_delay) - sum(mins.values())
    mins["carrier"] += drift

    return (mins["carrier"], mins["weather"], mins["nas"], mins["security"], mins["late_aircraft"])


def main():
    fleet = build_fleet()
    tails_by_carrier = {}
    for tail, (code, _) in fleet.items():
        tails_by_carrier.setdefault(code, []).append(tail)

    directional_routes = []
    for o, d, dist in ROUTES:
        directional_routes.append((o, d, dist))
        directional_routes.append((d, o, dist))

    rows = []
    flight_num_lookup = {}

    start_date = datetime(2025, 1, 1)
    end_date = datetime(2025, 12, 31)

    for origin, dest, distance in directional_routes:
        route_carriers = random.sample(list(CARRIERS.keys()), k=random.choice([2, 3, 3, 4]))
        for carrier in route_carriers:
            key = (carrier, origin, dest)
            flight_num_lookup[key] = random.randint(100, 3999)
            flight_number = flight_num_lookup[key]

            d = start_date
            while d <= end_date:
                # ~40% of days this carrier operates this route (realistic frequency, not daily)
                if random.random() < 0.40:
                    month = d.month
                    holiday = is_holiday(d)

                    dep_sched, arr_sched = scheduled_times(d, distance)
                    hour = dep_sched.hour

                    cancel_p = 0.015
                    if month in WEATHER_RISK.get(origin, set()):
                        cancel_p += 0.02
                    if holiday:
                        cancel_p += 0.02
                    cancelled = random.random() < cancel_p

                    diverted = "N"
                    if not cancelled and random.random() < 0.003:
                        diverted = "Y"

                    tail = random.choice(tails_by_carrier[carrier])
                    _, ac_type = fleet[tail]

                    if cancelled:
                        reason = random.choices(
                            ["Weather", "Carrier", "NAS", "Security"],
                            weights=[0.55, 0.30, 0.10, 0.05],
                        )[0]
                        dep_actual = pd.NaT
                        arr_actual = pd.NaT
                        dep_delay = np.nan
                        arr_delay = np.nan
                        cause_mins = (np.nan,) * 5
                    else:
                        dep_delay = draw_dep_delay(carrier, month, origin, hour, holiday)
                        dep_actual = dep_sched + timedelta(minutes=dep_delay)
                        enroute_noise = np.random.normal(0, 8)
                        arr_delay = max(dep_delay - 20, dep_delay + enroute_noise)
                        if diverted == "Y":
                            arr_delay += np.random.uniform(60, 180)
                        arr_actual = arr_sched + timedelta(minutes=arr_delay)
                        reason = ""
                        cause_mins = allocate_delay_causes(arr_delay, month, origin, hour)

                    rows.append({
                        "FlightDate": d.strftime("%Y-%m-%d"),
                        "Airline": CARRIERS[carrier],
                        "CarrierCode": carrier,
                        "FlightNumber": flight_number,
                        "TailNumber": tail,
                        "AircraftType": ac_type,
                        "Origin": origin,
                        "OriginCity": AIRPORTS[origin],
                        "Destination": dest,
                        "DestCity": AIRPORTS[dest],
                        "ScheduledDeparture": dep_sched.strftime("%Y-%m-%d %H:%M"),
                        "ActualDeparture": dep_actual.strftime("%Y-%m-%d %H:%M") if pd.notna(dep_actual) else "",
                        "ScheduledArrival": arr_sched.strftime("%Y-%m-%d %H:%M"),
                        "ActualArrival": arr_actual.strftime("%Y-%m-%d %H:%M") if pd.notna(arr_actual) else "",
                        "Cancelled": "Y" if cancelled else "N",
                        "CancellationReason": reason,
                        "Diverted": diverted,
                        "CarrierDelayMin": cause_mins[0],
                        "WeatherDelayMin": cause_mins[1],
                        "NASDelayMin": cause_mins[2],
                        "SecurityDelayMin": cause_mins[3],
                        "LateAircraftDelayMin": cause_mins[4],
                        "Distance": distance,
                    })
                d += timedelta(days=1)

    df = pd.DataFrame(rows)

    # -----------------------------------------------------------------
    # Inject realistic, deliberate data-quality issues (for the cleaning lesson)
    # -----------------------------------------------------------------
    rng = np.random.default_rng(SEED)
    n = len(df)

    # 1) Missing TailNumber (~2%)
    idx = rng.choice(n, size=int(n * 0.02), replace=False)
    df.loc[idx, "TailNumber"] = ""

    # 2) Missing Distance (~10 rows)
    idx = rng.choice(n, size=10, replace=False)
    df.loc[idx, "Distance"] = np.nan

    # 3) Inconsistent casing/whitespace in city names (~1%)
    idx = rng.choice(n, size=int(n * 0.01), replace=False)
    df.loc[idx, "OriginCity"] = df.loc[idx, "OriginCity"].str.upper() + "  "

    # 4) Inconsistent Y/N formatting on Cancelled/Diverted (~1%)
    idx = rng.choice(n, size=int(n * 0.01), replace=False)
    df.loc[idx, "Cancelled"] = df.loc[idx, "Cancelled"].map({"Y": "Yes", "N": "No"})

    # 5) Stray whitespace on CarrierCode (~0.5%)
    idx = rng.choice(n, size=int(n * 0.005), replace=False)
    df.loc[idx, "CarrierCode"] = " " + df.loc[idx, "CarrierCode"]

    # 6) Exact duplicate rows (20 rows)
    dup_rows = df.sample(n=20, random_state=SEED)
    df = pd.concat([df, dup_rows], ignore_index=True)

    # Shuffle so duplicates/messy rows aren't suspiciously clustered at the end
    df = df.sample(frac=1, random_state=SEED).reset_index(drop=True)

    out_path = "/home/claude/airline-ontime-performance/data/raw/flights_2025_raw.csv"
    df.to_csv(out_path, index=False)
    print(f"Wrote {len(df):,} rows to {out_path}")
    return df


if __name__ == "__main__":
    main()
