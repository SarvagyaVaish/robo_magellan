from enum import Enum, auto


class Environment(Enum):
    DEV = auto()
    PROD = auto()


ENV_TYPE = Environment.DEV

#
# Hard coded settings
#

# The Server is node running the "robot" side code.
# It is the laptop in development. And the RPi in production.
server_machine_dev = "survy-mac"
server_machine_prod = "raspberrypi"

# The Client is node that provides sensor data to the Server.
client_machine = "iphone-15-pro"

# The Server API is running on port 8000
sensor_service_port = 8000


def get_sensor_service_address():
    if ENV_TYPE == Environment.DEV:
        server_host = server_machine_dev + ".tail49268.ts.net"
    else:
        server_host = server_machine_prod + ".tail49268.ts.net"

    return server_host, sensor_service_port
