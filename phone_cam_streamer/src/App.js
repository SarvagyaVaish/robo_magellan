import React, { useState, useEffect, useRef } from "react";

import * as tf from "@tensorflow/tfjs";
import "@tensorflow/tfjs-backend-webgl"; // set backend to webgl

import { detectVideo } from "./detect";
import { Webcam } from "./webcam";

function App() {
  // model related variables
  const modelName = "cones_yolov8s";
  const [loading, setLoading] = useState({ loading: true, progress: 0 });
  const [model, setModel] = useState({
    net: null,
    inputShape: [1, 0, 0, 3],
  });

  // webcam related variables
  const cameraRef = useRef(null);
  const canvasRef = useRef(null);
  const webcam = new Webcam();
  const [streaming, setStreaming] = useState(false);

  // load and warmup the model
  useEffect(() => {
    tf.ready().then(async () => {
      // load model
      const yolov8 = await tf.loadGraphModel(
        `${window.location.href}/${modelName}/model.json`,
        {
          onProgress: (fractions) => {
            setLoading({ loading: true, progress: fractions });
          },
        }
      );

      // warming up model
      const dummyInput = tf.ones(yolov8.inputs[0].shape);
      const warmupResults = yolov8.execute(dummyInput);

      // update model & input shape
      setLoading({ loading: false, progress: 1 });
      setModel({
        net: yolov8,
        inputShape: yolov8.inputs[0].shape,
      });

      // cleanup memory
      tf.dispose([warmupResults, dummyInput]);
    });
  }, []);

  // when model is loaded call start camera
  useEffect(() => {
    if (model.net) {
      // webcam.openNormalCamera(cameraRef.current, setStreaming);
    }
  }, [model]);

  return (
    <div className="flex justify-center">
      <div className="max-w-screen-md w-full">
        {/* Title */}
        <div className="flex justify-center m-2">
          <h1 className="text-xl text-gray-800 font-semibold">
            Camera Streamer!
          </h1>
        </div>

        {/* Loaded model */}
        <div className="flex justify-center m-2 text-sm text-gray-800">
          {loading.loading && (
            <div>
              Loading: <strong>{(loading.progress * 100).toFixed(2)}%</strong>
            </div>
          )}
          {!loading.loading && loading.progress === 1 && (
            <div>
              Model: <strong>{modelName}</strong>
            </div>
          )}
        </div>

        {/* Camera selection */}
        <div className="grid grid-cols-2 m-2 space-x-2 text-lg">
          <button
            disabled={streaming === "telephoto"}
            className={`
            bg-blue-500 text-white font-bold p-4 rounded
            ${streaming === "telephoto" ? "opacity-50" : ""}
            `}
            onClick={() => {
              if (streaming) {
                webcam.close(cameraRef.current, setStreaming);
              } else {
                webcam.openNormalCamera(cameraRef.current, setStreaming);
              }
            }}
          >
            {streaming === "normal" ? "Stop" : "Normal"}
          </button>
          <button
            disabled={streaming === "normal"}
            className={`
            bg-blue-500 text-white font-bold p-4 rounded
            ${streaming === "normal" ? "opacity-50" : ""}
            `}
            onClick={() => {
              if (streaming === "telephoto") {
                webcam.close(cameraRef.current, setStreaming);
              } else {
                webcam.close(cameraRef.current, setStreaming);
                webcam.openTelephotoCamera(cameraRef.current, setStreaming);
              }
            }}
          >
            {streaming === "telephoto" ? "Stop" : "Telephoto"}
          </button>
        </div>

        <div className="relative m-2">
          {/* Camera stream */}
          <video
            className="w-full h-auto"
            autoPlay
            display="none"
            playsInline={true}
            muted
            ref={cameraRef}
            onPlay={() =>
              detectVideo(cameraRef.current, model, canvasRef.current)
            }
          />

          {/* Canvas to draw detections */}
          <canvas
            className="absolute top-0 left-0 w-full h-full"
            width={model.inputShape[1]}
            height={model.inputShape[2]}
            ref={canvasRef}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
