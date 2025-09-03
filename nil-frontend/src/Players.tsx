import { useEffect, useState } from "react";
import { apiGet, apiPost } from "./api/client";
import type { Player, OptimizationResult, RosterOptimizationRequest } from "./types";
import { Button } from "./components/ui/button";
import { Input } from "./components/ui/input";

type ComplianceSim = { cap_utilization: number; warnings: string[]; reporting_obligations: string[] };
type OfferValidation = { valid: boolean; violations: string[]; evidence_required: string[] };

export default function Players() {
  const [players, setPlayers] = useState<Player[]>([]);
  const [filter, setFilter] = useState<string>("LB");
  const [optResult, setOptResult] = useState<OptimizationResult | null>(null);
  const [loading, setLoading] = useState(false);

  const [offerAmount, setOfferAmount] = useState<string>("15000");
  const [offerResult, setOfferResult] = useState<OfferValidation | null>(null);
  const [simResult, setSimResult] = useState<ComplianceSim | null>(null);

  useEffect(() => {
    setLoading(true);
    const qp = filter ? `?position=${encodeURIComponent(filter)}` : "";
    apiGet<Player[]>(`/api/v1/players${qp}`)
      .then(setPlayers)
      .finally(() => setLoading(false));
  }, [filter]);

  async function runOptimize() {
    const req: RosterOptimizationRequest = {
      budget_tier: "Group5_High",
      total_budget: 1300000,
      position_requirements: { LB: 1, WR: 2 },
      max_individual: 45000,
    };
    const res = await apiPost<OptimizationResult>("/api/v1/optimize/roster", req);
    setOptResult(res);
  }

  async function validateOffer() {
    const first = players[0];
    if (!first) return;
    const res = await apiPost<OfferValidation>("/api/v1/offers/validate", {
      athlete_id: first.athlete_id,
      amount: Number(offerAmount || 0),
      term_months: 12,
      school: first.school || "KSU",
      budget_tier: "Group5_High",
    });
    setOfferResult(res);
  }

  async function simulateCompliance() {
    const res = await apiPost<ComplianceSim>("/api/v1/offers/simulate-compliance", {
      budget_tier: "Group5_High",
      allocations: { LB: Number(offerAmount || 0), WR: 26000 },
    });
    setSimResult(res);
  }

  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">NIL Moneyball – Players</h1>

      <div className="flex items-center gap-3">
        <label className="text-sm">Position filter</label>
        <Input
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          placeholder="LB, WR, DL..."
          className="max-w-xs"
        />
        <Button onClick={() => runOptimize()}>Optimize (G5 High)</Button>
      </div>

      <div className="flex items-center gap-3">
        <label className="text-sm">Offer $</label>
        <Input
          value={offerAmount}
          onChange={(e) => setOfferAmount(e.target.value)}
          placeholder="15000"
          className="max-w-xs"
        />
        <Button variant="secondary" onClick={validateOffer}>Validate Offer</Button>
        <Button variant="outline" onClick={simulateCompliance}>Simulate Compliance</Button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : (
        <div className="grid gap-3">
          {players.map((p) => (
            <div key={p.athlete_id} className="border rounded p-3 flex items-center justify-between">
              <div>
                <div className="font-medium">
                  <a className="underline" href={`/player/${p.athlete_id}`}>{p.name}</a> • {p.position}
                </div>
                <div className="text-sm text-zinc-600">
                  {p.conference_level} • {p.school ?? ""} • ${p.market_value.toLocaleString()}
                </div>
              </div>
              <div className="text-right">
                <div className="text-sm">Prod: {p.metrics?.production_score ?? "-"}</div>
                <div className="text-sm">
                  Value/$: {(p.metrics?.value_per_dollar ?? 0).toFixed(2)}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {optResult && (
        <div className="mt-6 border rounded p-3">
          <div className="font-semibold mb-2">Optimization Result</div>
          <div className="text-sm mb-2">
            Cost: ${optResult.total_cost.toLocaleString()} • Remaining: $
            {optResult.remaining_budget.toLocaleString()} • Method: {optResult.method}
          </div>
          <div className="grid gap-2">
            {optResult.selected_players.map((s) => (
              <div key={s.athlete_id} className="flex items-center justify-between text-sm">
                <div>
                  {s.name} • {s.position}
                </div>
                <div>
                  ${s.market_value.toLocaleString()} • V/$ {s.value_per_dollar.toFixed(2)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {(offerResult || simResult) && (
        <div className="mt-6 border rounded p-3">
          <div className="font-semibold mb-2">Compliance</div>
          {offerResult && (
            <div className="text-sm mb-2">
              Offer valid: {String(offerResult.valid)} • Violations: {offerResult.violations.join(", ") || "None"} • Evidence: {offerResult.evidence_required.join(", ") || "None"}
            </div>
          )}
          {simResult && (
            <div className="text-sm">
              Cap Utilization: {(simResult.cap_utilization * 100).toFixed(2)}% • Warnings: {simResult.warnings.join(", ") || "None"} • Reporting: {simResult.reporting_obligations.join(", ") || "None"}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
