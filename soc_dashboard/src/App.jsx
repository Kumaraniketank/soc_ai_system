import { useEffect, useState, useRef } from "react";

const FONTS_CSS = `
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800&family=Share+Tech+Mono&family=Inter:wght@300;400;500&display=swap');

  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

  body { background: #020c1b; }

  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: #020c1b; }
  ::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.3); border-radius: 2px; }

  @keyframes pulse-ring {
    0% { transform: scale(0.8); opacity: 1; }
    100% { transform: scale(2.2); opacity: 0; }
  }
  @keyframes scan {
    0% { transform: translateY(-100%); opacity: 0.6; }
    100% { transform: translateY(100vh); opacity: 0; }
  }
  @keyframes flicker {
    0%, 95%, 100% { opacity: 1; }
    96% { opacity: 0.4; }
    97% { opacity: 1; }
    98% { opacity: 0.5; }
  }
  @keyframes slideIn {
    from { transform: translateX(40px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
  }
  @keyframes blink {
    0%, 49% { opacity: 1; }
    50%, 100% { opacity: 0; }
  }
  @keyframes gridMove {
    from { background-position: 0 0; }
    to { background-position: 0 40px; }
  }
`;

function getSeverity(report) {
  const t = (report || "").toLowerCase();
  if (t.includes("critical") || t.includes("emergency") || t.includes("ransomware") || t.includes("breach")) return "critical";
  if (t.includes("high") || t.includes("malware") || t.includes("intrusion") || t.includes("exploit") || t.includes("attack")) return "high";
  if (t.includes("medium") || t.includes("warning") || t.includes("suspicious") || t.includes("anomaly")) return "medium";
  return "low";
}

const SEV = {
  critical: { color: "#ff2d55", bg: "rgba(255,45,85,0.08)", border: "rgba(255,45,85,0.4)", glow: "rgba(255,45,85,0.25)", label: "CRITICAL" },
  high:     { color: "#ff6b2b", bg: "rgba(255,107,43,0.08)", border: "rgba(255,107,43,0.4)", glow: "rgba(255,107,43,0.2)", label: "HIGH" },
  medium:   { color: "#ffd60a", bg: "rgba(255,214,10,0.06)", border: "rgba(255,214,10,0.35)", glow: "rgba(255,214,10,0.15)", label: "MEDIUM" },
  low:      { color: "#00ff88", bg: "rgba(0,255,136,0.05)", border: "rgba(0,255,136,0.3)", glow: "rgba(0,255,136,0.12)", label: "LOW" },
};

function StatCard({ label, value, accent }) {
  return (
    <div style={{
      flex: "1 1 120px",
      background: "rgba(0,212,255,0.03)",
      border: `1px solid ${accent || "rgba(0,212,255,0.2)"}`,
      borderRadius: "8px",
      padding: "14px 18px",
      minWidth: "100px",
    }}>
      <div style={{ fontSize: "11px", color: "#4a7fa5", fontFamily: "'Inter', sans-serif", letterSpacing: "0.12em", textTransform: "uppercase", marginBottom: "6px" }}>
        {label}
      </div>
      <div style={{ fontSize: "26px", fontFamily: "'Orbitron', sans-serif", fontWeight: 600, color: accent || "#00d4ff", lineHeight: 1 }}>
        {value}
      </div>
    </div>
  );
}

function AlertCard({ alert, index }) {
  const sev = getSeverity(alert.report);
  const cfg = SEV[sev];
  const time = alert.timestamp || new Date().toISOString();
  const formatted = typeof time === "string" ? time.replace("T", " ").slice(0, 19) : "";

  return (
    <div style={{
      animation: "slideIn 0.35s ease forwards",
      background: cfg.bg,
      border: `1px solid ${cfg.border}`,
      borderLeft: `3px solid ${cfg.color}`,
      borderRadius: "8px",
      padding: "16px 20px",
      marginBottom: "10px",
      boxShadow: `0 0 20px ${cfg.glow}`,
      position: "relative",
      overflow: "hidden",
    }}>
      <div style={{
        position: "absolute", top: 0, right: 0, width: "120px", height: "120px",
        background: `radial-gradient(circle at top right, ${cfg.glow}, transparent 70%)`,
        pointerEvents: "none",
      }} />

      <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "10px", flexWrap: "wrap" }}>
        <span style={{
          fontFamily: "'Orbitron', sans-serif", fontSize: "10px", fontWeight: 600,
          color: cfg.color, background: `${cfg.border}`, border: `1px solid ${cfg.color}`,
          padding: "3px 10px", borderRadius: "4px", letterSpacing: "0.1em",
        }}>
          {cfg.label}
        </span>
        <span style={{ fontSize: "11px", fontFamily: "'Share Tech Mono', monospace", color: "#4a7fa5" }}>
          #{String(index + 1).padStart(4, "0")}
        </span>
        {formatted && (
          <span style={{ fontSize: "11px", fontFamily: "'Share Tech Mono', monospace", color: "#4a7fa5", marginLeft: "auto" }}>
            {formatted}
          </span>
        )}
      </div>

      <pre style={{
        fontFamily: "'Share Tech Mono', monospace",
        fontSize: "13px",
        lineHeight: "1.7",
        color: "#c8e6f5",
        whiteSpace: "pre-wrap",
        wordBreak: "break-word",
        overflowX: "hidden",
      }}>
        {alert.report}
      </pre>
    </div>
  );
}

