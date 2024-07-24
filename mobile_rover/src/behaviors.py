import math
from enum import Enum, auto

from cmd_vel import CmdVel
from custom_logger import get_logger


logger = get_logger(__name__)


class Behavior(Enum):
    TURN_IN_PLACE = auto()


class BehaviorResult(Enum):
    NONE = auto()
    RUNNING = auto()
    SUCCESS = auto()
    ERROR = auto()


class TurnInPlace:
    # TODO: Support turning in both directions.
    # TODO: Support timeout

    def __init__(self, starting_th, rotation_th, speed_rpm):
        self.starting_th = starting_th
        self.rotation_th = rotation_th
        self.speed_rpm = speed_rpm

        self.has_moved_enough = False

    def step(self, current_th) -> tuple[CmdVel, bool]:
        # Measure the change in angle from the starting angle, in the right hand coordinate system.
        logger.debug(
            "Starting th: {}, current th: {}, rotation_th: {}".format(
                math.degrees(self.starting_th),
                math.degrees(current_th),
                math.degrees(self.rotation_th),
            )
        )

        if current_th >= self.starting_th:
            delta_th = current_th - self.starting_th
        else:
            logger.debug("Current th is less than starting th. Adding 2pi to current th.")
            delta_th = 2 * math.pi + current_th - self.starting_th

        # Check if it seems like we have moved a whole lot, but are actually within the sensor noise.
        if not self.has_moved_enough and delta_th > math.radians(270):
            logger.debug("Unexpected large delta_th. Setting delta-th to 0.")
            delta_th = 0

        # Check if we have moved more than 25% of the way. If so, it's safe to say we are making progress.
        if not self.has_moved_enough and delta_th > 0.25 * self.rotation_th:
            logger.debug("Moved more than 25%.")
            self.has_moved_enough = True

        # Construct a CmdVel
        if delta_th < self.rotation_th:
            angular_vel = self.speed_rpm / 60 * 2 * math.pi
            cmd_vel = CmdVel(angular_vel=angular_vel)
            return cmd_vel, BehaviorResult.RUNNING
        else:
            logger.debug("Moved more than target rotation angle. Returning success.")
            cmd_vel = CmdVel()
            return cmd_vel, BehaviorResult.SUCCESS
