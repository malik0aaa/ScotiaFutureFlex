import { useState, useEffect } from "react";
import { SCOTIA_RED } from "../../constants/colors";
import { GOALS } from "../../constants/data";

export default function OnboardConfirm({ onDone, amount, goal, roundup }) {
  const goalObj = GOALS.find((g) => g.id === goal) || GOALS[0];
  const [shown, setShown] = useState(false);

  useEffect(() => { setTimeout(() => setShown(true), 100); }, []);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", padding: "1.5rem 1.25rem", textAlign: "center" }}>
      <div
        style={{
          width: 56, height: 56, borderRadius: "50%", background: "#E1F5EE",
          display: "flex", alignItems: "center", justifyContent: "center", fontSize: 26,
          marginBottom: "1rem",
          opacity: shown ? 1 : 0,
          transform: shown ? "scale(1)" : "scale(0.6)",
          transition: "all 0.4s cubic-bezier(0.34,1.56,0.64,1)",
        }}
      >
        ✓
      </div>

      <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 22, marginBottom: 6 }}>You&apos;re invested.</div>
      <div style={{ fontSize: 12, color: "rgba(0,0,0,0.5)", lineHeight: 1.6, marginBottom: "1.25rem", maxWidth: 220 }}>
        ${amount} is now growing toward your {goalObj.name.toLowerCase()} goal.
      </div>

      {[
        ["Portfolio", "Balanced Growth"],
        ["Amount",    `$${amount}`],
        ["Account",   "TFSA Starter"],
        ["Goal",      goalObj.name],
      ].map(([l, r]) => (
        <div key={l} style={{ width: "100%", background: "rgba(0,0,0,0.04)", borderRadius: 9, padding: "9px 12px", marginBottom: 6, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span style={{ fontSize: 11, color: "rgba(0,0,0,0.5)" }}>{l}</span>
          <span style={{ fontSize: 12, fontWeight: 500 }}>{r}</span>
        </div>
      ))}

      {roundup && (
        <div style={{ width: "100%", background: "#E1F5EE", borderRadius: 9, padding: "9px 12px", marginBottom: 6, display: "flex", gap: 8, alignItems: "flex-start", textAlign: "left" }}>
          <span style={{ color: "#0F6E56", fontSize: 14 }}>↺</span>
          <span style={{ fontSize: 10, color: "#085041", lineHeight: 1.5 }}>
            Round-up active — your next Tim Hortons purchase of $3.67 will invest <strong>$0.33</strong> automatically.
          </span>
        </div>
      )}

      <div style={{ width: "100%", background: "#FAEEDA", borderRadius: 9, padding: "9px 12px", marginBottom: "1.25rem", display: "flex", alignItems: "center", gap: 8 }}>
        <span style={{ fontSize: 14 }}>⚡</span>
        <span style={{ flex: 1, fontSize: 10, color: "#633806", textAlign: "left", lineHeight: 1.4 }}>
          First deposit complete! You earned XP and unlocked a streak.
        </span>
        <span style={{ fontSize: 14, fontWeight: 500, color: "#854F0B" }}>+150 XP</span>
      </div>

      <div style={{ width: "100%", background: "#FAEEDA", borderRadius: 9, padding: "8px 11px", marginBottom: "1.25rem", textAlign: "left" }}>
        <div style={{ fontSize: 10, color: "#854F0B", lineHeight: 1.5 }}>
          ⚠ Identity verification in progress — deposit up to <strong>$2,500</strong> while we verify. Withdrawals unlock once complete.
        </div>
      </div>

      <button
        onClick={onDone}
        style={{ background: SCOTIA_RED, color: "#fff", border: "none", borderRadius: 12, padding: 13, fontSize: 13, fontWeight: 500, cursor: "pointer", width: "100%", fontFamily: "inherit" }}
      >
        Go to my portfolio →
      </button>
    </div>
  );
}
