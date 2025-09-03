from enum import Enum
from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ConferenceLevel(str, Enum):
    FCS = "FCS"
    GROUP5 = "Group5"
    POWER4 = "Power4"


class BudgetTier(str, Enum):
    GROUP5_LOW = "Group5_Low"
    GROUP5_HIGH = "Group5_High"
    POWER4_STANDARD = "Power4_Standard"
    POWER4_ELITE = "Power4_Elite"


class Position(str, Enum):
    QB = "QB"
    RB = "RB"
    WR = "WR"
    TE = "TE"
    OL = "OL"
    DL = "DL"
    LB = "LB"
    DB = "DB"
    K = "K"
    P = "P"


class PlayerStats(BaseModel):
    total_tackles: Optional[int] = 0
    solo_tackles: Optional[int] = 0
    assisted_tackles: Optional[int] = 0
    games_played: int = 1
    conference: Optional[str] = None


class MoneyballMetrics(BaseModel):
    production_score: int
    efficiency_rating: int
    positional_impact: int
    adjusted_value: float
    value_per_dollar: float
    fcs_transfer_multiplier: float = 1.0


class Player(BaseModel):
    athlete_id: str
    name: str
    position: Position
    conference_level: ConferenceLevel
    school: Optional[str] = None
    transfer_from: Optional[str] = None
    stats: PlayerStats = Field(default_factory=PlayerStats)
    market_value: float = 0.0
    metrics: Optional[MoneyballMetrics] = None


class BaronHopsonAnalysis(BaseModel):
    player_name: str
    production_score: int
    player_market_value: float
    value_per_dollar: float
    comparable_market_value: float
    comparable_value_per_dollar: float
    similarity_score: float


class RosterOptimizationRequest(BaseModel):
    budget_tier: BudgetTier
    total_budget: float
    position_requirements: Dict[Position, int] = Field(default_factory=dict)
    max_individual: Optional[float] = None


class OptimizationSelectedPlayer(BaseModel):
    athlete_id: str
    name: str
    position: Position
    market_value: float
    adjusted_value: float
    value_per_dollar: float


class OptimizationResult(BaseModel):
    success: bool
    selected_players: List[OptimizationSelectedPlayer]
    total_cost: float
    total_value: float
    remaining_budget: float
    method: str


class NILContract(BaseModel):
    athlete_id: str
    amount: float
    term_months: int = 12
    school: Optional[str] = None
    budget_tier: BudgetTier


class ComplianceValidation(BaseModel):
    valid: bool
    violations: List[str] = Field(default_factory=list)
    evidence_required: List[str] = Field(default_factory=list)


class BudgetScenario(BaseModel):
    budget_tier: BudgetTier
    allocations: Dict[str, float] = Field(default_factory=dict)


class ComplianceSimulation(BaseModel):
    cap_utilization: float
    warnings: List[str] = Field(default_factory=list)
    reporting_obligations: List[str] = Field(default_factory=list)


class DataQualityValidationResult(BaseModel):
    passed: bool
    issues: List[str] = Field(default_factory=list)
