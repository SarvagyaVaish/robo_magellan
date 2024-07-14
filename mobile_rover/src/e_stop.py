import time
from motors import stop_motors, set_motor_speeds

while True:
    stop_motors()
    time.sleep(.001)
