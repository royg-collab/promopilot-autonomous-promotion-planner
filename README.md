# PromoPilot — Autonomous Promotion Planner Agent

## Hackathon MVP
PromoPilot is an agentic-style promotion planning system for an electronics retailer. It combines inventory, competitor pricing, demand events, customer segments and product relationships to select products, propose promotion strategies, validate constraints and simulate outcomes.

## Core flow
Data ingestion → opportunity scoring → promotion strategy → discount simulation → constraint validation → re-planning → final recommendation.

## Retail features demonstrated
1. Product selection
2. Promotion mechanism selection
3. Discount optimization
4. Cannibalization/product relationship awareness (relationship data included)
5. Product relationships
6. Inventory constraints
7. Geographic customization
8. Competitor awareness
9. Promotion simulation

## Run locally
```bash
pip install -r requirements.txt
streamlit run app/app.py
```

## Important design choice
Deterministic Python handles arithmetic, constraints and simulation. An LLM/agent layer can be placed over this trusted calculation layer for strategy reasoning and natural-language explanations. This reduces hallucination risk while preserving an agentic workflow.

## Agentic behavior
The orchestrator autonomously moves through Observe → Select → Strategize → Simulate → Validate → Approve. Failed candidates can be rejected by the deterministic validator and replaced by another candidate. The calculation layer is deliberately kept outside the language model.
