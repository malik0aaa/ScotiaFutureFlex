import { useState } from "react";
import { SCOTIA_RED } from "../../constants/colors";
import { REWARDS } from "../../constants/data";
import Pill from "../../components/ui/Pill";

const TIERS = [
  { name: "Starter", range: "0–499 XP",    icon: "◎", color: "#888780", minXP: 0,    maxXP: 500  },
  { name: "Spark",   range: "500–999 XP",  icon: "🔥", color: SCOTIA_RED, minXP: 500,  maxXP: 1000 },
  { name: "Gold",    range: "1000–2499 XP",icon: "🏆", color: "#BA7517", minXP: 1000, maxXP: 2500 },
  { name: "Vault",   range: "2500+ XP",    icon: "◆", color: "#534AB7", minXP: 2500, maxXP: Infinity },
];

function RedeemModal({ reward, xp, onConfirm, onCancel }) {
  return (
    <div style={{ minHeight: 520, background: "rgba(0,0,0,0.45)", display: "flex", alignItems: "center", justifyContent: "center", padding: "1rem" }}>
      <div style={{ background: "#fff", borderRadius: 16, padding: "1.5rem", width: "100%", maxWidth: 260, textAlign: "center" }}>
        <div style={{ width: 52, height: 52, borderRadius: 14, background: "#E1F5EE", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24, margin: "0 auto 0.75rem" }}>
          ⊘
        </div>
        <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 18, marginBottom: 4 }}>Redeem reward</div>
        <div style={{ fontSize: 11, color: "rgba(0,0,0,0.5)", marginBottom: "1rem" }}>{reward.name}</div>

        {[
          ["Reward",    reward.name],
          ["XP cost",   `${reward.cost} XP`],
          ["Remaining", `${xp - reward.cost} XP`],
        ].map(([l, r]) => (
          <div key={l} style={{ display: "flex", justifyContent: "space-between", background: "rgba(0,0,0,0.04)", borderRadius: 8, padding: "8px 10px", marginBottom: 6 }}>
            <span style={{ fontSize: 11, color: "rgba(0,0,0,0.5)" }}>{l}</span>
            <span style={{ fontSize: 11, fontWeight: 500, color: l === "XP cost" ? "#854F0B" : "#1a1a1a" }}>{r}</span>
          </div>
        ))}

        <button onClick={onConfirm} style={{ background: SCOTIA_RED, color: "#fff", border: "none", borderRadius: 10, padding: 11, fontSize: 12, fontWeight: 500, cursor: "pointer", width: "100%", marginTop: "0.75rem", fontFamily: "inherit" }}>
          Confirm
        </button>
        <button onClick={onCancel} style={{ background: "none", border: "none", fontSize: 11, color: "rgba(0,0,0,0.4)", marginTop: 8, cursor: "pointer", fontFamily: "inherit" }}>
          Cancel
        </button>
      </div>
    </div>
  );
}

export default function RewardsTab({ xp, setXp }) {
  const [redeeming, setRedeeming] = useState(null);
  const [redeemed, setRedeemed]   = useState([]);

  const handleConfirm = () => {
    if (xp >= redeeming.cost && !redeemed.includes(redeeming.id)) {
      setXp((x) => x - redeeming.cost);
      setRedeemed((p) => [...p, redeeming.id]);
      setRedeeming(null);
    }
  };

  const activeTier = [...TIERS].reverse().find((t) => xp >= t.minXP) || TIERS[0];

  if (redeeming) {
    return <RedeemModal reward={redeeming} xp={xp} onConfirm={handleConfirm} onCancel={() => setRedeeming(null)} />;
  }

  return (
    <div style={{ overflowY: "auto", flex: 1 }}>
      <div style={{ background: SCOTIA_RED, padding: "1rem 1.25rem 0.9rem" }}>
        <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 19, color: "#fff", marginBottom: 2 }}>Rewards store</div>
        <div style={{ fontSize: 11, color: "rgba(255,255,255,0.7)" }}>{xp} XP available to spend</div>
        <div style={{ marginTop: 10 }}>
          <div style={{ height: 5, background: "rgba(255,255,255,0.25)", borderRadius: 3, overflow: "hidden" }}>
            <div style={{ height: "100%", width: `${Math.min((xp / 1000) * 100, 100)}%`, background: "#fff", borderRadius: 3, transition: "width 0.6s" }} />
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", marginTop: 4 }}>
            <span style={{ fontSize: 9, color: "rgba(255,255,255,0.6)" }}>Spark Saver · Lv 2</span>
            <span style={{ fontSize: 9, color: "rgba(255,255,255,0.6)" }}>{Math.max(1000 - xp, 0)} XP to Gold</span>
          </div>
        </div>
      </div>

      <div style={{ padding: "1rem" }}>
        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Tier benefits
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 7, marginBottom: "1rem" }}>
          {TIERS.map((t) => {
            const isActive = t.name === activeTier.name;
            return (
              <div key={t.name} style={{ border: isActive ? `2px solid ${t.color}` : "0.5px solid rgba(0,0,0,0.1)", borderRadius: 11, padding: "9px 10px", background: isActive ? "#fff9f9" : "#fff" }}>
                <div style={{ display: "flex", alignItems: "center", gap: 6, marginBottom: 3 }}>
                  <span style={{ fontSize: 14 }}>{t.icon}</span>
                  <span style={{ fontSize: 11, fontWeight: 500, color: isActive ? t.color : "#1a1a1a" }}>{t.name}</span>
                </div>
                <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)", marginBottom: 2 }}>{t.range}</div>
                {isActive && <Pill color={t.color} small>You are here</Pill>}
              </div>
            );
          })}
        </div>

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Available rewards
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8 }}>
          {REWARDS.map((r) => {
            const isRedeemed = redeemed.includes(r.id);
            const canAfford  = xp >= r.cost;
            const actionable = r.available && canAfford && !isRedeemed;
            return (
              <div key={r.id} style={{ border: "0.5px solid rgba(0,0,0,0.1)", borderRadius: 12, padding: "9px 10px", opacity: (!r.available || isRedeemed) ? 0.5 : 1, background: "#fff" }}>
                <div style={{ width: 34, height: 34, borderRadius: 9, background: "rgba(0,0,0,0.05)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 16, marginBottom: 7 }}>
                  {r.icon}
                </div>
                <div style={{ fontSize: 11, fontWeight: 500, marginBottom: 2, lineHeight: 1.3 }}>{r.name}</div>
                <div style={{ fontSize: 9, color: "rgba(0,0,0,0.45)", marginBottom: 6, lineHeight: 1.35 }}>{r.desc}</div>
                <div style={{ display: "flex", alignItems: "center", gap: 5, marginBottom: 6 }}>
                  <span style={{ fontSize: 11 }}>⚡</span>
                  <span style={{ fontSize: 10, fontWeight: 500, color: "#854F0B" }}>{r.cost} XP</span>
                </div>
                <button
                  onClick={() => actionable && setRedeeming(r)}
                  style={{
                    fontSize: 10,
                    background: isRedeemed ? "#E1F5EE" : actionable ? SCOTIA_RED : "rgba(0,0,0,0.08)",
                    color: isRedeemed ? "#085041" : actionable ? "#fff" : "rgba(0,0,0,0.3)",
                    border: "none", borderRadius: 7, padding: "4px 9px",
                    cursor: actionable ? "pointer" : "default",
                    fontFamily: "inherit", fontWeight: 500,
                  }}
                >
                  {isRedeemed ? "Redeemed ✓" : !r.available ? "Locked" : !canAfford ? `Need ${r.cost - xp} more` : "Redeem"}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
