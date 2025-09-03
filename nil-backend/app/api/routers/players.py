from typing import List, Optional
from fastapi import APIRouter, Query
from ...models.schemas import Player, Position, ConferenceLevel, MoneyballMetrics, BaronHopsonAnalysis
from ...services.evaluation_service import MoneyballPlayerEvaluator
from ...core.config import BUDGET_TIER_CONFIG
from ...data.seed import DATA, TIER_FOR_GROUP5_HIGH

router = APIRouter()
evaluator = MoneyballPlayerEvaluator()


@router.get("/players", response_model=List[Player])
def list_players(position: Optional[Position] = Query(None), conference_level: Optional[ConferenceLevel] = Query(None)):
    items = DATA.copy()
    if position:
        items = [p for p in items if p.position == position]
    if conference_level:
        items = [p for p in items if p.conference_level == conference_level]
    cfg = BUDGET_TIER_CONFIG[TIER_FOR_GROUP5_HIGH]
    for p in items:
        p.metrics = evaluator.calc_metrics(p, cfg["fcs_bonus"])
    items.sort(key=lambda x: x.metrics.value_per_dollar if x.metrics else 0.0, reverse=True)
    return items


@router.get("/players/{athlete_id}", response_model=Player)
def player_detail(athlete_id: str):
    cfg = BUDGET_TIER_CONFIG[TIER_FOR_GROUP5_HIGH]
    for p in DATA:
        if p.athlete_id == athlete_id:
            p.metrics = evaluator.calc_metrics(p, cfg["fcs_bonus"])
            return p
    return Player(athlete_id="not_found", name="not_found", position=Position.LB, conference_level=ConferenceLevel.FCS)


@router.get("/players/{athlete_id}/baron", response_model=BaronHopsonAnalysis)
def baron_analysis(athlete_id: str):
    cfg = BUDGET_TIER_CONFIG[TIER_FOR_GROUP5_HIGH]
    p = next((x for x in DATA if x.athlete_id == athlete_id), None)
    if not p:
        return BaronHopsonAnalysis(player_name="not_found", production_score=0, player_market_value=0.0, value_per_dollar=0.0, comparable_market_value=165000.0, comparable_value_per_dollar=0.58, similarity_score=0.0)
    m = evaluator.calc_metrics(p, cfg["fcs_bonus"])
    sim = evaluator.baron_hopson_similarity(p, m)
    return BaronHopsonAnalysis(player_name=p.name, production_score=m.production_score, player_market_value=p.market_value, value_per_dollar=m.value_per_dollar, comparable_market_value=165000.0, comparable_value_per_dollar=0.58, similarity_score=sim)
