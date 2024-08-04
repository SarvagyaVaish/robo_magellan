"""
Run a specific behavior against the physical Magellan Mobile Robot.
"""

import signal
import sys
import time

from behaviors import BehaviorType, BehaviorResult
from mobile_robot_magellan import MobileRobotMagellan
from motors import stop_motors


def signal_handler(sig, frame):
    stop_motors()
    sys.exit(0)


rate = 2

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create a mobile robot
    mobile_robot = MobileRobotMagellan()
    mobile_robot.wait_for_pose()
    mobile_robot.start_behavior(behavior_type=BehaviorType.SEARCH_FOR_CONE)

    # Run the state machine to completion
    while True:
        result = mobile_robot.step()
        if result == BehaviorResult.SUCCESS:
            print("Success!")
            break
        elif result == BehaviorResult.ERROR:
            print("Error!")
            break

        time.sleep(1 / rate)
