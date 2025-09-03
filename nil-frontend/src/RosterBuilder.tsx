import { useState } from "react";
import { apiPost } from "./api/client";
import type { OptimizationResult, RosterOptimizationRequest, Position } from "./types";
import { BudgetTierSelector, BudgetMap } from "./BudgetTierSelector";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";

const POSITIONS: Position[] = ["QB","RB","WR","TE","OL","DL","LB","DB","K","P"];

export default function RosterBuilder() {
  const [tier, setTier] = useState<"Group5_Low" | "Group5_High" | "Power4_Standard" | "Power4_Elite">("Group5_High");
  const [reqs, setReqs] = useState<Partial<Record<Position, number>>>({ WR: 2, DL: 4, LB: 1 });
  const [result, setResult] = useState<OptimizationResult | null>(null);
  const totalBudget = BudgetMap[tier];

  function setReq(pos: Position, v: string) {
    const n = Math.max(0, Number(v || 0));
    setReqs(r => ({ ...r, [pos]: n }));
  }

  async function run() {
    const req: RosterOptimizationRequest = {
      budget_tier: tier,
      total_budget: totalBudget,
      position_requirements: reqs,
    };
    const res = await apiPost<OptimizationResult>("/api/v1/optimize/roster", req);
    setResult(res);
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Roster Builder</h1>
      <BudgetTierSelector value={tier} onChange={setTier} />
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {POSITIONS.map(p => (
          <div key={p} className="flex items-center gap-2">
            <label className="w-10 text-sm">{p}</label>
            <Input className="max-w-[100px]" value={String(reqs[p] ?? 0)} onChange={(e)=>setReq(p, e.target.value)} />
          </div>
        ))}
      </div>
      <Button onClick={run}>Optimize</Button>

      {result && (
        <div className="mt-4 border rounded p-3">
          <div className="text-sm mb-2">
            Cost: ${result.total_cost.toLocaleString()} • Remaining: ${result.remaining_budget.toLocaleString()} • Method: {result.method}
          </div>
          <div className="grid gap-2">
            {result.selected_players.map(s => (
              <div key={s.athlete_id} className="flex items-center justify-between text-sm">
                <div>{s.name} • {s.position}</div>
                <div>${s.market_value.toLocaleString()} • V/$ {s.value_per_dollar.toFixed(2)}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
