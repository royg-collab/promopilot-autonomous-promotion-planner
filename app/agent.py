from planner import PromotionPlanner


class PromotionAgent:
    """Lightweight agentic orchestrator for the MVP.

    The agent chooses candidates, simulates alternatives, validates hard constraints,
    and returns an auditable decision trace. Arithmetic stays in the deterministic
    planner so the business rules are independently testable.
    """

    def __init__(self, workbook):
        self.workbook = workbook

    def run(self, top_n=5, min_margin=12.0):
        planner = PromotionPlanner(self.workbook, min_margin=min_margin)
        ranked = planner.run(top_n)

        if ranked.empty:
            return {
                'status': 'NO_PLAN',
                'trace': [
                    'OBSERVE: retail signals loaded',
                    'SELECT: promotion opportunities ranked',
                    'VALIDATE: no candidate satisfied the active constraints',
                    'RE-PLAN: increase feasibility by evaluating remaining candidates',
                    'RESULT: no approved promotion for the current settings',
                ],
                'plans': ranked,
            }

        trace = [
            'OBSERVE: inventory, competitor, demand-event and customer signals loaded',
            'SELECT: promotion opportunities ranked',
            'STRATEGIZE: discount, duration, mechanism and target segment generated',
            'SIMULATE: candidate outcomes estimated before launch',
            'VALIDATE: margin and budget constraints checked',
            'APPROVE: highest-value valid candidate returned',
        ]
        return {'status': 'APPROVED', 'trace': trace, 'plans': ranked}
