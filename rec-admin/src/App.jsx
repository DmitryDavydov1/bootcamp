import { useState } from "react";
import Dashboard from "./pages/Dashboard";
import CurrentTop from "./pages/CurrentTop";

function App() {
  const [page, setPage] = useState("dashboard");

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">R</div>
          <div>
            <h1>Reco Admin</h1>
            <p>Recommendation dashboard</p>
          </div>
        </div>

        <nav className="nav">
          <button
            className={page === "dashboard" ? "nav-button active" : "nav-button"}
            onClick={() => setPage("dashboard")}
          >
            Отчет
          </button>

          <button
            className={page === "current-top" ? "nav-button active" : "nav-button"}
            onClick={() => setPage("current-top")}
          >
            Текущий топ
          </button>
        </nav>
      </aside>

      <main className="main">
        {page === "dashboard" && <Dashboard />}
        {page === "current-top" && <CurrentTop />}
      </main>
    </div>
  );
}

export default App;