export const sendConeDetections = async (detections, serverName) => {
  const api_url = `https://${serverName}.tail49268.ts.net:8000/cone_detections`;

  try {
    const response = await fetch(api_url, {
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