function ConnectionDot({ connected }) {
  return (
    <span style={{ position: "relative", display: "inline-flex", alignItems: "center", justifyContent: "center", width: "16px", height: "16px" }}>
      {connected && (
        <span style={{
          position: "absolute", width: "16px", height: "16px", borderRadius: "50%",
          background: "#00ff88", animation: "pulse-ring 1.5s ease-out infinite", opacity: 0.5,
        }} />
      )}
      <span style={{
        width: "8px", height: "8px", borderRadius: "50%",
        background: connected ? "#00ff88" : "#ff2d55",
        display: "block",
      }} />
    </span>
  );
}

export default function App() {
  const [alerts, setAlerts] = useState([]);
  const [connected, setConnected] = useState(false);
  const [time, setTime] = useState(new Date());
  const feedRef = useRef(null);

  useEffect(() => {
    const styleEl = document.createElement("style");
    styleEl.textContent = FONTS_CSS;
    document.head.appendChild(styleEl);
    return () => document.head.removeChild(styleEl);
  }, []);

  useEffect(() => {
    const t = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(t);
  }, []);

  useEffect(() => {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws");
    socket.onopen = () => { console.log("WebSocket Connected"); setConnected(true); };
    socket.onmessage = (e) => {
      console.log("Message Received:", e.data);
      const data = JSON.parse(e.data);
      setAlerts((prev) => [{ ...data, timestamp: data.timestamp || new Date().toISOString() }, ...prev]);
    };
    socket.onerror = (err) => { console.log("WebSocket Error:", err); setConnected(false); };
    socket.onclose = () => { console.log("WebSocket Closed"); setConnected(false); };
    return () => socket.close();
  }, []);

  const counts = alerts.reduce(
    (acc, a) => { acc[getSeverity(a.report)]++; return acc; },
    { critical: 0, high: 0, medium: 0, low: 0 }
  );

  const pad = (n) => String(n).padStart(2, "0");
  const timeStr = `${pad(time.getHours())}:${pad(time.getMinutes())}:${pad(time.getSeconds())}`;
  const dateStr = time.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" }).toUpperCase();

  return (
    <div style={{
      background: "#020c1b",
      color: "#c8e6f5",
      minHeight: "100vh",
      fontFamily: "'Inter', sans-serif",
      position: "relative",
      overflow: "hidden",
    }}>
      {/* Scrolling grid background */}
      <div style={{
        position: "fixed", inset: 0, pointerEvents: "none", zIndex: 0,
        backgroundImage: "linear-gradient(rgba(0,212,255,0.04) 1px, transparent 1px), linear-gradient(90deg, rgba(0,212,255,0.04) 1px, transparent 1px)",
        backgroundSize: "40px 40px",
        animation: "gridMove 4s linear infinite",
      }} />

      {/* Scan line */}
      <div style={{
        position: "fixed", left: 0, right: 0, height: "2px", pointerEvents: "none", zIndex: 1,
        background: "linear-gradient(90deg, transparent, rgba(0,212,255,0.3), transparent)",
        animation: "scan 8s linear infinite",
      }} />

      <div style={{ position: "relative", zIndex: 2, maxWidth: "960px", margin: "0 auto", padding: "24px 20px 40px" }}>

        {/* Header */}
        <header style={{ marginBottom: "28px" }}>
          <div style={{
            display: "flex", alignItems: "flex-start", justifyContent: "space-between",
            flexWrap: "wrap", gap: "16px", marginBottom: "20px",
          }}>
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: "10px", marginBottom: "4px" }}>
                <div style={{
                  width: "32px", height: "32px", borderRadius: "6px",
                  background: "rgba(0,212,255,0.1)", border: "1px solid rgba(0,212,255,0.4)",
                  display: "flex", alignItems: "center", justifyContent: "center",
                }}>
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
                    <rect x="3" y="11" width="18" height="11" rx="2" stroke="#00d4ff" strokeWidth="2" fill="rgba(0,212,255,0.15)"/>
                    <path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="#00d4ff" strokeWidth="2" strokeLinecap="round"/>
                    <circle cx="12" cy="16" r="1.5" fill="#00d4ff"/>
                    <line x1="12" y1="17.5" x2="12" y2="20" stroke="#00d4ff" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                </div>
                <h1 style={{
                  fontFamily: "'Orbitron', sans-serif", fontWeight: 800,
                  fontSize: "clamp(16px, 3vw, 22px)", letterSpacing: "0.08em",
                  color: "#00d4ff", animation: "flicker 6s infinite",
                }}>
                  KAITRA<span style={{ color: "#4a7fa5" }}> SECURITY</span>
                </h1>
              </div>
              <div style={{
                fontSize: "11px", fontFamily: "'Share Tech Mono', monospace",
                color: "#4a7fa5", letterSpacing: "0.15em", textTransform: "uppercase",
              }}>
                Security Operations Center — Live Dashboard
              </div>
            </div>

            <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: "4px" }}>
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <ConnectionDot connected={connected} />
                <span style={{
                  fontSize: "12px", fontFamily: "'Share Tech Mono', monospace",
                  color: connected ? "#00ff88" : "#ff2d55", letterSpacing: "0.1em",
                }}>
                  {connected ? "LIVE" : "OFFLINE"}
                </span>
              </div>
              <div style={{
                fontSize: "20px", fontFamily: "'Orbitron', sans-serif", fontWeight: 600,
                color: "#00d4ff", lineHeight: 1,
              }}>
                {timeStr}
                <span style={{ animation: "blink 1s step-end infinite", color: "#00d4ff" }}> </span>
              </div>
              <div style={{ fontSize: "11px", fontFamily: "'Share Tech Mono', monospace", color: "#4a7fa5" }}>
                {dateStr}
              </div>
            </div>
          </div>

          {/* Divider */}
          <div style={{ height: "1px", background: "linear-gradient(90deg, rgba(0,212,255,0.5), rgba(0,212,255,0.1), transparent)" }} />
        </header>

        {/* Stat cards */}
        <div style={{ display: "flex", gap: "10px", flexWrap: "wrap", marginBottom: "24px" }}>
          <StatCard label="Total Alerts" value={alerts.length} />
          <StatCard label="Critical"     value={counts.critical} accent={counts.critical > 0 ? "#ff2d55" : undefined} />
          <StatCard label="High"         value={counts.high}     accent={counts.high > 0 ? "#ff6b2b" : undefined} />
          <StatCard label="Medium"       value={counts.medium}   accent={counts.medium > 0 ? "#ffd60a" : undefined} />
          <StatCard label="Low"          value={counts.low}      accent="#00ff88" />
        </div>

        {/* Feed label */}
        <div style={{
          display: "flex", alignItems: "center", gap: "10px", marginBottom: "14px",
        }}>
          <span style={{ fontSize: "11px", fontFamily: "'Share Tech Mono', monospace", color: "#4a7fa5", letterSpacing: "0.15em" }}>
            ALERT FEED
          </span>
          <div style={{ flex: 1, height: "1px", background: "rgba(0,212,255,0.12)" }} />
          {alerts.length > 0 && (
            <span style={{ fontSize: "11px", fontFamily: "'Share Tech Mono', monospace", color: "#4a7fa5" }}>
              {alerts.length} event{alerts.length !== 1 ? "s" : ""}
            </span>
          )}
        </div>

        {/* Feed */}
        <div ref={feedRef}>
          {alerts.length === 0 ? (
            <div style={{
              textAlign: "center", padding: "60px 20px",
              border: "1px dashed rgba(0,212,255,0.15)", borderRadius: "8px",
            }}>
              <div style={{
                fontSize: "13px", fontFamily: "'Share Tech Mono', monospace",
                color: "#4a7fa5", letterSpacing: "0.1em",
              }}>
                <span style={{ animation: "blink 1s step-end infinite" }}>█</span>
                {"  "}AWAITING INCOMING EVENTS
              </div>
            </div>
          ) : (
            alerts.map((alert, i) => <AlertCard key={i} alert={alert} index={i} />)
          )}
        </div>

      </div>
    </div>
  );
}
