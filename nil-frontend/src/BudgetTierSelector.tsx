import { Button } from "./components/ui/button";

type Tier = { key: "Group5_Low" | "Group5_High" | "Power4_Standard" | "Power4_Elite"; label: string; budget: number };
const TIERS: Tier[] = [
  { key: "Group5_Low", label: "Group5 Low", budget: 800_000 },
  { key: "Group5_High", label: "Group5 High", budget: 1_300_000 },
  { key: "Power4_Standard", label: "Power4 Standard", budget: 8_500_000 },
  { key: "Power4_Elite", label: "Power4 Elite", budget: 20_500_000 },
];

export function BudgetTierSelector({ value, onChange }: { value: Tier["key"]; onChange: (v: Tier["key"]) => void }) {
  return (
    <div className="grid grid-cols-2 gap-3">
      {TIERS.map(t => (
        <Button
          key={t.key}
          variant={t.key === value ? "default" : "secondary"}
          onClick={() => onChange(t.key)}
        >
          {t.label} • ${t.budget.toLocaleString()}
        </Button>
      ))}
    </div>
  );
}

export const BudgetMap: Record<Tier["key"], number> = {
  Group5_Low: 800_000,
  Group5_High: 1_300_000,
  Power4_Standard: 8_500_000,
  Power4_Elite: 20_500_000,
};
