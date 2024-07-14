from roboclaw import Roboclaw

# Initialize Roboclaw
roboclaw = Roboclaw("/dev/ttyAMA0", 38400)
roboclaw.Open()

# Roboclaw addresses
ADDRESS_LEFT = 0x80
ADDRESS_RIGHT = 0x81

# Max speed (adjust as needed)
MAX_SPEED = 3000


def set_motor_speeds(right_speed, left_speed):
    roboclaw.SpeedM1M2(ADDRESS_RIGHT, int(right_speed * MAX_SPEED), int(right_speed * MAX_SPEED))
    roboclaw.SpeedM1M2(ADDRESS_LEFT, int(left_speed * MAX_SPEED), int(left_speed * MAX_SPEED))


def stop_motors():
    set_motor_speeds(0, 0)
