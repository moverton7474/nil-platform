import BaronHopsonCard from "./BaronHopsonCard";
import MarketMatrix from "./MarketMatrix";

export default function Home() {
  return (
    <div className="p-6 space-y-6">
      <h1 className="text-2xl font-semibold">NIL Moneyball</h1>
      <BaronHopsonCard />
      <MarketMatrix />
    </div>
  );
}
