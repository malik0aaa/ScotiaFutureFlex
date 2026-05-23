import { SCOTIA_RED } from "../../constants/colors";

export default function RedHeader({ title, sub, onBack, children }) {
  return (
    <div style={{ background: SCOTIA_RED, padding: "1rem 1.25rem 0.9rem" }}>
      {onBack && (
        <button
          onClick={onBack}
          style={{
            background: "none", border: "none", color: "rgba(255,255,255,0.75)",
            fontSize: 12, cursor: "pointer", display: "flex", alignItems: "center",
            gap: 4, marginBottom: 8, padding: 0, fontFamily: "inherit",
          }}
        >
          ← Back
        </button>
      )}
      <div style={{ fontFamily: "'DM Serif Display', serif", fontSize: 22, color: "#fff", lineHeight: 1.2, marginBottom: 3 }}>
        {title}
      </div>
      {sub && <div style={{ fontSize: 11, color: "rgba(255,255,255,0.7)" }}>{sub}</div>}
      {children}
    </div>
  );
}
