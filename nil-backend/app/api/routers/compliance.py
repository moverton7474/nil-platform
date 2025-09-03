from fastapi import APIRouter
from ...models.schemas import NILContract, ComplianceValidation, BudgetScenario, ComplianceSimulation
from ...services.compliance_service import ComplianceService

router = APIRouter()
svc = ComplianceService()


@router.post("/offers/validate", response_model=ComplianceValidation)
def validate_offer(contract: NILContract):
    return svc.validate_contract(contract)


@router.post("/offers/simulate-compliance", response_model=ComplianceSimulation)
def simulate(scenario: BudgetScenario):
    return svc.simulate_budget(scenario)
