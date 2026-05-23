import { SCOTIA_RED } from "../../constants/colors";

export default function ProgressBar({ value, max, color = SCOTIA_RED, height = 5 }) {
  return (
    <div style={{ height, background: "rgba(0,0,0,0.07)", borderRadius: height / 2, overflow: "hidden" }}>
      <div
        style={{
          height: "100%",
          width: `${Math.min((value / max) * 100, 100)}%`,
          background: color,
          borderRadius: height / 2,
          transition: "width 0.6s ease",
        }}
      />
    </div>
  );
}
