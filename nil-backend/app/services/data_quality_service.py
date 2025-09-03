from datetime import datetime, timedelta
from typing import List, Dict
from ..models.schemas import DataQualityValidationResult


class DataQualityService:
    def __init__(self):
        self.block_optimization = False

    def validate_batch(self, data_batch: List[Dict]) -> DataQualityValidationResult:
        issues: List[str] = []
        if not data_batch:
            self.block_optimization = True
            return DataQualityValidationResult(passed=False, issues=["empty_batch"])
        latest_ts = max([item.get("timestamp") or datetime.min for item in data_batch])
        if isinstance(latest_ts, str):
            try:
                latest_ts = datetime.fromisoformat(latest_ts)
            except Exception:
                issues.append("bad_timestamp_format")
                latest_ts = datetime.min
        hours_old = (datetime.now() - latest_ts).total_seconds() / 3600.0
        if hours_old > 24:
            issues.append("stale_data")
        required = ["athlete_id", "name", "position", "games_played"]
        completeness = []
        for item in data_batch:
            complete = sum(1 for f in required if item.get(f)) / len(required)
            completeness.append(complete)
        avg = sum(completeness) / len(completeness)
        if avg < 0.85:
            issues.append("low_completeness")
        passed = len(issues) == 0
        self.block_optimization = not passed
        return DataQualityValidationResult(passed=passed, issues=issues)
