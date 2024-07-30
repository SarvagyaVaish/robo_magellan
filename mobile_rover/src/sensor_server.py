# Usage
# -----
# On the phone app:
#   - ip: http://survy-mac.tail49268.ts.net:8000/sensor_data
#   - http method: POST
#   - payload coding: json
#
# Start the server with:
#   uvicorn sensor_server:app --reload --host survy-mac.tail49268.ts.net --port 8000
#     or
#   python sensor_server.py


from contextlib import asynccontextmanager
import json
import math
import os
import signal
import sys

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from config_manager import get_sensor_service_address
from custom_logger import get_logger
from pub_sub import get_publisher_gps
from pub_sub import get_publisher_cone_detections


def signal_handler(sig, frame):
    sys.exit(0)


logger = get_logger(__name__, "info")


# Use the lifespan to start and close the GPS publisher.
# This closes the publisher socket when using the uvicorn hot reloading functionality.
@asynccontextmanager
async def lifespan(app: FastAPI):
    global gps_publisher, cone_detections_publisher

    logger.debug("Server lifespan start")
    gps_publisher = get_publisher_gps()
    cone_detections_publisher = get_publisher_cone_detections()

    yield

    logger.debug("Server lifespan end")
    gps_publisher.close()
    cone_detections_publisher.close()


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test_get")
def read_root():
    return {"Request type": "GET", "status": "OK"}


def gps_from_sensor_frame(data_json):
    available_keys = set(data_json.keys())
    required_keys = {
        "locationTimestamp_since1970",
        "locationLongitude",
        "locationLatitude",
        "locationHorizontalAccuracy",
        "locationTrueHeading",
        "locationHeadingAccuracy",
    }
    if len(required_keys - available_keys) > 0:
        return None

    data_gps = {
        "timestamp": float(data_json["locationTimestamp_since1970"]),
        "longitude": float(data_json["locationLongitude"]),
        "latitude": float(data_json["locationLatitude"]),
        "gpsAccuracy": float(data_json["locationHorizontalAccuracy"]),
        "heading": math.radians(float(data_json["locationTrueHeading"])),
        "headingAccuracy": math.radians(float(data_json["locationHeadingAccuracy"])),
    }

    return data_gps


gps_publisher = None


@app.post("/sensor_data")
async def sensor_data(request: Request):
    data_raw = await request.body()
    logger.debug(f"Raw data received on /server_data: {data_raw}")

    data_json = json.loads(data_raw.decode("utf-8"))
    data_gps = gps_from_sensor_frame(data_json)
    if data_gps is not None:
        logger.info(f"Sending data: {data_gps}")
        gps_publisher.send_json(data_gps)

    return {"status": "OK"}


cone_detections_publisher = None


@app.post("/cone_detections")
async def cone_detections(request: Request):
    data_raw = await request.body()
    logger.debug(f"Raw data received on /server_data: {data_raw}")

    data_json = json.loads(data_raw.decode("utf-8"))
    """
    example_raw_data = {
        "detections": [
            {
                "x": 0.5295924186706543,
                "y": 0.42527180910110474,
                "width": 0.10086383819580078,
                "height": 0.1837218999862671,
                "score": 0.9829293489456177,
                "class": 0,
            },
        ]
    }
    """

    # Iterate over detections and find the largest one by area of image
    largest_detection = None
    largest_detection_area = 0
    for detection in data_json["detections"]:
        detection_area = detection["width"] * detection["height"]
        if detection_area > largest_detection_area:
            largest_detection = detection
            largest_detection_area = detection_area
    logger.debug(f"Largest detection: {largest_detection}")

    cone_detections_publisher.send_json(largest_detection)

    return {"status": "OK"}


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Check if the cert and key files exist
    tls_crt_path = os.path.join(os.path.expanduser("~"), "tailscale_tls.crt")
    tls_key_path = os.path.join(os.path.expanduser("~"), "tailscale_tls.key")
    if not os.path.exists(tls_crt_path):
        raise FileNotFoundError(f"Certificate file not found at {tls_crt_path}")
    if not os.path.exists(tls_key_path):
        raise FileNotFoundError(f"Key file not found at {tls_key_path}")

    # Get server config
    host, port = get_sensor_service_address()

    # Print Client settings
    logger.info("Client Settings:")
    logger.info(f"Set Client HTTP requests endpoint to: https://{host}:{port}/sensor_data")

    uvicorn.run(
        "__main__:app",
        host=host,
        port=port,
        reload=True,
        ssl_certfile=tls_crt_path,
        ssl_keyfile=tls_key_path,
    )
