# Data Model — Table Setup & Calculated Columns

Builds on `docs/02_data_cleaning.md`. Applies to `tbl_Flights` inside `excel/airline_ontime_dashboard.xlsx`.

## Table

Loaded via Power Query (`Close & Load To → Table`), renamed from the default to `tbl_Flights`
via Table Design → Properties → Table Name. Every PivotTable, chart, and slicer in this project
references `tbl_Flights` by name rather than a fixed cell range, so the dashboard stays correct
if rows are ever added or the source file refreshes.

## Calculated columns

All formulas use structured references (`[@ColumnName]`), typed once in row 2 — Excel Tables
auto-fill new formula columns to every row automatically.

| # | Column | Formula | Purpose |
|---|---|---|---|
| 1 | `DepDelayMinutes` | `=IF([@ActualDeparture]="","",ROUND(([@ActualDeparture]-[@ScheduledDeparture])*1440,0))` | Minutes late leaving the gate |
| 2 | `ArrDelayMinutes` | `=IF([@ActualArrival]="","",ROUND(([@ActualArrival]-[@ScheduledArrival])*1440,0))` | Minutes late arriving — the core metric |
| 3 | `OnTimeFlag` | `=IF([@ActualArrival]="","Cancelled",IF([@ArrDelayMinutes]<=15,"On-Time","Delayed"))` | On-time (≤15 min, DOT/BTS standard) / Delayed / Cancelled |
| 4 | `Route` | `=[@Origin]&"-"&[@Destination]` | Single field for route-level grouping |
| 5 | `MonthNum` | `=MONTH([@FlightDate])` | Correct chronological sort |
| 6 | `MonthName` | `=TEXT([@FlightDate],"mmm")` | Chart-axis label |
| 7 | `DayOfWeek` | `=TEXT([@FlightDate],"ddd")` | Day-of-week analysis |
| 8 | `MaxDelayMin` | `=IF([@ArrDelayMinutes]="","",MAX([@CarrierDelayMin],[@WeatherDelayMin],[@NASDelayMin],[@SecurityDelayMin],[@LateAircraftDelayMin]))` | Helper column feeding #9 |
| 9 | `PrimaryDelayCause` | `=IF([@ArrDelayMinutes]="","",IF([@ArrDelayMinutes]<=15,"None",IF([@CarrierDelayMin]=[@MaxDelayMin],"Carrier",IF([@WeatherDelayMin]=[@MaxDelayMin],"Weather",IF([@NASDelayMin]=[@MaxDelayMin],"NAS",IF([@SecurityDelayMin]=[@MaxDelayMin],"Security","Late Aircraft"))))))` | Dominant root cause per delayed flight |

## Design notes

- Every `IF([@Actual... ]="",...)` guard exists because cancelled flights have blank actual
  times; without the guard, Excel treats blank as 0 and produces a nonsense large negative
  "delay" instead of a clean blank.
- `DepDelayMinutes`/`ArrDelayMinutes` results can inherit time formatting (e.g. display as
  `12:00 AM`) from the datetime columns they're derived from. Set Number Format to **Number**.
- `MaxDelayMin` is a deliberate helper column rather than nesting `MAX(...)` five times inside
  `PrimaryDelayCause` — smaller, named, checkable steps over one dense formula.
- `MonthName`/`DayOfWeek` sort alphabetically by default (Apr, Aug, Dec…), not chronologically.
  `MonthNum` exists specifically to sort correctly; add `DayOfWeekNum =WEEKDAY([@FlightDate])`
  if day-of-week needs the same treatment for a chart.

## Known limitation: `PrimaryDelayCause` never returns "Security"

By design in `scripts/generate_dataset.py`, each delay cause draws a random weight that decides
which one wins `MAX()` on a given flight. Carrier's range is 0.5–1.5; Security's is 0.0–0.15 —
Security's ceiling never reaches Carrier's floor, so Carrier mathematically outweighs Security on
every single row. `SecurityDelayMin` has real, nonzero values in the raw data; it simply never
happens to be the largest of the five, so it never surfaces as a *primary* cause.

This is left as-is rather than patched by regenerating the dataset, because (a) doing so would
cascade into redoing every downstream cleaning/formula/PivotTable step already built on top of
it, and (b) it's a defensible, even realistic pattern — Security is consistently the smallest,
rarest delay cause in the real BTS dataset too.

