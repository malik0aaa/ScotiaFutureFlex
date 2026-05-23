import { useState } from "react";
import NavBar from "./components/ui/NavBar";
import OnboardWelcome   from "./screens/onboarding/OnboardWelcome";
import OnboardGoal      from "./screens/onboarding/OnboardGoal";
import OnboardPortfolio from "./screens/onboarding/OnboardPortfolio";
import OnboardConfirm   from "./screens/onboarding/OnboardConfirm";
import HomeTab     from "./screens/tabs/HomeTab";
import InvestTab   from "./screens/tabs/InvestTab";
import RewardsTab  from "./screens/tabs/RewardsTab";
import HabitsTab   from "./screens/tabs/HabitsTab";
import RoundupsTab from "./screens/tabs/RoundupsTab";

export default function App() {
  const [screen, setScreen] = useState("onboard_welcome");
  const [tab,    setTab]    = useState("home");
  const [goal,   setGoal]   = useState(null);
  const [amount, setAmount] = useState(50);
  const [roundup,setRoundup]= useState(true);
  const [xp,     setXp]     = useState(620);

  const goToApp = (t = "home") => { setTab(t); setScreen("app"); };

  const renderOnboard = () => {
    switch (screen) {
      case "onboard_welcome":
        return <OnboardWelcome onNext={() => setScreen("onboard_goal")} />;
      case "onboard_goal":
        return <OnboardGoal onNext={() => setScreen("onboard_portfolio")} onBack={() => setScreen("onboard_welcome")} goal={goal} setGoal={setGoal} />;
      case "onboard_portfolio":
        return <OnboardPortfolio onNext={() => setScreen("onboard_confirm")} onBack={() => setScreen("onboard_goal")} goal={goal} amount={amount} setAmount={setAmount} roundup={roundup} setRoundup={setRoundup} />;
      case "onboard_confirm":
        return (
          <div style={{ overflowY: "auto" }}>
            <OnboardConfirm onDone={() => { setXp((x) => x + 150); goToApp(); }} amount={amount} goal={goal} roundup={roundup} />
          </div>
        );
      default:
        return null;
    }
  };

  const renderTab = () => {
    switch (tab) {
      case "home":     return <HomeTab    xp={xp} amount={amount} goal={goal || "home"} roundup={roundup} />;
      case "invest":   return <InvestTab  xp={xp} setXp={setXp} amount={amount} />;
      case "rewards":  return <RewardsTab xp={xp} setXp={setXp} />;
      case "habits":   return <HabitsTab  xp={xp} setXp={setXp} />;
      case "roundups": return <RoundupsTab />;
      default:         return null;
    }
  };

  const isApp = screen === "app";

  return (
    <div style={{ display: "flex", justifyContent: "center", alignItems: "flex-start", padding: "1.5rem 0 2rem", fontFamily: "'DM Sans', sans-serif", minHeight: "100vh", background: "var(--color-background-secondary)" }}>
      <div style={{ width: 320, background: "#fff", borderRadius: 44, border: "9px solid #1a1a1a", overflow: "hidden", display: "flex", flexDirection: "column" }}>
        {/* Phone notch */}
        <div style={{ height: 28, background: "#1a1a1a", display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0 }}>
          <div style={{ width: 80, height: 18, background: "#000", borderRadius: "0 0 12px 12px" }} />
        </div>

        <div style={{ flex: 1, display: "flex", flexDirection: "column", maxHeight: 620, overflow: "hidden" }}>
          {isApp ? (
            <>
              <div style={{ flex: 1, overflowY: "auto", display: "flex", flexDirection: "column" }}>
                {renderTab()}
              </div>
              <NavBar active={tab} onChange={goToApp} />
            </>
          ) : (
            <div style={{ flex: 1, overflowY: "auto" }}>
              {renderOnboard()}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
