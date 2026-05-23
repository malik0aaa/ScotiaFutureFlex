import { SCOTIA_RED } from "../../constants/colors";
import { GOALS } from "../../constants/data";
import RedHeader from "../../components/ui/RedHeader";
import Card from "../../components/ui/Card";

export default function OnboardGoal({ onNext, onBack, goal, setGoal }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <RedHeader title="What's the goal?" sub="Pick one — takes 5 seconds" onBack={onBack}>
        <div style={{ display: "flex", gap: 5, marginTop: 10 }}>
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              style={{ height: 3, borderRadius: 2, background: i === 1 ? "#fff" : "rgba(255,255,255,0.3)", width: i === 1 ? 18 : 8 }}
            />
          ))}
        </div>
      </RedHeader>

      <div style={{ padding: "1rem", flex: 1, display: "flex", flexDirection: "column" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: "1rem", flex: 1 }}>
          {GOALS.map((g) => (
            <Card key={g.id} onClick={() => setGoal(g.id)} accent={goal === g.id} style={{ background: goal === g.id ? "#fff9f9" : "#fff" }}>
              <div style={{ fontSize: 22, marginBottom: 6 }}>{g.icon}</div>
              <div style={{ fontSize: 12, fontWeight: 500, color: "#1a1a1a", marginBottom: 2 }}>{g.name}</div>
              <div style={{ fontSize: 10, color: "rgba(0,0,0,0.5)", lineHeight: 1.4 }}>{g.desc}</div>
            </Card>
          ))}
        </div>

        <button
          onClick={onNext}
          disabled={!goal}
          style={{
            background: goal ? SCOTIA_RED : "rgba(0,0,0,0.1)",
            color: goal ? "#fff" : "rgba(0,0,0,0.3)",
            border: "none", borderRadius: 12, padding: 13, fontSize: 13,
            fontWeight: 500, cursor: goal ? "pointer" : "default", fontFamily: "inherit",
          }}
        >
          See my portfolio →
        </button>
      </div>
    </div>
  );
}
