import { SCOTIA_RED } from "../../constants/colors";
import { GOALS, TRANSACTIONS } from "../../constants/data";
import { useAnimatedNumber } from "../../hooks/useAnimatedNumber";
import Card from "../../components/ui/Card";
import ProgressBar from "../../components/ui/ProgressBar";

export default function HomeTab({ xp, amount, goal }) {
  const goalObj = GOALS.find((g) => g.id === goal) || GOALS[0];
  const animXP  = useAnimatedNumber(xp);
  const animAmt = useAnimatedNumber(amount * 10 + 262);

  return (
    <div style={{ overflowY: "auto", flex: 1 }}>
      <div style={{ background: SCOTIA_RED, padding: "1.25rem 1.25rem 1rem" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 12 }}>
          <div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.65)", marginBottom: 2 }}>Good morning, Alex</div>
            <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 20, color: "#fff" }}>Your portfolio</div>
          </div>
          <div style={{ width: 34, height: 34, borderRadius: "50%", background: "rgba(255,255,255,0.2)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, color: "#fff" }}>
            A
          </div>
        </div>

        <div style={{ background: "rgba(255,255,255,0.15)", borderRadius: 12, padding: "12px 14px" }}>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.7)", marginBottom: 4 }}>Total invested</div>
          <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 30, color: "#fff", lineHeight: 1 }}>
            ${(animAmt / 100).toFixed(2)}
          </div>
          <div style={{ fontSize: 10, color: "rgba(255,255,255,0.7)", marginTop: 4 }}>↑ +$2.14 this week via round-ups</div>
        </div>
      </div>

      <div style={{ padding: "1rem" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: "1rem" }}>
          <div style={{ background: "rgba(0,0,0,0.04)", borderRadius: 10, padding: "10px 12px" }}>
            <div style={{ fontSize: 9, color: "rgba(0,0,0,0.45)", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.08em" }}>XP balance</div>
            <div style={{ fontSize: 22, fontWeight: 500 }}>{animXP}</div>
            <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)", marginTop: 2 }}>Spark Saver · Lv 2</div>
          </div>
          <div style={{ background: "rgba(0,0,0,0.04)", borderRadius: 10, padding: "10px 12px" }}>
            <div style={{ fontSize: 9, color: "rgba(0,0,0,0.45)", marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.08em" }}>Streak</div>
            <div style={{ fontSize: 22, fontWeight: 500 }}>3</div>
            <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)", marginTop: 2 }}>days in a row</div>
          </div>
        </div>

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Goal progress
        </div>
        <Card style={{ marginBottom: "1rem" }}>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
            <span style={{ fontSize: 18 }}>{goalObj.icon}</span>
            <div>
              <div style={{ fontSize: 12, fontWeight: 500 }}>{goalObj.name}</div>
              <div style={{ fontSize: 10, color: "rgba(0,0,0,0.45)" }}>TFSA · Balanced Growth</div>
            </div>
          </div>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
            <span style={{ fontSize: 11, color: "rgba(0,0,0,0.5)" }}>Invested</span>
            <span style={{ fontSize: 12, fontWeight: 500 }}>${(animAmt / 100).toFixed(2)} / $5,000</span>
          </div>
          <ProgressBar value={animAmt / 100} max={5000} />
          <div style={{ fontSize: 10, color: "rgba(0,0,0,0.4)", marginTop: 5 }}>
            At this pace: $5,000 in ~3.1 years · boost round-ups to cut to 2.4 yrs
          </div>
        </Card>

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Recent activity
        </div>
        {TRANSACTIONS.slice(0, 3).map((tx) => (
          <div key={tx.name} style={{ display: "flex", alignItems: "center", gap: 9, paddingBottom: 9, marginBottom: 9, borderBottom: "0.5px solid rgba(0,0,0,0.07)" }}>
            <div style={{ width: 32, height: 32, borderRadius: 8, background: "rgba(0,0,0,0.05)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14, flexShrink: 0 }}>
              {tx.icon}
            </div>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 11, fontWeight: 500 }}>{tx.name}</div>
              <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)" }}>{tx.time}</div>
            </div>
            <div style={{ textAlign: "right" }}>
              <div style={{ fontSize: 11, color: "rgba(0,0,0,0.45)" }}>-${tx.spent.toFixed(2)}</div>
              <div style={{ fontSize: 11, fontWeight: 500, color: "#0F6E56" }}>+${tx.roundup.toFixed(2)}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
