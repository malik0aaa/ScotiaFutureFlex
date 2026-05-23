import { useState } from "react";
import { SCOTIA_RED } from "../../constants/colors";
import { TRANSACTIONS } from "../../constants/data";

export default function RoundupsTab() {
  const [mode, setMode] = useState("round");
  const [dest, setDest] = useState("TFSA");

  const total = TRANSACTIONS.reduce((a, t) => a + t.roundup, 0);

  return (
    <div style={{ overflowY: "auto", flex: 1 }}>
      <div style={{ background: SCOTIA_RED, padding: "1rem 1.25rem 0.9rem" }}>
        <div style={{ fontSize: 10, color: "rgba(255,255,255,0.65)", marginBottom: 3 }}>Total invested via round-ups</div>
        <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 30, color: "#fff", marginBottom: 2 }}>
          ${total.toFixed(2)}
        </div>
        <div style={{ fontSize: 10, color: "rgba(255,255,255,0.65)" }}>
          Since May 1, 2025 · from {TRANSACTIONS.length} transactions
        </div>
      </div>

      <div style={{ padding: "1rem" }}>
        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Round-up mode
        </div>
        <div style={{ display: "flex", gap: 7, marginBottom: "1rem" }}>
          {[
            ["round", "Round up",  "Next dollar"],
            ["double","Double up", "2× round-up"],
          ].map(([id, label, sub]) => (
            <div
              key={id}
              onClick={() => setMode(id)}
              style={{
                flex: 1, border: mode === id ? `2px solid ${SCOTIA_RED}` : "0.5px solid rgba(0,0,0,0.12)",
                borderRadius: 10, padding: "8px 10px", cursor: "pointer",
                background: mode === id ? "#fff9f9" : "#fff",
              }}
            >
              <div style={{ fontSize: 11, fontWeight: 500, color: mode === id ? SCOTIA_RED : "#1a1a1a" }}>{label}</div>
              <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)" }}>{sub}</div>
            </div>
          ))}
        </div>

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Destination account
        </div>
        <div style={{ display: "flex", gap: 7, marginBottom: "1rem" }}>
          {[
            ["TFSA", "Tax-free"],
            ["RRSP", "Tax-deferred"],
            ["FHSA", "Home savings"],
          ].map(([d, sub]) => (
            <button
              key={d}
              onClick={() => setDest(d)}
              style={{
                flex: 1, border: dest === d ? `2px solid ${SCOTIA_RED}` : "0.5px solid rgba(0,0,0,0.12)",
                borderRadius: 10, padding: "8px 10px", cursor: "pointer",
                background: dest === d ? "#fff9f9" : "#fff",
                fontFamily: "inherit", textAlign: "center",
              }}
            >
              <div style={{ fontSize: 12, fontWeight: 500, color: dest === d ? SCOTIA_RED : "#1a1a1a" }}>{d}</div>
              <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)" }}>{sub}</div>
            </button>
          ))}
        </div>

        <div style={{ background: "rgba(0,0,0,0.04)", borderRadius: 10, padding: "9px 12px", marginBottom: "1rem", display: "flex", justifyContent: "space-between" }}>
          <span style={{ fontSize: 11, color: "rgba(0,0,0,0.5)" }}>Pending today</span>
          <span style={{ fontSize: 13, fontWeight: 500, color: "#0F6E56" }}>+$0.33 → {dest}</span>
        </div>

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Recent round-ups
        </div>
        {TRANSACTIONS.map((tx) => (
          <div key={tx.name} style={{ display: "flex", alignItems: "center", gap: 9, paddingBottom: 9, marginBottom: 9, borderBottom: "0.5px solid rgba(0,0,0,0.07)" }}>
            <div style={{ width: 32, height: 32, borderRadius: 8, background: "rgba(0,0,0,0.05)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, flexShrink: 0 }}>
              {tx.icon}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 11, fontWeight: 500 }}>{tx.name}</div>
              <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)" }}>{tx.time}</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 11, color: "rgba(0,0,0,0.45)" }}>${tx.spent.toFixed(2)}</div>
              <div style={{ fontSize: 11, fontWeight: 500, color: "#0F6E56" }}>
                +${(mode === "double" ? tx.roundup * 2 : tx.roundup).toFixed(2)} → {dest}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
