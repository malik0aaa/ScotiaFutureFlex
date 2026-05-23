import { SCOTIA_RED } from "../../constants/colors";

export default function Card({ children, style, onClick, accent }) {
  return (
    <div
      onClick={onClick}
      style={{
        background: "#fff",
        border: accent ? `2px solid ${SCOTIA_RED}` : "0.5px solid rgba(0,0,0,0.1)",
        borderRadius: 12,
        padding: "10px 12px",
        cursor: onClick ? "pointer" : "default",
        transition: "opacity .15s",
        ...style,
      }}
    >
      {children}
    </div>
  );
}
