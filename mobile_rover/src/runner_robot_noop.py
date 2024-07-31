"""
Run the State Machine against the No-op Mobile Robot.
"""

from state_machine import StateMachine
from mobile_robot_noop import MobileRobotNoop


if __name__ == "__main__":
    # Create a mobile robot
    mobile_robot = MobileRobotNoop()

    # Create a state machine to orchestrate the mission
    state_machine = StateMachine(robot=mobile_robot, mission_filename="mission.csv")

    # Run the state machine to completion
    while not state_machine.in_final_state():
        state_machine.step()
