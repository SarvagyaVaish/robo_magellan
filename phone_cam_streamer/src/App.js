import { Routes, Route } from "react-router-dom";

import Home from "./Home";
import ConeDetector from "./ConeDetector";
import ControlCenter from "./ControlCenter";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/robo_magellan" element={<ConeDetector />} />
      <Route path="/control_center" element={<ControlCenter />} />
    </Routes>
  );
}

export default App;
