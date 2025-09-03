from typing import Dict
from .typing_alias import StrFloatDict


BUDGET_TIER_CONFIG: Dict[str, Dict[str, float]] = {
    "Group5_Low": {"total_budget": 800000.0, "max_individual": 25000.0, "fcs_bonus": 3.5},
    "Group5_High": {"total_budget": 1300000.0, "max_individual": 45000.0, "fcs_bonus": 3.0},
    "Power4_Standard": {"total_budget": 8500000.0, "max_individual": 200000.0, "fcs_bonus": 1.5},
    "Power4_Elite": {"total_budget": 20500000.0, "max_individual": 500000.0, "fcs_bonus": 1.0},
}

HOUSE_CAP = 20500000.0
REPORTING_THRESHOLD = 600.0
