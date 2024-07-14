function ControlCenter() {
  return (
    <div className="flex justify-center">
      <div className="max-w-screen-md w-full">
        {/* Title */}
        <div className="flex justify-center m-2">
          <h1 className="text-xl text-gray-800 font-semibold">
            Control Center!
          </h1>
        </div>

        {/* Links */}
        <div className="grid grid-cols-1 m-2 space-y-2 text-lg ">
          <a
            href="/"
            className="bg-gray-300 text-black font-bold p-4 rounded text-center"
          >
            Home
          </a>
        </div>
      </div>
    </div>
  );
}

export default ControlCenter;
