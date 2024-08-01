"""
A StateMachine that encapsulates the logic and orchestrates the Mission.

- It takes in a Mobile Robot and a Mission file
- It executes the Mission by executing the right Behavior on the Robot
"""

from enum import Enum, auto
import logging

from transitions import Machine

from behaviors import BehaviorResult, BehaviorType
from custom_logger import get_logger
from mission import Mission
from mobile_robot_base import MobileRobotBase


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
    MISSION_COMPLETE = auto()
    CONE_LOST = auto()
    ERROR = auto()


class StateMachine:
    def __init__(self, robot: MobileRobotBase, mission_filename: str):
        # The entity that the state machine will control
        self.robot = robot
        self.mission_filename = mission_filename
        self.mission = None  # type: Mission

        # Create the state machine
        self.machine = Machine(model=self, states=State, initial=State.START)
        self.machine.get_state(State.END.name).final = True

        # Define transitions
        self.machine.add_transition(Transition.START_MISSION.name, State.START, State.IDLING)
        self.machine.add_transition(Transition.NEW_WAYPOINT.name, State.IDLING, State.NAVIGATING_TO_WAYPOINT)
        self.machine.add_transition(Transition.MISSION_COMPLETE.name, State.IDLING, State.END)
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
        self.machine.add_transition(Transition.ERROR.name, "*", State.END)

    #
    # START
    #

    def step_START(self):
        # Load the mission from a CSV file
        self.mission = Mission()
        self.mission.load_from_file(filename=self.mission_filename)

        # Transition out of state
        logger.info(" ⚡ START_MISSION")
        self.START_MISSION()

    #
    # IDLING
    #

    def step_IDLING(self):
        logger.info(" ▶️  IDLING")
        self.mission.go_to_next_waypoint()

        if self.mission.is_mission_complete():
            logger.info(" ⚡ MISSION_COMPLETE")
            self.MISSION_COMPLETE()
        else:
            logger.info(" ⚡ NEW_WAYPOINT")
            self.NEW_WAYPOINT()

    #
    # NAVIGATING_TO_WAYPOINT
    #

    def on_enter_NAVIGATING_TO_WAYPOINT(self):
        target_waypoint_idx = self.mission.get_current_waypoint_idx()
        logger.info(f" ✅ NAVIGATING_TO_WAYPOINT ({target_waypoint_idx})")

        target_waypoint = self.mission.get_current_waypoint()
        target_pose = target_waypoint.gps.to_pose()
        distance_threshold = 1.0
        self.robot.start_behavior(
            BehaviorType.NAV_TO_POSE,
            target_pose=target_pose,
            distance_threshold=distance_threshold,
        )

    def step_NAVIGATING_TO_WAYPOINT(self):
        logger.info(" ▶️  NAVIGATING_TO_WAYPOINT")

        behavior_result = self.robot.step()
        if behavior_result == BehaviorResult.SUCCESS:
            logger.info(" ⚡ REACHED_WAYPOINT")
            self.REACHED_WAYPOINT()
        elif behavior_result == BehaviorResult.ERROR:
            logger.info(" ⚡ ERROR")
            self.ERROR()

    #
    # SEARCHING_FOR_CONE
    #

    def on_enter_SEARCHING_FOR_CONE(self):
        logger.info(" ✅ SEARCHING_FOR_CONE")

        self.robot.start_behavior(BehaviorType.SEARCH_FOR_CONE)

    def step_SEARCHING_FOR_CONE(self):
        logger.info(" ▶️  SEARCHING_FOR_CONE")

        behavior_result = self.robot.step()
        if behavior_result == BehaviorResult.SUCCESS:
            logger.info(" ⚡ CONE_FOUND")
            self.CONE_FOUND()
        elif behavior_result == BehaviorResult.ERROR:
            logger.info(" ⚡ ERROR")
            self.ERROR()

    #
    # APPROACHING_CONE
    #

    def step_APPROACHING_CONE(self):
        logger.info(" ▶️  APPROACHING_CONE")
        logger.info(" ⚡ NEAR_CONE")
        self.NEAR_CONE()

    #
    # ENSURING_CONTACT
    #

    def step_ENSURING_CONTACT(self):
        logger.info(" ▶️  ENSURING_CONTACT")
        logger.info(" ⚡ CONTACT_MADE")
        self.CONTACT_MADE()

    #
    # Step
    #

    def step(self):
        # Call the self.step_* method for the current state
        getattr(self, f"step_{self.state.name}")()

    #
    # Helpers
    #

    def should_look_for_cone(self):
        return not self.mission.get_current_waypoint().is_route

    def in_final_state(self):
        return self.machine.get_state(self.state).final
