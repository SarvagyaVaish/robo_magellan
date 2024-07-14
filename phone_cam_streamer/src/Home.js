import { useLocation } from "react-router-dom";
import queryString from "query-string";

import ConeDetector from "./ConeDetector";
import ControlCenter from "./ControlCenter";

function Menu() {
  return (
    <div className="flex justify-center">
      <div className="max-w-screen-md w-full">
        {/* Title */}
        <div className="flex justify-center m-2">
          <h1 className="text-xl text-gray-800 font-semibold">Home!</h1>
        </div>

        {/* Links */}
        <div className="grid grid-cols-1 m-2 space-y-2 text-lg ">
          <a
            href="/robo_magellan?pg=cone_detector"
            className="bg-blue-500 text-white font-bold p-4 rounded text-center"
          >
            📸 &nbsp; Cone Detector
          </a>

          <a
            href="/robo_magellan?pg=control_center"
            className="bg-blue-500 text-white font-bold p-4 rounded text-center"
          >
            ⚙️ &nbsp; Control Center
          </a>
        </div>
      </div>
    </div>
  );
}

function Home() {
  const { search } = useLocation();
  const parsed = queryString.parse(search);

  return (
    <div>
      {parsed.pg === "cone_detector" && <ConeDetector />}
      {parsed.pg === "control_center" && <ControlCenter />}
      {!parsed.pg && <Menu />}
    </div>
  );
}

export default Home;
