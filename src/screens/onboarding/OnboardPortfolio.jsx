import { SCOTIA_RED } from "../../constants/colors";
import { GOALS, AMOUNTS } from "../../constants/data";
import RedHeader from "../../components/ui/RedHeader";
import Card from "../../components/ui/Card";
import Pill from "../../components/ui/Pill";
import Toggle from "../../components/ui/Toggle";

export default function OnboardPortfolio({ onNext, onBack, goal, amount, setAmount, roundup, setRoundup }) {
  const goalObj = GOALS.find((g) => g.id === goal) || GOALS[0];

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%", overflowY: "auto" }}>
      <RedHeader title="Your portfolio" sub={`Curated for ${goalObj.name.toLowerCase()}`} onBack={onBack}>
        <div style={{ display: "flex", gap: 5, marginTop: 10 }}>
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              style={{ height: 3, borderRadius: 2, background: i === 2 ? "#fff" : "rgba(255,255,255,0.3)", width: i === 2 ? 18 : 8 }}
            />
          ))}
        </div>
      </RedHeader>

      <div style={{ padding: "0.85rem 1rem" }}>
        <Card style={{ marginBottom: "0.85rem" }}>
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 8 }}>
            <div style={{ fontSize: 14, fontWeight: 500 }}>Balanced Growth</div>
            <Pill color="#E1F5EE" textColor="#085041" small>↑ 6.4% avg/yr</Pill>
          </div>
          {[
            ["Canadian equities", 40, SCOTIA_RED],
            ["Global ETFs",       35, "#378ADD"],
            ["Bonds",             25, "#1D9E75"],
          ].map(([label, pct, color]) => (
            <div key={label} style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 5 }}>
              <span style={{ fontSize: 10, color: "rgba(0,0,0,0.5)", width: 100, flexShrink: 0 }}>{label}</span>
              <div style={{ flex: 1, height: 5, background: "rgba(0,0,0,0.07)", borderRadius: 3, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 3 }} />
              </div>
              <span style={{ fontSize: 10, color: "rgba(0,0,0,0.5)", width: 28, textAlign: "right" }}>{pct}%</span>
            </div>
          ))}
          <button style={{ fontSize: 11, color: SCOTIA_RED, background: "none", border: "none", padding: 0, marginTop: 4, cursor: "pointer", fontFamily: "inherit" }}>
            ⓘ Why this portfolio?
          </button>
        </Card>

        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 8 }}>
          <span style={{ fontSize: 12, color: "rgba(0,0,0,0.5)" }}>First deposit</span>
          <span style={{ fontSize: 22, fontWeight: 500 }}>${amount}</span>
        </div>

        <div style={{ display: "flex", gap: 6, marginBottom: "0.85rem", flexWrap: "wrap" }}>
          {AMOUNTS.map((a) => (
            <button
              key={a}
              onClick={() => setAmount(a)}
              style={{
                fontSize: 11, padding: "5px 11px", borderRadius: 100,
                border: amount === a ? "none" : "0.5px solid rgba(0,0,0,0.15)",
                background: amount === a ? SCOTIA_RED : "transparent",
                color: amount === a ? "#fff" : "rgba(0,0,0,0.5)",
                cursor: "pointer", fontFamily: "inherit", fontWeight: amount === a ? 500 : 400,
              }}
            >
              ${a}
            </button>
          ))}
        </div>

        <div style={{ background: "#FAEEDA", borderRadius: 10, padding: "9px 11px", display: "flex", alignItems: "center", gap: 8, marginBottom: "0.85rem" }}>
          <div style={{ flex: 1 }}>
            <div style={{ fontSize: 11, fontWeight: 500, color: "#633806" }}>Round-up investing</div>
            <div style={{ fontSize: 10, color: "#854F0B", lineHeight: 1.4, marginTop: 2 }}>
              Spare change from every purchase auto-invests to your TFSA
            </div>
          </div>
          <Toggle on={roundup} onChange={setRoundup} />
        </div>

        <button
          onClick={onNext}
          style={{ background: SCOTIA_RED, color: "#fff", border: "none", borderRadius: 12, padding: 13, fontSize: 13, fontWeight: 500, cursor: "pointer", width: "100%", fontFamily: "inherit" }}
        >
          Invest now — from Scotia chequing
        </button>
        <div style={{ fontSize: 10, color: "rgba(0,0,0,0.4)", textAlign: "center", marginTop: 6 }}>
          TFSA-eligible · Cancel anytime
        </div>
      </div>
    </div>
  );
}
