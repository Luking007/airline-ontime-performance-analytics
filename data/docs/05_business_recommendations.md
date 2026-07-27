# Business Recommendations — FY2025 On-Time Performance

## Executive Summary

Across 25,971 flights and 6 carriers, fleet-wide on-time performance sits at **79.75%**, with a
2.20% cancellation rate and a 6.7-minute average arrival delay. The fleet average hides the real
story: individual carrier performance ranges from **85.87% (Alaska)** down to **71.10%
(JetBlue)** — a **14.77-point spread** on largely overlapping route networks. That gap, not the
fleet average, is where the actionable opportunity sits.

## 1. Audit JetBlue's carrier-controllable delay sources

JetBlue trails the fleet average by 8.65 points and the top performer by 14.77 points. Carrier-
attributable delay (1,709 total minutes across the dataset) is the single largest of the five
tracked delay causes — larger than Weather (1,623), despite weather being entirely outside any
airline's control. Since multiple carriers fly the same routes with meaningfully different
results, the gap is more likely explained by controllable factors — crew scheduling, aircraft
turnaround, boarding process — than by which routes JetBlue happens to fly.
**Suggested first step:** pull JetBlue's `CarrierDelayMin` distribution by route and compare
turnaround times directly against Alaska/Delta on the same routes.

## 2. Investigate JFK's departure-side operations specifically, not the airport broadly

JFK appears in 3 of the 5 worst-performing routes (JFK-SFO 73.33%, JFK-MIA 72.56%, JFK-BOS
71.84%) — but SFO-JFK, the *same city pair in the opposite direction*, ranks in the top 5
(86.32%). This directional asymmetry narrows the problem meaningfully: a generic "JFK has bad
weather" or "JFK is congested" explanation would depress both directions roughly equally. It
doesn't. This points specifically at ground operations on the departure side at JFK — a cheaper,
faster problem to scope and fix than an airport-wide review.

## 3. Build seasonal capacity buffers for July and December, not a flat year-round buffer

Average arrival delay peaks in December (9.09 min) and July (8.92 min), well above the 6.66-
minute yearly average, while spring/fall months (May: 4.55, Sep: 5.43) run well under it. This
lines up with known holiday-travel and summer-thunderstorm seasonality rather than random noise.
Padding scheduled block times or pre-positioning extra ground crew specifically in these two
windows — instead of a flat buffer spread evenly across all 12 months — targets the actual
source of the delay average instead of diluting resources into months that don't need them.

## 4. Quantify the cost of the 2.20% cancellation rate

572 cancelled flights currently sit in this dashboard as a rate, not a cost. Even a conservative
per-cancellation estimate (rebooking, compensation, crew repositioning) would convert this into a
dollar figure finance stakeholders can act on directly, rather than a percentage that's easy to
deprioritize against more visibly costly problems.
**Suggested for the next iteration:** add a cost-per-cancellation assumption as a single
adjustable input cell, and have the Cancellation Rate KPI card display both the rate and its
estimated dollar impact side by side.
