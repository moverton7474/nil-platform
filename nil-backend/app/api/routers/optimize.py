from fastapi import APIRouter
from ...models.schemas import RosterOptimizationRequest, OptimizationResult, BudgetTier
from ...core.config import BUDGET_TIER_CONFIG
from ...data.seed import DATA
from ...services.evaluation_service import MoneyballPlayerEvaluator
from ...services.optimization_service import GreedyRosterOptimizer

router = APIRouter()
evaluator = MoneyballPlayerEvaluator()
optimizer = GreedyRosterOptimizer()


@router.post("/optimize/roster", response_model=OptimizationResult)
def optimize_roster(req: RosterOptimizationRequest):
    cfg = BUDGET_TIER_CONFIG[req.budget_tier.value]
    players = []
    for p in DATA:
        pp = p
        pp.metrics = evaluator.calc_metrics(pp, cfg["fcs_bonus"])
        players.append(pp)
    max_ind = req.max_individual if req.max_individual is not None else cfg["max_individual"]
    return optimizer.optimize(players, req.total_budget, req.position_requirements, max_ind)
