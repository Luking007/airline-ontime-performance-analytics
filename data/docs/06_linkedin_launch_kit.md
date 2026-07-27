# LinkedIn Launch Kit — Airline On-Time Performance Dashboard

## Post copy

Airlines lose real money to on-time performance gaps that often go unmeasured until they're
expensive to fix.

I built a full-year on-time performance dashboard — 25,971 flights, 6 carriers, 60 routes — to
find exactly where those gaps live.

The headline finding: fleet-wide on-time rate is 79.75%, but individual carriers range from
85.87% down to 71.10% on largely the *same* routes — a 14.77-point gap that's mostly
carrier-controllable delay, not weather.

I also found something more specific: JFK isn't a problem airport overall. It's specifically
flights *departing* JFK — arrivals into JFK perform fine. That's a cheaper, faster problem to fix
than "audit the whole airport."

Built entirely in Excel — Power Query for cleaning, calculated columns, PivotTables, slicers, no
add-ins. This is stage 1 of a 4-part series solving the same problem in SQL, Python, and Power BI
next.

Full breakdown, methodology, and every bug I found and fixed along the way (including a data-loss
incident I had to root-cause) is documented in the repo — link in the comments.

#DataAnalytics #Excel #AviationAnalytics #BusinessIntelligence #PowerQuery

## Video voiceover script (~50 seconds)

Timing is approximate — read at a natural, conversational pace, not rushed.

---

**[Show full dashboard]**
"I built this on-time performance dashboard for a full year of flight data — twenty-six thousand
flights, six carriers."

**[Click a carrier on the slicer]**
"Every chart here is interactive — filtering by carrier updates the whole view instantly."

**[Show the carrier ranking chart]**
"The headline finding: JetBlue and Alaska fly a lot of the same routes, but there's a fifteen-point
on-time gap between them — and it's mostly carrier-controllable delay, not weather."

**[Show the Top 5 / Bottom 5 route tables]**
"And it's not JFK the airport that's the problem — it's specifically flights departing JFK.
Arrivals there actually perform fine."

**[Zoom back to full dashboard view]**
"Built entirely in Excel — Power Query, PivotTables, slicers, no add-ins. This is stage one of a
four-part series — SQL, Python, and Power BI are next. Full write-up's linked below."

---

**Filming tip:** record the clicks in real time at normal speed rather than speeding up the
screen capture — a hiring manager watching wants to see genuine responsiveness, not an edited
illusion of it.
