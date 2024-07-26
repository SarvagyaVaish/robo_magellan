import math
import unittest

from utils.gps import Pose, GPSPose


class TestGPS(unittest.TestCase):

    def test_gps_pose(self):
        return

        # Test for if the angle stored in the GPSPose object is converted to the map frame
        pose_deg_list = [0, 90, 180, 270, -90, -180, -270, 360]
        expected_gps_deg_list = [90, 0, 270, 180, 180, 270, 0, 90]

        for pose_deg, expected_gps_deg in zip(pose_deg_list, expected_gps_deg_list):
            pose = Pose(1e5, 1e5, math.radians(pose_deg))
            gps_pose = GPSPose(pose)

            self.assertAlmostEqual(gps_pose.th, math.radians(expected_gps_deg))


if __name__ == "__main__":
    unittest.main()
