from typing import Dict
from ..models.schemas import Player, MoneyballMetrics, ConferenceLevel


class MoneyballPlayerEvaluator:
    def __init__(self):
        self.lb_scale = 8.0
        self.solo_weight = 20.0

    def conference_multiplier(self, level: ConferenceLevel) -> float:
        if level == ConferenceLevel.FCS:
            return 1.0
        if level == ConferenceLevel.GROUP5:
            return 1.05
        return 1.1

    def calc_production_score(self, player: Player) -> int:
        if player.position.value == "LB":
            gp = max(player.stats.games_played or 1, 1)
            tackles_pg = (player.stats.total_tackles or 0) / gp
            total = max(player.stats.total_tackles or 0, 1)
            solo_pct = (player.stats.solo_tackles or 0) / total
            base = (tackles_pg * self.lb_scale) + (solo_pct * self.solo_weight)
            score = int(min(100, base * self.conference_multiplier(player.conference_level)))
            return score
        return 50

    def fcs_transfer_multiplier(self, player: Player, tier_bonus: float) -> float:
        if (player.transfer_from or "").upper() == "FCS":
            return tier_bonus
        return 1.0

    def calc_metrics(self, player: Player, tier_bonus: float) -> MoneyballMetrics:
        production = self.calc_production_score(player)
        efficiency = 85
        impact = 80
        fcs_mult = self.fcs_transfer_multiplier(player, tier_bonus)
        adjusted = (production + efficiency + impact) / 3.0
        adjusted *= fcs_mult
        mv = max(player.market_value, 1.0)
        vpd = adjusted / (mv / 1000.0)
        return MoneyballMetrics(
            production_score=production,
            efficiency_rating=efficiency,
            positional_impact=impact,
            adjusted_value=adjusted,
            value_per_dollar=vpd,
            fcs_transfer_multiplier=fcs_mult,
        )

    def baron_hopson_similarity(self, player: Player, metrics: MoneyballMetrics) -> float:
        target_prod = 92.0
        target_vpd = 6.57
        prod_diff = abs(metrics.production_score - target_prod)
        prod_score = max(0.0, 100.0 - prod_diff)
        vpd_ratio = metrics.value_per_dollar / max(target_vpd, 0.01)
        vpd_score = min(vpd_ratio, 2.0) * 50.0
        pos_score = 50.0 if player.position.value == "LB" else 0.0
        score = min(100.0, 0.4 * prod_score + 0.4 * vpd_score + 0.2 * pos_score)
        return score
