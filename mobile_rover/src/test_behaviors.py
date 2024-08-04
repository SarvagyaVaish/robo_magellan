import math
import unittest

from behaviors import TurnInPlace, BehaviorResult, NavToPose
from utils.gps import Pose


class TestBehaviors(unittest.TestCase):

    def test_nav_to_pose(self):
        starting_pose_list = [Pose(0, 0, 0), Pose(-1, 0, 0), Pose(-1, 0, 0)]
        target_pose_list = [Pose(1, 0, 0), Pose(0, 1, 0), Pose(0, -1, 0)]
        expected_linear_vel_list = [1.0, 0.5, 0.5]
        expected_angular_vel_list = [0.0, math.pi / 2, -math.pi / 2]

        for starting_pose, target_pose, expected_linear_vel, expected_angular_vel in zip(
            starting_pose_list, target_pose_list, expected_linear_vel_list, expected_angular_vel_list
        ):
            behavior = NavToPose(target_pose, 0.1)
            cmd_vel, result = behavior.step(starting_pose)

            assert abs(cmd_vel.linear_vel - expected_linear_vel) < 0.01
            assert abs(cmd_vel.angular_vel - expected_angular_vel) < 0.01

    def test_turn_in_place(self):
        starting_th_list = [math.radians(0), math.radians(0), math.radians(360 - 45)]
        rotation_th_list = [math.radians(180), math.radians(360), math.radians(90)]
        expected_th_list = [math.radians(180), math.radians(360), math.radians(315 + 90)]
        expected_duration_list = [0.5, 1.0, 0.25]

        rate = 1e5

        for starting_th, rotation_th, expected_th, expected_duration in zip(
            starting_th_list, rotation_th_list, expected_th_list, expected_duration_list
        ):
            behavior = TurnInPlace(rotation_th, speed_rpm=60)
            behavior_duration = 0
            current_th = starting_th

            while True:
                cmd_vel, result = behavior.step(Pose(0, 0, current_th))
                if result == BehaviorResult.SUCCESS:
                    break
                behavior_duration += 1 / rate
                current_th += cmd_vel.angular_vel * (1 / rate)

            assert abs(math.degrees(current_th) - math.degrees(expected_th)) < 0.01
            assert abs(behavior_duration - expected_duration) < 0.01


if __name__ == "__main__":
    unittest.main()
