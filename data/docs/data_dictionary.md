# Data Dictionary — Airline On-Time Performance (FY2025)

## Source & methodology

This dataset is **simulated**, not scraped or licensed — every project decision needs a defensible
answer in an interview, and "I generated it myself, here's the exact logic" is a stronger answer
than an unsourced download. The schema and delay-cause structure are modeled directly on the
real, public **U.S. DOT / Bureau of Transportation Statistics (BTS) Airline On-Time Performance**
dataset (`transtats.bts.gov`), so column names and conventions match what a hiring manager in
this space will recognize on sight.

Generation logic (seasonality, carrier bias, delay-cause weighting) lives in
`scripts/generate_dataset.py`, seeded for reproducibility (`SEED = 42`).

**File:** `data/raw/flights_2025_raw.csv` · 25,991 rows · 23 columns · Jan 1 – Dec 31, 2025 ·
6 carriers · 10 airports · 60 directional routes.

> This file is the immutable source of truth for the whole portfolio project. It is never edited
> in place — Excel, SQL, Python, and Power BI all read it unmodified and produce their own
> cleaned/derived outputs downstream. If a number ever looks wrong, this file is where you go to
> re-derive the truth.

## Columns

| Column | Type | Description | Example |
|---|---|---|---|
| `FlightDate` | Date | Scheduled date of the flight | `2025-03-14` |
| `Airline` | Text | Full carrier name | `Delta Air Lines` |
| `CarrierCode` | Text | 2-letter IATA carrier code | `DL` |
| `FlightNumber` | Integer | Flight number | `1624` |
| `TailNumber` | Text | Aircraft registration (tail number) | `N963NU` |
| `AircraftType` | Text | Aircraft type code | `B738` |
| `Origin` | Text | Origin airport, IATA code | `SEA` |
| `OriginCity` | Text | Origin city | `Seattle` |
| `Destination` | Text | Destination airport, IATA code | `DFW` |
| `DestCity` | Text | Destination city | `Dallas/Fort Worth` |
| `ScheduledDeparture` | Datetime | Scheduled gate departure | `2025-01-31 15:45` |
| `ActualDeparture` | Datetime | Actual gate departure (blank if cancelled) | `2025-01-31 16:29` |
| `ScheduledArrival` | Datetime | Scheduled gate arrival | `2025-01-31 20:14` |
| `ActualArrival` | Datetime | Actual gate arrival (blank if cancelled) | `2025-01-31 21:01` |
| `Cancelled` | Text | Whether the flight was cancelled | `Y` / `N` |
| `CancellationReason` | Text | Weather / Carrier / NAS / Security (blank if not cancelled) | `Weather` |
| `Diverted` | Text | Whether the flight diverted to a different airport | `Y` / `N` |
| `CarrierDelayMin` | Numeric | Minutes of arrival delay attributable to the carrier (airline-controllable: maintenance, crew, cleaning) | `13` |
| `WeatherDelayMin` | Numeric | Minutes attributable to weather | `10` |
| `NASDelayMin` | Numeric | Minutes attributable to the National Airspace System (ATC, congestion) | `8` |
| `SecurityDelayMin` | Numeric | Minutes attributable to security | `2` |
| `LateAircraftDelayMin` | Numeric | Minutes attributable to the inbound aircraft arriving late (cascading delay) | `14` |
| `Distance` | Numeric | Great-circle route distance, miles | `1660` |

### Business conventions (industry standard — keep these consistent across every tool)

- **On-time** = arrival delay **≤ 15 minutes**. This is the actual DOT/BTS definition — use it
  everywhere so your KPI is defensible if someone asks "on-time by what definition?"
- The five `*DelayMin` columns are **only populated when arrival delay ≥ 15 minutes**, exactly like
  real BTS data. A flight delayed 8 minutes has no assigned cause — it's just normal operational
  variance, not a tracked delay event.
- `DepDelayMinutes`, `ArrDelayMinutes`, `Route`, `OnTimeFlag`, `DayOfWeek`, and other derived
  fields are **intentionally not in this raw file** — they're built as calculated columns in the
  next stage (Excel), which is where that formula practice belongs.

## Known data-quality issues (intentional — this is the cleaning checklist)

| Issue | Column(s) | Scope | Fix in Excel |
|---|---|---|---|
| Missing values | `TailNumber` | ~519 rows | Leave blank or flag `"Unknown"` — don't invent a tail number |
| Missing values | `Distance` | 10 rows | `=AVERAGEIFS()` by route, or drop from distance-based analysis only |
| Inconsistent category labels | `Cancelled` | ~259 rows use `Yes`/`No` instead of `Y`/`N` | `Find & Replace`, or a `SWITCH`/nested `IF` standardizing column |
| Stray whitespace | `CarrierCode` | ~129 rows have a leading space | `=TRIM()` |
| Inconsistent casing/whitespace | `OriginCity` | ~1% of rows are `UPPERCASE` with trailing spaces | `=TRIM(PROPER())` |
| Exact duplicate rows | entire row | 20 rows | Excel `Remove Duplicates`, or Power Query dedup |

None of this is random corruption — each issue mirrors something that actually happens when
data gets exported from an ops system, merged from two source systems with different
conventions, or re-uploaded. Point this out in your README: it shows you understand *why*
cleaning matters, not just that you ran a tool.
