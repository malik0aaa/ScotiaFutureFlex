import { SCOTIA_RED } from "../../constants/colors";

export default function OnboardWelcome({ onNext }) {
  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100%" }}>
      <div style={{ background: SCOTIA_RED, padding: "2rem 1.5rem 1.75rem", flex: "0 0 auto" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: "1.5rem" }}>
          <div style={{ width: 24, height: 24, background: "#fff", borderRadius: 5, display: "flex", alignItems: "center", justifyContent: "center" }}>
            <span style={{ fontSize: 11, fontWeight: 700, color: SCOTIA_RED }}>S</span>
          </div>
          <span style={{ fontSize: 13, fontWeight: 500, color: "rgba(255,255,255,0.9)" }}>Scotiabank</span>
        </div>
        <div style={{ fontSize: 10, letterSpacing: "0.12em", textTransform: "uppercase", color: "rgba(255,255,255,0.6)", marginBottom: 6 }}>
          New — for first-time investors
        </div>
        <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 30, color: "#fff", lineHeight: 1.15, marginBottom: 8 }}>
          Instant Starter<br />
          <em style={{ color: "rgba(255,255,255,0.75)" }}>Portfolio</em>
        </div>
        <div style={{ fontSize: 12, color: "rgba(255,255,255,0.8)", lineHeight: 1.6 }}>
          Invest spare change, build streaks, unlock rewards. Your money actually working.
        </div>
        <div style={{ display: "inline-flex", alignItems: "center", gap: 6, background: "rgba(255,255,255,0.15)", borderRadius: 100, padding: "5px 12px", marginTop: 12 }}>
          <span style={{ fontSize: 12 }}>⚡</span>
          <span style={{ fontSize: 10, color: "#fff", fontWeight: 500 }}>Earn XP every time you invest</span>
        </div>
      </div>

      <div style={{ padding: "1.25rem", flex: 1, display: "flex", flexDirection: "column", justifyContent: "space-between" }}>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: "1rem" }}>
          {[
            ["$0.43", "avg. daily round-up"],
            ["60s",   "to first portfolio"],
            ["0.25%", "annual fee"],
            ["TFSA",  "tax-free growth"],
          ].map(([n, l]) => (
            <div key={l} style={{ background: "rgba(0,0,0,0.04)", borderRadius: 10, padding: "10px 12px" }}>
              <div style={{ fontSize: 20, fontWeight: 500, color: "#1a1a1a", lineHeight: 1 }}>{n}</div>
              <div style={{ fontSize: 10, color: "rgba(0,0,0,0.5)", marginTop: 3 }}>{l}</div>
            </div>
          ))}
        </div>

        <div>
          <button
            onClick={onNext}
            style={{ background: SCOTIA_RED, color: "#fff", border: "none", borderRadius: 12, padding: "14px", fontSize: 14, fontWeight: 500, cursor: "pointer", width: "100%", fontFamily: "inherit" }}
          >
            Start in 60 seconds — it&apos;s free
          </button>
          <div style={{ fontSize: 11, color: "rgba(0,0,0,0.4)", textAlign: "center", marginTop: 10 }}>
            Already investing? Sign in
          </div>
        </div>
      </div>
    </div>
  );
}
