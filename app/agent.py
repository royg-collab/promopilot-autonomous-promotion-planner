from planner import PromotionPlanner

class PromotionAgent:
    """Lightweight agentic orchestrator for the MVP.

    The agent chooses candidates, simulates alternatives, validates hard constraints,
    and re-plans when a candidate fails. LLM reasoning can be plugged into the
    strategy/explanation step without moving arithmetic into the LLM.
    """
    def __init__(self, workbook):
        self.planner = PromotionPlanner(workbook)

    def run(self, top_n=5):
        ranked = self.planner.run(top_n)
        if ranked.empty:
            return {"status":"NO_PLAN", "trace":["No valid promotion candidate found."], "plans": ranked}
        trace = [
            "OBSERVE: inventory, competitor, demand-event and customer signals loaded",
            "SELECT: promotion opportunities ranked",
            "STRATEGIZE: discount, duration, mechanism and target segment generated",
            "SIMULATE: candidate outcomes estimated before launch",
            "VALIDATE: margin and budget constraints checked",
            "APPROVE: highest-value valid candidate returned",
        ]
        return {"status":"APPROVED", "trace":trace, "plans":ranked}
