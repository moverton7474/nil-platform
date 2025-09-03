from typing import List
from ..models.schemas import NILContract, ComplianceValidation, BudgetScenario, ComplianceSimulation, BudgetTier
from ..core.config import HOUSE_CAP, REPORTING_THRESHOLD, BUDGET_TIER_CONFIG


class ComplianceService:
    def validate_contract(self, contract: NILContract) -> ComplianceValidation:
        violations: List[str] = []
        if contract.amount < 0:
            violations.append("negative_amount")
        if contract.amount >= REPORTING_THRESHOLD:
            pass
        tier_cfg = BUDGET_TIER_CONFIG[contract.budget_tier.value]
        if contract.amount > tier_cfg["max_individual"]:
            violations.append("exceeds_individual_cap")
        if contract.amount > HOUSE_CAP:
            violations.append("exceeds_house_cap")
        evidence = []
        if contract.amount >= REPORTING_THRESHOLD:
            evidence.append("disclosure_required")
        valid = len(violations) == 0
        return ComplianceValidation(valid=valid, violations=violations, evidence_required=evidence)

    def simulate_budget(self, scenario: BudgetScenario) -> ComplianceSimulation:
        tier_cfg = BUDGET_TIER_CONFIG[scenario.budget_tier.value]
        total = sum(scenario.allocations.values()) if scenario.allocations else 0.0
        cap_util = min(1.0, total / tier_cfg["total_budget"]) if tier_cfg["total_budget"] > 0 else 0.0
        warnings: List[str] = []
        if total > tier_cfg["total_budget"]:
            warnings.append("over_budget")
        obligations: List[str] = []
        for k, v in (scenario.allocations or {}).items():
            if v >= REPORTING_THRESHOLD:
                obligations.append(f"report_{k}")
        return ComplianceSimulation(cap_utilization=cap_util, warnings=warnings, reporting_obligations=obligations)
