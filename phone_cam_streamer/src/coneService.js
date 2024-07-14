const API_URL = "https://survy-mac.tail49268.ts.net:8000/cone_detections";

export const sendConeDetections = async (detections) => {
  try {
    const response = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ detections }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error("Error sending data:", error);
    // throw error;
  }
};
