/**
 * Class to handle webcam
 */
export class Webcam {
  /**
   * Open normal zoom back webcam and stream it through video tag.
   * @param {HTMLVideoElement} videoRef video tag reference
   */
  openNormalCamera = async (videoRef, setStreaming) => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      // get a list of available cameras
      const devices = await navigator.mediaDevices.enumerateDevices();

      // find the right back camera
      let selectedDevice = devices.find(
        (device) =>
          device.kind === "videoinput" &&
          device.label.toLowerCase().includes("back") &&
          !device.label.toLowerCase().includes("wide") &&
          !device.label.toLowerCase().includes("telephoto") &&
          !device.label.toLowerCase().includes("dual") &&
          !device.label.toLowerCase().includes("triple")
      );

      // if not found, use any video input
      if (!selectedDevice) {
        console.log("No NORMAL BACK camera found, using any video input.");
        selectedDevice = devices.find((device) => device.kind === "videoinput");
      }

      // is still not found, alert user
      if (!selectedDevice) {
        alert("No back camera found!");
        setStreaming(false);
        return;
      }

      // console.log("Selected input device:");
      // console.log("       ID:", selectedDevice.deviceId);
      // console.log("     Kind:", selectedDevice.kind);
      // console.log("    Label:", selectedDevice.label);

      // start streaming the selected camera
      navigator.mediaDevices
        .getUserMedia({
          video: {
            deviceId: { exact: selectedDevice.deviceId },
          },
        })
        .then((stream) => {
          videoRef.srcObject = stream;
          // videoRef.playsInline = true;
          videoRef.style.display = "block";
          setStreaming("normal");
        });
    }
  };
  /**
   * Open telephoto back webcam and stream it through video tag.
   * @param {HTMLVideoElement} videoRef video tag reference
   */
  openTelephotoCamera = async (videoRef, setStreaming) => {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      // get a list of available cameras
      const devices = await navigator.mediaDevices.enumerateDevices();

      // find the right back camera
      let selectedDevice = devices.find(
        (device) =>
          device.kind === "videoinput" &&
          device.label.toLowerCase().includes("back") &&
          device.label.toLowerCase().includes("telephoto") &&
          !device.label.toLowerCase().includes("wide") &&
          !device.label.toLowerCase().includes("dual") &&
          !device.label.toLowerCase().includes("triple")
      );

      // if not found, use any video input
      if (!selectedDevice) {
        console.log("No TELEPHOTO BACK camera found, using any video input.");
        selectedDevice = devices.find((device) => device.kind === "videoinput");
      }

      // is still not found, alert user
      if (!selectedDevice) {
        alert("No back camera found!");
        setStreaming(false);
        return;
      }

      // console.log("Selected input device:");
      // console.log("       ID:", selectedDevice.deviceId);
      // console.log("     Kind:", selectedDevice.kind);
      // console.log("    Label:", selectedDevice.label);

      // start streaming the selected camera
      navigator.mediaDevices
        .getUserMedia({
          video: {
            deviceId: { exact: selectedDevice.deviceId },
          },
        })
        .then((stream) => {
          videoRef.srcObject = stream;
          // videoRef.playsInline = true;
          videoRef.style.display = "block";
          setStreaming("telephoto");
        });
    }
  };

  /**
   * Close opened webcam.
   * @param {HTMLVideoElement} videoRef video tag reference
   */
  close = (videoRef, setStreaming) => {
    if (videoRef.srcObject) {
      videoRef.srcObject.getTracks().forEach((track) => {
        track.stop();
      });
      videoRef.srcObject = null;
      videoRef.style.display = "none";
    }
    setStreaming(false);
  };
}
