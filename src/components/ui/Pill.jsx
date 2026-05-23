import { SCOTIA_RED } from "../../constants/colors";

export default function Pill({ children, color = SCOTIA_RED, textColor = "#fff", small }) {
  return (
    <span
      style={{
        background: color,
        color: textColor,
        fontSize: small ? 9 : 11,
        fontWeight: 500,
        borderRadius: 100,
        padding: small ? "2px 7px" : "3px 9px",
        whiteSpace: "nowrap",
      }}
    >
      {children}
    </span>
  );
}
