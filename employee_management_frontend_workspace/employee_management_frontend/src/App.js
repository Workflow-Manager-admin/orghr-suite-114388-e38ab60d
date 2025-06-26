import React, { useState, useEffect } from "react";
import { BrowserRouter } from "react-router-dom";
import "./App.css";
import AppRouter from "./router";
import { COLORS } from "./theme";

// PUBLIC_INTERFACE
function App() {
  const [theme, setTheme] = useState("light");

  // Effect to apply theme to document element
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  return (
    <div className="App">
      <TopBar theme={theme} setTheme={setTheme} />
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </div>
  );
}

function TopBar({ theme, setTheme }) {
  return (
    <div className="topbar" style={{ background: COLORS.primary, color: "#fff", display: "flex", alignItems: "center", height: 56, padding: "0 2rem", justifyContent: "space-between" }}>
      <div className="topbar-title" style={{ fontWeight: 600, fontSize: 22 }}>
        Employee Management
      </div>
      <button
        className="theme-toggle"
        onClick={() => setTheme(theme === "light" ? "dark" : "light")}
        aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
        style={{ background: COLORS.accent, color: "#222", border: 0, borderRadius: 8, padding: "5px 18px", fontSize: 16, cursor: "pointer", fontWeight: 500 }}
      >
        {theme === "light" ? "🌙 Dark" : "☀️ Light"}
      </button>
    </div>
  );
}

export default App;
