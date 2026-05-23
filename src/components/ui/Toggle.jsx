import { SCOTIA_RED } from "../../constants/colors";

export default function Toggle({ on, onChange }) {
  return (
    <div
      onClick={() => onChange(!on)}
      style={{
        width: 36, height: 20, borderRadius: 10,
        background: on ? SCOTIA_RED : "rgba(0,0,0,0.12)",
        position: "relative", cursor: "pointer",
        transition: "background .2s", flexShrink: 0,
      }}
    >
      <div
        style={{
          width: 14, height: 14, borderRadius: "50%", background: "#fff",
          position: "absolute", top: 3, left: on ? 19 : 3, transition: "left .2s",
        }}
      />
    </div>
  );
}
