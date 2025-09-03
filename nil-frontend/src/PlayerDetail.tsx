import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiGet } from "./api/client";
import type { Player } from "./types";

type Baron = {
  player_name: string;
  production_score: number;
  player_market_value: number;
  value_per_dollar: number;
  comparable_market_value: number;
  comparable_value_per_dollar: number;
  similarity_score: number;
};

export default function PlayerDetail() {
  const { id } = useParams();
  const [player, setPlayer] = useState<Player | null>(null);
  const [baron, setBaron] = useState<Baron | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      if (!id) return;
      setLoading(true);
      const p = await apiGet<Player>(`/api/v1/players/${id}`);
      setPlayer(p);
      const b = await apiGet<Baron>(`/api/v1/players/${id}/baron`);
      setBaron(b);
      setLoading(false);
    }
    load();
  }, [id]);

  if (loading) return <div className="p-6">Loading...</div>;
  if (!player) return <div className="p-6">Not found</div>;

  return (
    <div className="p-6 space-y-4">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">{player.name} • {player.position}</h1>
        <Link to="/" className="text-sm underline">Back</Link>
      </div>
      <div className="text-sm text-zinc-600">
        {player.conference_level} • {player.school ?? ""} • ${player.market_value.toLocaleString()}
      </div>
      <div className="grid gap-2">
        <div className="border rounded p-3">
          <div className="font-semibold mb-1">Moneyball Metrics</div>
          <div className="text-sm">
            Production: {player.metrics?.production_score ?? "-"} • Efficiency: {player.metrics?.efficiency_rating ?? "-"} • Impact: {player.metrics?.positional_impact ?? "-"}
          </div>
          <div className="text-sm">
            Adjusted Value: {player.metrics?.adjusted_value?.toFixed?.(2) ?? "-"} • Value/$: {player.metrics ? player.metrics.value_per_dollar.toFixed(2) : "-"}
          </div>
        </div>
        {baron && (
          <div className="border rounded p-3">
            <div className="font-semibold mb-1">Baron Hopson Comparison</div>
            <div className="text-sm">
              Production: {baron.production_score} • Value/$: {baron.value_per_dollar.toFixed(2)} • Similarity: {baron.similarity_score.toFixed(1)}
            </div>
            <div className="text-sm">
              Comparable SEC MV: ${baron.comparable_market_value.toLocaleString()} • SEC Value/$: {baron.comparable_value_per_dollar}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
