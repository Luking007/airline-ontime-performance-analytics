# Data Dictionary — Airline On-Time Performance Analytics (FY2025)

## Purpose
Defines every field, KPI calculation, and category boundary used in this project, so any reviewer can verify a number without opening the workbook.

## Data Source
Synthetic dataset modeled on the U.S. DOT/BTS Airline On-Time Performance schema. 25,971 flights across 12 months (Jan–Dec 2025), 6 carriers.

## Carriers
| Code | Carrier |
|---|---|
| AA | American Airlines |
| AS | Alaska Airlines |
| B6 | JetBlue Airways |
| DL | Delta Air Lines |
| UA | United Airlines |
| WN | Southwest Airlines |



## Raw Field Schema
Confirmed columns A–G below. Columns beyond G (destination, delay/time fields) still pending.

| Field | Type | Description |
|---|---|---|
| FlightDate | Date (DD/MM/YYYY) | Scheduled date of the flight |
| Airline | Text | Full carrier name |
| CarrierCode | Text (2-char) | IATA-style carrier code — see Carriers table above |
| FlightNumber | Number | Flight number as filed |
| AircraftType | Text | Aircraft model/variant (e.g. B738, A320) |
| Origin | Text (3-char) | Origin airport IATA code |
| OriginCity | Text | City served by the origin airport |

## KPI Definitions

On-Time % — On-Time Flights ÷ All Scheduled Flights. Cancelled flights count as *not* on-time rather than being excluded from the denominator, matching the U.S. DOT/BTS convention.

Cancellation Rate — Cancelled Flights ÷ All Scheduled Flights

Avg Delay (min) — [PLACEHOLDER — confirm your formula]: averaged across delayed flights only, or across all flights (0 for on-time)? Both are valid; needs to be stated explicitly.

## Delay Category Buckets
| Category | Range |
|---|---|
| On Time | 0–15 min |
| Minor Delay | 16–59 min |
| Moderate Delay | 60–119 min |
| Major Delay | 120+ min |
| Cancelled | Did not operate — counted as not on-time |

## Known Data-Quality Notes
See docs/02_data_cleaning.md for the full cleaning log.