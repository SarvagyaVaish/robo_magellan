import logging
from enum import Enum, auto

from transitions import Machine

from custom_logger import get_logger
from mission import Mission
from mobile_robot_sim import MobileRobot


# TODO: figure out how to enable state machine internal logger
logging.basicConfig(level=logging.DEBUG)
logging.getLogger("transitions").setLevel(logging.WARN)

logger = get_logger("state_machine")


class State(Enum):
    START = auto()
    IDLING = auto()
    NAVIGATING_TO_WAYPOINT = auto()
    SEARCHING_FOR_CONE = auto()
    APPROACHING_CONE = auto()
    ENSURING_CONTACT = auto()
    END = auto()


class Transition(Enum):
    START_MISSION = auto()
    NEW_WAYPOINT = auto()
    REACHED_WAYPOINT = auto()
    CONE_FOUND = auto()
    NEAR_CONE = auto()
    CONTACT_MADE = auto()
    REACHED_GOAL = auto()
    CONE_LOST = auto()


class StateMachine:
    def __init__(self, robot):
        # The entity that the state machine will control
        self.robot = robot  # type: MobileRobot
        self.mission = None

        # Create the state machine
        self.machine = Machine(model=self, states=State, initial=State.START)
        self.machine.get_state(State.END.name).final = True

        # Define transitions
        self.machine.add_transition(Transition.START_MISSION.name, State.START, State.IDLING)
        self.machine.add_transition(Transition.NEW_WAYPOINT.name, State.IDLING, State.NAVIGATING_TO_WAYPOINT)
        self.machine.add_transition(Transition.REACHED_GOAL.name, State.IDLING, State.END)
        self.machine.add_transition(
            Transition.REACHED_WAYPOINT.name,
            State.NAVIGATING_TO_WAYPOINT,
            State.SEARCHING_FOR_CONE,
            conditions=self.should_look_for_cone,
        )
        self.machine.add_transition(
            Transition.REACHED_WAYPOINT.name,
            State.NAVIGATING_TO_WAYPOINT,
            State.IDLING,
            conditions=lambda: not self.should_look_for_cone(),
        )
        self.machine.add_transition(Transition.CONE_FOUND.name, State.SEARCHING_FOR_CONE, State.APPROACHING_CONE)
        self.machine.add_transition(Transition.NEAR_CONE.name, State.APPROACHING_CONE, State.ENSURING_CONTACT)
        self.machine.add_transition(Transition.CONTACT_MADE.name, State.ENSURING_CONTACT, State.IDLING)
        self.machine.add_transition(Transition.CONE_LOST.name, State.APPROACHING_CONE, State.SEARCHING_FOR_CONE)

    #
    # START
    #

    def step_START(self):
        print("Start")

        # Load the mission from a CSV file
        if self.mission is None:
            self.mission = Mission()
            self.mission.load_from_file()

        # Transition out of state
        self.START_MISSION()

    #
    # IDLING
    #

    def step_IDLING(self):
        print("Idling")
        self.mission.go_to_next_waypoint()

        if self.mission.is_mission_complete():
            self.REACHED_GOAL()
        else:
            self.NEW_WAYPOINT()

    #
    # NAVIGATING_TO_WAYPOINT
    #

    def step_NAVIGATING_TO_WAYPOINT(self):
        print("Navigating to waypoint")

        current_waypoint = self.mission.get_current_waypoint()
        waypoint_pose = current_waypoint.gps.to_pose()
        dist_from_waypoint = self.robot.pose.dist(waypoint_pose)

        # print(f"Robot pose: {self.robot.pose}")

        if dist_from_waypoint < 2:
            self.REACHED_WAYPOINT()
        else:
            self.robot.go_to(waypoint_pose)

    def should_look_for_cone(self):
        return not self.mission.get_current_waypoint().is_route

    #
    # SEARCHING_FOR_CONE
    #

    def step_SEARCHING_FOR_CONE(self):
        print("Searching for cone")
        self.CONE_FOUND()

    #
    # APPROACHING_CONE
    #

    def step_APPROACHING_CONE(self):
        print("Approaching cone")
        self.NEAR_CONE()

    #
    # ENSURING_CONTACT
    #

    def step_ENSURING_CONTACT(self):
        print("Ensuring contact with cone")
        self.CONTACT_MADE()

    #
    # Step
    #

    def step(self):
        # Call the self.step_* method for the current state
        getattr(self, f"step_{self.state.name}")()

    def in_final_state(self):
        return self.machine.get_state(self.state).final


if __name__ == "__main__":
    # Create a mobile robot
    mobile_robot = MobileRobot(0, 0, 0)

    # Create a state machine to orchestrate the mission
    state_machine = StateMachine(robot=mobile_robot)

    while not state_machine.in_final_state():
        state_machine.step()
