# 3-Minute Demo Script

**0:00–0:20 — Problem**
“Retail promotions require balancing inventory, competitor pricing, customer behavior and margin constraints. Manual planning is slow and difficult to optimize.”

**0:20–0:45 — Solution**
“PromoPilot is an autonomous promotion planner. It ingests five business signals, generates promotion candidates, simulates them, validates constraints and re-plans when a candidate fails.”

**0:45–1:30 — Live prototype**
Show the dashboard. Explain the ranked recommendations. Select the top product and show the decision trace: excess inventory, aging, competitor pressure and customer sensitivity.

**1:30–2:15 — Simulation and constraints**
Show discount candidates. Explain that discounts violating minimum margin are rejected. The planner selects the strongest valid candidate and estimates 14-day units, revenue and margin.

**2:15–2:40 — Agentic loop**
“Instead of asking an LLM to make unsupported guesses, we give the reasoning agent trusted calculations. If simulation or constraints fail, the planner re-plans. This creates a measurable agentic loop.”

**2:40–3:00 — Impact**
“PromoPilot can reduce manual promotion analysis, protect margin and focus promotions where inventory and market signals justify action. The architecture is extensible to live retail data and enterprise policy constraints.”
