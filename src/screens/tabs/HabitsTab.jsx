import { useState } from "react";
import { SCOTIA_RED } from "../../constants/colors";
import { HABITS, BADGES } from "../../constants/data";
import Card from "../../components/ui/Card";
import Pill from "../../components/ui/Pill";
import ProgressBar from "../../components/ui/ProgressBar";

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"];

export default function HabitsTab({ xp, setXp }) {
  const [habits, setHabits] = useState(HABITS);
  const [freeze, setFreeze] = useState(true);

  const complete = (id) => {
    const h = habits.find((x) => x.id === id);
    if (h && !h.done) {
      setHabits((prev) => prev.map((x) => x.id === id ? { ...x, done: true, progress: x.total } : x));
      setXp((p) => p + h.xp);
    }
  };

  return (
    <div style={{ overflowY: "auto", flex: 1 }}>
      <div style={{ background: SCOTIA_RED, padding: "1rem 1.25rem 0.85rem" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8 }}>
          <div>
            <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 17, color: "#fff" }}>Spark Saver</div>
            <div style={{ fontSize: 10, color: "rgba(255,255,255,0.7)" }}>Level 2 investor</div>
          </div>
          <div style={{ width: 38, height: 38, borderRadius: 10, background: "rgba(255,255,255,0.2)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 20, color: "#fff" }}>
            🔥
          </div>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <div style={{ flex: 1, height: 5, background: "rgba(255,255,255,0.25)", borderRadius: 3, overflow: "hidden" }}>
            <div style={{ height: "100%", width: "62%", background: "#fff", borderRadius: 3 }} />
          </div>
          <span style={{ fontSize: 10, color: "rgba(255,255,255,0.75)" }}>{xp} / 1000 XP</span>
        </div>
      </div>

      <div style={{ padding: "1rem" }}>
        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Weekly streak
        </div>
        <div style={{ display: "flex", gap: 5, marginBottom: "1rem" }}>
          {DAYS.map((d, i) => (
            <div key={d} style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", gap: 3 }}>
              <div style={{
                width: 28, height: 28, borderRadius: "50%",
                background: i < 3 ? SCOTIA_RED : "transparent",
                border: i < 3 ? `0.5px solid ${SCOTIA_RED}` : i === 3 ? `2px solid ${SCOTIA_RED}` : "0.5px solid rgba(0,0,0,0.12)",
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 11,
                color: i < 3 ? "#fff" : i === 3 ? SCOTIA_RED : "rgba(0,0,0,0.25)",
              }}>
                {i < 3 ? "✓" : i === 3 ? "⚡" : ""}
              </div>
              <span style={{ fontSize: 9, color: i === 3 ? SCOTIA_RED : "rgba(0,0,0,0.4)", fontWeight: i === 3 ? 600 : 400 }}>
                {d}
              </span>
            </div>
          ))}
        </div>

        <div style={{ background: "#E6F1FB", borderRadius: 10, padding: "9px 11px", display: "flex", gap: 7, alignItems: "flex-start", marginBottom: "1rem" }}>
          <span style={{ fontSize: 13, color: "#185FA5", marginTop: 1 }}>🔔</span>
          <span style={{ fontSize: 10, color: "#042C53", lineHeight: 1.5 }}>
            <strong>Today&apos;s cue:</strong> You usually check your portfolio around 8am. Do it after your morning coffee to keep your streak.
          </span>
        </div>

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", marginBottom: 8 }}>
          Today&apos;s habits
        </div>
        {habits.map((h) => (
          <Card key={h.id} style={{ marginBottom: 8 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
              <span style={{ fontSize: 15, color: SCOTIA_RED }}>{h.icon}</span>
              <span style={{ fontSize: 11, fontWeight: 500, flex: 1 }}>{h.name}</span>
              <Pill color="#FAEEDA" textColor="#854F0B" small>+{h.xp} XP</Pill>
            </div>
            <ProgressBar value={h.progress} max={h.total} color={h.done ? "#1D9E75" : SCOTIA_RED} />
            <div style={{ display: "flex", justifyContent: "space-between", marginTop: 4 }}>
              <span style={{ fontSize: 9, color: "rgba(0,0,0,0.4)" }}>{h.done ? "Done today ✓" : "Due today"}</span>
              {!h.done && (
                <button
                  onClick={() => complete(h.id)}
                  style={{ fontSize: 9, background: SCOTIA_RED, color: "#fff", border: "none", borderRadius: 6, padding: "2px 8px", cursor: "pointer", fontFamily: "inherit" }}
                >
                  Mark done +{h.xp}XP
                </button>
              )}
            </div>
          </Card>
        ))}

        <div style={{ fontSize: 9, fontWeight: 500, letterSpacing: "0.11em", textTransform: "uppercase", color: "rgba(0,0,0,0.4)", margin: "1rem 0 8px" }}>
          Badges
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: "1rem" }}>
          {BADGES.map((b) => (
            <div key={b.id} style={{ border: "0.5px solid rgba(0,0,0,0.1)", borderRadius: 11, padding: "9px 10px", display: "flex", alignItems: "center", gap: 8, opacity: b.earned ? 1 : 0.4 }}>
              <div style={{ width: 32, height: 32, borderRadius: 8, background: b.earned ? "#FAEEDA" : "rgba(0,0,0,0.05)", display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15, flexShrink: 0 }}>
                {b.icon}
              </div>
              <div>
                <div style={{ fontSize: 10, fontWeight: 500, lineHeight: 1.3 }}>{b.name}</div>
                <div style={{ fontSize: 9, color: "rgba(0,0,0,0.4)" }}>{b.sub}</div>
              </div>
            </div>
          ))}
        </div>

        {freeze && (
          <div style={{ background: "#FAEEDA", borderRadius: 10, padding: "9px 11px", display: "flex", gap: 8, alignItems: "flex-start" }}>
            <span style={{ fontSize: 13, color: "#854F0B", marginTop: 1 }}>❄</span>
            <div style={{ flex: 1 }}>
              <div style={{ fontSize: 10, color: "#633806", lineHeight: 1.5, marginBottom: 5 }}>
                <strong>Streak freeze available</strong> — miss a day without losing your streak. Free once/month.
              </div>
              <button
                onClick={() => setFreeze(false)}
                style={{ fontSize: 10, background: "#854F0B", color: "#fff", border: "none", borderRadius: 7, padding: "4px 9px", cursor: "pointer", fontFamily: "inherit" }}
              >
                Save my streak (free)
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
