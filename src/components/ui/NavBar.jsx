import { SCOTIA_RED } from "../../constants/colors";

const TABS = [
  { id: "home",     label: "Home",     icon: "⌂" },
  { id: "invest",   label: "Invest",   icon: "↑" },
  { id: "rewards",  label: "Rewards",  icon: "✦" },
  { id: "habits",   label: "Habits",   icon: "◎" },
  { id: "roundups", label: "Round-ups",icon: "↺" },
];

export default function NavBar({ active, onChange }) {
  return (
    <div style={{ display: "flex", borderTop: "0.5px solid rgba(0,0,0,0.1)", background: "#fff" }}>
      {TABS.map((t) => (
        <button
          key={t.id}
          onClick={() => onChange(t.id)}
          style={{
            flex: 1, border: "none", background: "none",
            padding: "8px 4px 6px", cursor: "pointer",
            display: "flex", flexDirection: "column", alignItems: "center", gap: 2,
            fontFamily: "inherit",
          }}
        >
          <span style={{ fontSize: 16, color: active === t.id ? SCOTIA_RED : "rgba(0,0,0,0.3)" }}>
            {t.icon}
          </span>
          <span
            style={{
              fontSize: 9,
              fontWeight: active === t.id ? 600 : 400,
              color: active === t.id ? SCOTIA_RED : "rgba(0,0,0,0.4)",
            }}
          >
            {t.label}
          </span>
        </button>
      ))}
    </div>
  );
}
