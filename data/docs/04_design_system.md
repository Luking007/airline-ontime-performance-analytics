# Design System — Dashboard Sheet

Consistent with the dark-navy, Segoe UI visual language used across the portfolio, so this
project reads as one consistent body of work rather than a one-off.

## Palette

| Role | Hex | Used for |
|---|---|---|
| Page background | `#0D1B2A` | Whole Dashboard sheet |
| Panel/card fill | `#14293D` | KPI cards, chart backgrounds |
| Border/structural accent | `#1F4E79` | Card borders, headers, table titles |
| Branding text | `#A8D8F0` | Name/credit line |
| Neutral KPI accent | `#3498DB` | Total Flights |
| Success accent | `#2ECC71` | On-Time %, Top 5 Routes |
| Danger accent | `#E74C3C` | Cancellation Rate, Bottom 5 Routes |
| Warning accent | `#F39C12` | Avg Arrival Delay |
| Chart data color | `#5DADE2` | Bars/lines in all 3 charts |
| Font | Segoe UI | Everywhere |

## Design decisions worth remembering

- **KPI accent colors are semantic, not decorative.** Green/red/amber map to whether a metric is
  "good," "concerning," or "watch this" — not chosen for variety. Total Flights stays neutral
  blue because raw volume has no inherent good/bad direction.
- **Top 5 / Bottom 5 route tables deliberately break the dark theme.** Titles and headers stay
  dark-themed for consistency with the rest of the dashboard, but the 5 data rows underneath each
  table's data bars are kept on a light background on purpose — a colored bar rendered on top of
  an already-dark cell loses contrast on both the bar and the text sitting on it. This is a
  legible-first exception, not an inconsistency.
- **Chart bars/lines use one consistent color (`#5DADE2`) across all three charts**, rather than
  semantic per-category coloring, to avoid a busy, inconsistent look. Only the KPI cards and
  route tables use the full green/red/amber semantic system, since those are the visuals where
  "good vs. bad" is the explicit point.
