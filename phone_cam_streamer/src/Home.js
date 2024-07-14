function Home() {
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
            href="/robo_magellan"
            className="bg-blue-500 text-white font-bold p-4 rounded text-center"
          >
            📸 &nbsp; Cone Detector
          </a>

          <a
            href="/control_center"
            className="bg-blue-500 text-white font-bold p-4 rounded text-center"
          >
            ⚙️ &nbsp; Control Center
          </a>
        </div>
      </div>
    </div>
  );
}

export default Home;
