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
Confirmed columns A–AB below, read directly from AirlineOTP_Dashboard.xlsm — the actual file in this repo. (An earlier version of this table was built against a different file with an incompatible schema and has been fully replaced.)

| Field | Type | Description |
|---|---|---|
| FlightDate | Date (DD/MM/YYYY) | Scheduled date of the flight |
| Airline | Text | Full carrier name |
| CarrierCode | Text (2-char) | IATA-style carrier code |
| FlightNumber | Number | Flight number as filed |
| TailNumber | Text | Aircraft registration ("Unknown" for some rows) |
| AircraftType | Text | Aircraft model/variant |
| Origin | Text (3-char) | Origin airport IATA code |
| OriginCity | Text | City served by origin airport |
| Destination | Text (3-char) | Destination airport IATA code |
| DestCity | Text | City served by destination airport |
| ScheduledDeparture | Datetime | Planned departure |
| ActualDeparture | Datetime | Actual departure (blank if cancelled) |
| ScheduledArrival | Datetime | Planned arrival |
| ActualArrival | Datetime | Actual arrival (blank if cancelled) |
| Cancelled | Text (Y/N) | Whether the flight operated |
| CancellationReason | Text | e.g. "Carrier" — blank if the flight operated |
| Diverted | Text (Y/N) | Whether the flight diverted from its scheduled destination |
| CarrierDelayMin | Number | Delay minutes attributed to the carrier |
| WeatherDelayMin | Number | Delay minutes attributed to weather |
| NASDelayMin | Number | Delay minutes attributed to the National Airspace System |
| SecurityDelayMin | Number | Delay minutes attributed to security |
| LateAircraftDelayMin | Number | Delay minutes attributed to a late inbound aircraft |
| Distance | Number | Route distance |
| ArrivalDelayMinutes | Number | Arrival delay (negative = early); the canonical figure used for on-time status |
| IsDelayed | Text (Y/N) | Whether ArrivalDelayMinutes exceeds the on-time threshold |
| DelayCategory | Text (derived) | On Time / Minor / Moderate / Major / On Time / Minor / Moderate / Major / Cancelled / Unknown — feeds the Delay Category pie chart directly |
| DayType | Text (derived) | "Weekday" / "Weekend" — feeds that chart directly |
| FlightMonth | Text (derived) | e.g. "Jan 2025" — feeds the FlightMonth slicer |

## KPI Definitions

On-Time % — On-Time Flights ÷ All Scheduled Flights. Cancelled flights count as *not* on-time rather than being excluded from the denominator, matching the U.S. DOT/BTS convention.

Cancellation Rate — Cancelled Flights ÷ All Scheduled Flights

Avg Delay (min) — Not a live formula; N3 holds a plain value written by VBA on refresh, most likely from mod_KPIEngine. Very likely averages ArrivalDelayMinutes, but exact scope — all flights vs. delayed-only, cancelled in vs. out — is unconfirmed pending a source check.

## Delay Category Buckets
| Category | Range |
|---|---|
| On Time | 0–15 min |
| Minor Delay | 16–59 min |
| Moderate Delay | 60–119 min |
| Major Delay | 120+ min |
| Cancelled | Did not operate — counted as not on-time |
| Unknown | Not cancelled, but ActualArrival is blank — code path exists, confirmed 0 occurrences in this dataset |

## Known Data-Quality Notes
See docs/02_data_cleaning.md for the full cleaning log.