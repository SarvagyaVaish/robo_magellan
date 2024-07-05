import json
import zmq
import time

from custom_logger import get_logger


logger = get_logger(__name__, "info")


class Publisher:
    def __init__(self, port=5050):
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
    def __init__(self, port=5050):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect(f"tcp://localhost:{port}")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")

    def receive_json(self):
        return self.socket.recv_json()

    def write_to_logs(self, filename):
        # Create an empty file
        with open(filename, "w") as f:
            f.write("")

        # Continuously receive and write to file
        while True:
            gps_json = self.receive_json()

            with open(filename, "a") as f:
                f.write(json.dumps(gps_json) + "\n")
