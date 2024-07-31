"""
Run the State Machine against the Simulated Mobile Robot.
"""

import math
from random import random

from mobile_robot_sim import MobileRobotSim
from pub_sub import get_publisher_cone_detections
from state_machine import StateMachine, State
from utils.gps import GPSCoordinate


if __name__ == "__main__":
    # Create a starting pose for the robot, and add some noise to it
    j = random() / 10000.0
    robot_init_gps = GPSCoordinate(37.57128 + j, -122.30064 + j)  # Survy's backyard
    robot_init_pose = robot_init_gps.to_pose()

    # Create a mobile robot at the starting pose, facing north
    mobile_robot = MobileRobotSim(robot_init_pose.x, robot_init_pose.y, math.pi / 2)

    # Create a state machine to orchestrate the mission
    state_machine = StateMachine(robot=mobile_robot, mission_filename="mission.csv")

    # Create a cone detection publisher to send out fake cone detections
    cone_detections_publisher = get_publisher_cone_detections()

    # Run the state machine to completion
    while not state_machine.in_final_state():
        state_machine.step()

        if state_machine.state == State.SEARCHING_FOR_CONE:
            cone_detections_publisher.send_json({})

    mobile_robot.visualize_path()
