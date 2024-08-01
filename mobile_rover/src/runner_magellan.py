"""
Run the State Machine against the physical Magellan Mobile Robot.
"""

import time

from mobile_robot_magellan import MobileRobotMagellan
from state_machine import StateMachine


rate = 2

if __name__ == "__main__":
    # Create a mobile robot
    mobile_robot = MobileRobotMagellan()
    mobile_robot.wait_for_pose()

    # Create a state machine to orchestrate the mission
    state_machine = StateMachine(robot=mobile_robot, mission_filename="mission.csv")

    # Run the state machine to completion
    while not state_machine.in_final_state():
        state_machine.step()

        time.sleep(1 / rate)

    mobile_robot.visualize_path()
