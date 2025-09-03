from typing import List
from fastapi import APIRouter
from ...data.seed import DATA
from ...services.evaluation_service import MoneyballPlayerEvaluator
from ...core.config import BUDGET_TIER_CONFIG
from ...models.schemas import Player

router = APIRouter()
evaluator = MoneyballPlayerEvaluator()


@router.get("/analytics/value-finds", response_model=List[Player])
def value_finds():
    cfg = BUDGET_TIER_CONFIG["Group5_High"]
    items = []
    for p in DATA:
        pp = p
        pp.metrics = evaluator.calc_metrics(pp, cfg["fcs_bonus"])
        if pp.metrics.value_per_dollar > 4.0:
            items.append(pp)
    items.sort(key=lambda x: x.metrics.value_per_dollar if x.metrics else 0.0, reverse=True)
    return items
