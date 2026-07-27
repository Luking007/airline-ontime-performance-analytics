# Data Cleaning Log — Power Query

Source: `data/raw/flights_2025_raw.csv` (25,991 rows, untouched). Output: an Excel Table via
Power Query, saved separately as `excel/airline_ontime_dashboard.xlsx`. This log exists so
anyone (including an interviewer) can see exactly what was done to the data and why, without
re-deriving it from scratch.

## Import method

`Data → Get Data → From File → From Text/CSV → Transform Data` (not "Load" — Transform Data
routes the import through the Power Query Editor so cleaning happens before the data ever lands
on a worksheet).

## Issues found and fixed

| # | Column | Issue | Rows affected | Fix | Tool |
|---|---|---|---|---|---|
| A | `CarrierCode` | Leading whitespace | ~129 | Trim | Transform → Format → Trim |
| B | `OriginCity` | Mixed case + trailing whitespace | ~260 | Trim + Capitalize Each Word | Transform → Format |
| C | `Cancelled` | Mixed `Y/N` and `Yes/No` labels | 259 | Standardize to `Y`/`N` | Replace Values (x2) |
| D | `TailNumber` | Missing values | 519 | Replace null with `"Unknown"` | Custom Column: `if [TailNumber] = null then "Unknown" else [TailNumber]` |
| E | `Distance` | Missing values | 10 | **Left as-is** — see rationale below | — |
| F | (all) | Exact duplicate rows | 20 | Removed | Home → Remove Rows → Remove Duplicates |

## Why issue C mattered most

Pre-fix, a PivotTable count of `Cancelled` returned four categories instead of two:

| Value | Count |
|---|---|
| N | 25,164 |
| Y | 568 |
| No | 254 |
| Yes | 5 |

An unfixed cancellation-rate KPI would have undercounted cancellations by 259 flights with no
error thrown — just a quietly wrong number on the dashboard.

## Why issue E was deliberately not fixed

10 rows / 25,991 = 0.04% of the dataset. `Distance` isn't used in any core on-time KPI (on-time
%, delay minutes, cancellation rate) — only in one secondary "delay by flight length" cut, where
AVERAGE/SUM formulas already skip blanks automatically. Building a merge-query lookup to recover
10 immaterial values costs more effort than it returns. Documented here instead of "fixed" for
the sake of a zero-blanks screenshot.

## Verification

Filter dropdown on `Cancelled` after cleaning shows exactly two values: `Y`, `N`. This same
check (filter dropdown → inspect unique values) is the fast way to spot-check any column after a
cleaning step.
