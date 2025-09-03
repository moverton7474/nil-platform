from typing import Dict, List
from ..models.schemas import Player, OptimizationResult, OptimizationSelectedPlayer, Position


class GreedyRosterOptimizer:
    def __init__(self):
        pass

    def optimize(self, players: List[Player], total_budget: float, position_requirements: Dict[Position, int], max_individual: float) -> OptimizationResult:
        sorted_players = sorted(players, key=lambda p: (p.metrics.value_per_dollar if p.metrics else 0), reverse=True)
        selected: List[OptimizationSelectedPlayer] = []
        remaining = total_budget
        pos_counts: Dict[str, int] = {p.value: 0 for p in position_requirements.keys()}
        for p in sorted_players:
            if p.market_value > remaining:
                continue
            if p.market_value > max_individual:
                continue
            need_met = True
            if p.position in position_requirements:
                if pos_counts[p.position.value] < position_requirements[p.position]:
                    need_met = True
                else:
                    need_met = False
            if need_met:
                mv = float(p.market_value)
                av = float(p.metrics.adjusted_value if p.metrics else 0.0)
                vpd = float(p.metrics.value_per_dollar if p.metrics else 0.0)
                selected.append(OptimizationSelectedPlayer(athlete_id=p.athlete_id, name=p.name, position=p.position, market_value=mv, adjusted_value=av, value_per_dollar=vpd))
                remaining -= mv
                pos_counts[p.position.value] = pos_counts.get(p.position.value, 0) + 1
            if remaining <= 0:
                break
        total_cost = sum(s.market_value for s in selected)
        total_value = sum(s.adjusted_value for s in selected)
        return OptimizationResult(success=True, selected_players=selected, total_cost=total_cost, total_value=total_value, remaining_budget=remaining, method="greedy_heuristic")
