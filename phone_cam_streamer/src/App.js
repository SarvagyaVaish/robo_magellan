import { Routes, Route } from "react-router-dom";
import Home from "./Home";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="robo_magellan" element={<Home />} />
    </Routes>
  );
}

export default App;
