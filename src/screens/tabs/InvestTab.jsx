import { useState } from "react";
import { SCOTIA_RED } from "../../constants/colors";
import RedHeader from "../../components/ui/RedHeader";

export default function InvestTab({ xp, setXp }) {
  const [dep, setDep]   = useState(50);
  const [done, setDone] = useState(false);

  const handleInvest = () => {
    setXp((x) => x + dep);
    setDone(true);
    setTimeout(() => setDone(false), 2500);
  };

  return (
    <div style={{ overflowY: "auto", flex: 1 }}>
      <RedHeader title="Invest" sub="Add to your Balanced Growth portfolio" />

      <div style={{ padding: "1rem" }}>
        {done && (
          <div style={{ background: "#E1F5EE", borderRadius: 10, padding: "10px 12px", marginBottom: "1rem", display: "flex", gap: 8, alignItems: "center" }}>
            <span style={{ fontSize: 14, color: "#0F6E56" }}>✓</span>
            <span style={{ fontSize: 11, color: "#085041", fontWeight: 500 }}>+${dep} invested! +{dep} XP earned.</span>
          </div>
        )}

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Amount
        </div>
        <div style={{ fontSize: 28, fontWeight: 500, textAlign: "center", margin: "0.75rem 0" }}>${dep}</div>
        <input
          type="range" min={10} max={500} step={10} value={dep}
          onChange={(e) => setDep(Number(e.target.value))}
          style={{ width: "100%", marginBottom: "0.75rem", accentColor: SCOTIA_RED }}
        />

        <div style={{ display: "flex", gap: 6, marginBottom: "1rem", flexWrap: "wrap" }}>
          {[25, 50, 100, 200, 500].map((a) => (
            <button
              key={a}
              onClick={() => setDep(a)}
              style={{
                fontSize: 11, padding: "5px 11px", borderRadius: 100,
                border: dep === a ? "none" : "0.5px solid rgba(0,0,0,0.15)",
                background: dep === a ? SCOTIA_RED : "transparent",
                color: dep === a ? "#fff" : "rgba(0,0,0,0.5)",
                cursor: "pointer", fontFamily: "inherit",
              }}
            >
              ${a}
            </button>
          ))}
        </div>

        <div style={{ background: "#FAEEDA", borderRadius: 10, padding: "9px 11px", marginBottom: "1rem" }}>
          <div style={{ fontSize: 11, fontWeight: 500, color: "#633806" }}>XP you&apos;ll earn</div>
          <div style={{ fontSize: 20, fontWeight: 500, color: "#854F0B" }}>+{dep} XP</div>
          <div style={{ fontSize: 10, color: "#854F0B" }}>Scales with deposit · current balance: {xp} XP</div>
        </div>

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Portfolio allocation
        </div>
        {[
          ["Canadian equities", 40, SCOTIA_RED],
          ["Global ETFs",       35, "#378ADD"],
          ["Bonds",             25, "#1D9E75"],
        ].map(([label, pct, color]) => (
          <div key={label} style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 6 }}>
            <span style={{ fontSize: 10, color: "rgba(0,0,0,0.5)", width: 110, flexShrink: 0 }}>{label}</span>
            <div style={{ flex: 1, height: 5, background: "rgba(0,0,0,0.07)", borderRadius: 3, overflow: "hidden" }}>
              <div style={{ height: "100%", width: `${pct}%`, background: color, borderRadius: 3 }} />
            </div>
            <span style={{ fontSize: 10, color: "rgba(0,0,0,0.5)", width: 28, textAlign: "right" }}>{pct}%</span>
          </div>
        ))}

        <button
          onClick={handleInvest}
          style={{ background: SCOTIA_RED, color: "#fff", border: "none", borderRadius: 12, padding: 13, fontSize: 13, fontWeight: 500, cursor: "pointer", width: "100%", marginTop: "1rem", fontFamily: "inherit" }}
        >
          Invest ${dep} now
        </button>
        <div style={{ fontSize: 10, color: "rgba(0,0,0,0.35)", textAlign: "center", marginTop: 6 }}>
          TFSA · From Scotia chequing · CDIC protected
        </div>
      </div>
    </div>
  );
}
