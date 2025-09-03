export type BudgetTier = "Group5_Low" | "Group5_High" | "Power4_Standard" | "Power4_Elite";
export type Position = "QB" | "RB" | "WR" | "TE" | "OL" | "DL" | "LB" | "DB" | "K" | "P";

export interface PlayerStats {
  total_tackles?: number;
  solo_tackles?: number;
  assisted_tackles?: number;
  games_played: number;
  conference?: string | null;
}

export interface MoneyballMetrics {
  production_score: number;
  efficiency_rating: number;
  positional_impact: number;
  adjusted_value: number;
  value_per_dollar: number;
  fcs_transfer_multiplier: number;
}

export interface Player {
  athlete_id: string;
  name: string;
  position: Position;
  conference_level: "FCS" | "Group5" | "Power4";
  school?: string | null;
  transfer_from?: string | null;
  stats: PlayerStats;
  market_value: number;
  metrics?: MoneyballMetrics;
}

export interface RosterOptimizationRequest {
  budget_tier: BudgetTier;
  total_budget: number;
  position_requirements: Partial<Record<Position, number>>;
  max_individual?: number | null;
}

export interface OptimizationSelectedPlayer {
  athlete_id: string;
  name: string;
  position: Position;
  market_value: number;
  adjusted_value: number;
  value_per_dollar: number;
}

export interface OptimizationResult {
  success: boolean;
  selected_players: OptimizationSelectedPlayer[];
  total_cost: number;
  total_value: number;
  remaining_budget: number;
  method: string;
}
