from typing import Dict, List
from fastapi import APIRouter
from ...services.data_quality_service import DataQualityService
from ...models.schemas import DataQualityValidationResult

router = APIRouter()
dq = DataQualityService()


@router.post("/ingest/players", response_model=DataQualityValidationResult)
def ingest_players(payload: List[Dict]):
    res = dq.validate_batch(payload)
    return res
