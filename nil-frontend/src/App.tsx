import "./App.css";
import Home from "./Home";
import Players from "./Players";
import PlayerDetail from "./PlayerDetail";
import RosterBuilder from "./RosterBuilder";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";

function App() {
  return (
    <BrowserRouter>
      <div className="p-4 flex gap-4">
        <Link className="underline" to="/">Home</Link>
        <Link className="underline" to="/players">Players</Link>
        <Link className="underline" to="/builder">Roster Builder</Link>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/players" element={<Players />} />
        <Route path="/player/:id" element={<PlayerDetail />} />
        <Route path="/builder" element={<RosterBuilder />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
