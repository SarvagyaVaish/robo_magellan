#
# Robot behaviors
#
# Each behavior has a .step() method
# - it uses the current state of the robot to execute the behavior
# - it outputs a cmd_vel and status
#

from enum import Enum, auto
import math

from cmd_vel import CmdVel
from custom_logger import get_logger
from geometry import normalize_th_pi
from pub_sub import get_subscriber_cone_detections
from utils.gps import Pose


logger = get_logger(__name__)


class BehaviorType(Enum):
    NAV_TO_POSE = auto()
    TURN_IN_PLACE = auto()
    SEARCH_FOR_CONE = auto()


class BehaviorResult(Enum):
    NONE = auto()
    RUNNING = auto()
    SUCCESS = auto()
    ERROR = auto()


class NavToPose:
    def __init__(self, target_pose: Pose, distance_threshold: float):
        self.target_pose = target_pose
        self.distance_threshold = distance_threshold

    def step(self, current_pose: Pose) -> tuple[CmdVel, BehaviorResult]:
        # Check if we have reached the goal
        dist_to_goal = current_pose.dist(self.target_pose)
        logger.debug(f"Dist to goal: {dist_to_goal}")

        if dist_to_goal < self.distance_threshold:
            logger.debug("Goal reached")
            return CmdVel(0.0, 0.0), BehaviorResult.SUCCESS

        # Make progress towards goal
        angle_to_goal = current_pose.angle(self.target_pose)
        heading_error = angle_to_goal - current_pose.th
        heading_error = normalize_th_pi(heading_error)
        logger.debug(f"Heading error: {math.degrees(heading_error)}")

        # Calculate angular velocity.
        # When error is >= 90 deg, turn at the max rate of pi rad/sec
        angular_vel = 2 * heading_error
        angular_vel = min(max(angular_vel, -math.pi), math.pi)

        # Calculate linear velocity.
        # When error is >= 90 deg, go slow. When error is 0, go at the max speed of 1 m/sec.
        if abs(heading_error) >= math.pi / 2:
            linear_vel = 0.1
        else:
            linear_vel = -2 / math.pi * abs(heading_error) + 1

        cmd_vel = CmdVel(linear_vel, angular_vel)
        return cmd_vel, BehaviorResult.RUNNING


class TurnInPlace:
    # TODO: Support turning in both directions.
    # TODO: Support timeout

    def __init__(self, rotation_th, speed_rpm):
        self.rotation_th = rotation_th
        self.speed_rpm = speed_rpm

        self.starting_th = None
        self.has_moved_enough = False

    def step(self, current_pose: Pose) -> tuple[CmdVel, BehaviorResult]:
        if self.starting_th is None:
            self.starting_th = current_pose.th

        # Measure the change in angle from the starting angle, in the right hand coordinate system.
        logger.debug(
            "Starting th: {}, current th: {}, rotation_th: {}".format(
                math.degrees(self.starting_th),
                math.degrees(current_pose.th),
                math.degrees(self.rotation_th),
            )
        )

        if current_pose.th >= self.starting_th:
            delta_th = current_pose.th - self.starting_th
        else:
            logger.debug("Current th is less than starting th. Adding 2pi to current th.")
            delta_th = 2 * math.pi + current_pose.th - self.starting_th

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


class SearchForCone:
    def __init__(self):
        self.turn_in_place = TurnInPlace(rotation_th=2 * math.pi, speed_rpm=4)
        self.cone_detections_subscriber = get_subscriber_cone_detections()

    def step(self, current_pose: Pose) -> tuple[CmdVel, BehaviorResult]:
        data = self.cone_detections_subscriber.receive_json()

        # If we found a cone, stop turning and return success
        if data is not None:
            logger.debug(f"Got cone detection: {data}")
            return CmdVel(), BehaviorResult.SUCCESS

        # Otherwise, continue to turn in place
        cmd_vel, turn_result = self.turn_in_place.step(current_pose)

        # If there is more turning to do, keep turning and return running
        if turn_result == BehaviorResult.RUNNING:
            return cmd_vel, BehaviorResult.RUNNING

        # If no longer turning, return failure
        return cmd_vel, BehaviorResult.ERROR
