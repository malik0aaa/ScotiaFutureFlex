export const GOALS = [
  { id: "home",      icon: "🏠", name: "Home deposit",    desc: "Save for your first down payment",  color: "#E1F5EE", text: "#085041" },
  { id: "travel",    icon: "✈️", name: "Travel fund",      desc: "Your next adventure",               color: "#E6F1FB", text: "#0C447C" },
  { id: "retire",    icon: "🌅", name: "Early retirement", desc: "Financial freedom",                 color: "#FAEEDA", text: "#633806" },
  { id: "emergency", icon: "🛡️", name: "Emergency fund",  desc: "Safety net for the unexpected",     color: "#FBEAF0", text: "#72243E" },
];

export const AMOUNTS = [25, 50, 100, 200];

export const REWARDS = [
  { id: "feefree",  icon: "⊘",  name: "Fee-free month",      desc: "Waive your 0.25% mgmt fee for 30 days",  cost: 500, type: "Loyalty", typeColor: "#E1F5EE", typeText: "#085041", available: true  },
  { id: "doubleup", icon: "↑↑", name: "2x round-up week",    desc: "Double all spare change for 7 days",     cost: 300, type: "Feature", typeColor: "#FAEEDA", typeText: "#633806", available: true  },
  { id: "bonus",    icon: "$+", name: "$5 bonus deposit",     desc: "Scotia adds $5 to your TFSA",            cost: 400, type: "Match",   typeColor: "#E6F1FB", typeText: "#0C447C", available: true  },
  { id: "scene",    icon: "◆",  name: "Scene+ double pts",   desc: "Requires Gold tier (1000 XP)",           cost: 800, type: "Scene+",  typeColor: "#EEEDFE", typeText: "#3C3489", available: false },
];

export const TRANSACTIONS = [
  { name: "Tim Hortons",       time: "Today, 8:14am",        spent: 3.67,  roundup: 0.33, icon: "☕" },
  { name: "Shoppers Drug Mart",time: "Yesterday, 5:41pm",    spent: 14.52, roundup: 0.48, icon: "🏪" },
  { name: "TTC Transit",       time: "Yesterday, 8:02am",    spent: 3.25,  roundup: 0.75, icon: "🚇" },
  { name: "Loblaws",           time: "May 21, 6:18pm",       spent: 47.83, roundup: 0.17, icon: "🛒" },
  { name: "Netflix",           time: "May 20, 12:00am",      spent: 17.99, roundup: 0.01, icon: "▶"  },
];

export const HABITS = [
  { id: "check",  icon: "👁",  name: "Check portfolio",        xp: 10, done: true,  progress: 1, total: 1 },
  { id: "roundup",icon: "↺",  name: "Round-up a purchase",    xp: 10, done: false, progress: 0, total: 1 },
  { id: "tip",    icon: "📖", name: "Read today's money tip", xp: 20, done: false, progress: 0, total: 1 },
];

export const BADGES = [
  { id: "first",   icon: "🚀", name: "First deposit",   sub: "Earned Apr 2025",         earned: true  },
  { id: "rookie",  icon: "↺",  name: "Round-up rookie", sub: "10 round-ups done",       earned: true  },
  { id: "century", icon: "💯", name: "Century club",    sub: "Reach $100 invested",     earned: false },
  { id: "streak30",icon: "📅", name: "30-day streak",   sub: "Invest 30 days straight", earned: false },
];
