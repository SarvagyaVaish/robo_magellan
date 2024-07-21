from utils.gps import Pose


class MobileRobot:
    def __init__(self, x, y, th):
        self.pose = Pose(x, y, th)

    def go_to(self, target_pose):
        self.pose.x += (target_pose.x - self.pose.x) * 0.9
        self.pose.y += (target_pose.y - self.pose.y) * 0.9
