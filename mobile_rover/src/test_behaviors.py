import math
import unittest

from behaviors import TurnInPlace, BehaviorResult


class TestBehaviors(unittest.TestCase):

    def test_turn_in_place(self):
        starting_th_list = [math.radians(0), math.radians(0), math.radians(360 - 45)]
        rotation_th_list = [math.radians(180), math.radians(360), math.radians(90)]
        expected_th_list = [math.radians(180), math.radians(360), math.radians(315 + 90)]
        expected_duration_list = [0.5, 1.0, 0.25]

        rate = 1e5

        for starting_th, rotation_th, expected_th, expected_duration in zip(
            starting_th_list, rotation_th_list, expected_th_list, expected_duration_list
        ):
            turning = TurnInPlace(starting_th, rotation_th, 60)
            behavior_duration = 0
            current_th = starting_th

            while True:
                cmd_vel, result = turning.step(current_th)
                if result == BehaviorResult.SUCCESS:
                    break
                behavior_duration += 1 / rate
                current_th += cmd_vel.angular_vel * (1 / rate)

            assert abs(math.degrees(current_th) - math.degrees(expected_th)) < 0.01
            assert abs(behavior_duration - expected_duration) < 0.01


if __name__ == "__main__":
    unittest.main()
