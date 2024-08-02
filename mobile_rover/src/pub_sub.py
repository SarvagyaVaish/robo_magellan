import json
import zmq
import time

from custom_logger import get_logger


logger = get_logger(__name__)


class Publisher:
    def __init__(self, port):
        self.address = f"tcp://*:{port}"

        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind(self.address)

        logger.info(f"Publisher started. Address: {self.address}")

    def send_json(self, message):
        self.socket.send_json(message)

    def read_from_logs(self, filename):
        time.sleep(1)
        with open(filename, "r") as f:
            for line in f:
                gps_json = json.loads(line)
                self.send_json(gps_json)
                print(gps_json)
                time.sleep(0.05)

    def close(self):
        self.socket.close()
        self.context.term()

        logger.info(f"Publisher closed. Address: {self.address}")


class Subscriber:
    def __init__(self, port, timeout=-1):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)

        # Set options
        self.socket.setsockopt(zmq.CONFLATE, 1)  # set CONFLATE for "last message only" mode.
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        if timeout > 0:
            self.socket.setsockopt(zmq.RCVTIMEO, timeout)

        # Connect
        self.socket.connect(f"tcp://localhost:{port}")

        self.none_received_count = 0

    def receive_json(self):
        try:
            data = self.socket.recv_json()
        except zmq.error.Again:
            data = None

        if data is None:
            self.none_received_count += 1
            if self.none_received_count > 10:
                logger.warning(f"No data received from subscriber after {self.none_received_count} attempts")
        else:
            self.none_received_count = 0

        return data

    def write_to_logs(self, filename):
        # Create an empty file
        with open(filename, "w") as f:
            f.write("")

        # Continuously receive and write to file
        while True:
            gps_json = self.receive_json()

            with open(filename, "a") as f:
                f.write(json.dumps(gps_json) + "\n")


PORT_GPS = 5050
PORT_POSE = 5060
PORT_CONE_DETECTIONS = 5070


def get_publisher_gps():
    return Publisher(port=PORT_GPS)


def get_subscriber_gps():
    return Subscriber(port=PORT_GPS, timeout=1)


def get_publisher_pose():
    return Publisher(port=PORT_POSE)


def get_subscriber_pose():
    return Subscriber(port=PORT_POSE, timeout=1)


def get_publisher_cone_detections():
    return Publisher(port=PORT_CONE_DETECTIONS)


def get_subscriber_cone_detections():
    return Subscriber(port=PORT_CONE_DETECTIONS, timeout=1)
