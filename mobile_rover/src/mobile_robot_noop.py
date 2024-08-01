from behaviors import BehaviorResult, BehaviorType, NoopBehavior
from mobile_robot_base import MobileRobotBase


class MobileRobotNoop(MobileRobotBase):
    def __init__(self):
        self.behavior = None

    def start_behavior(self, behavior_type: BehaviorType, **kwargs):
        self.behavior = NoopBehavior()

    def step(self) -> BehaviorResult:
        cmd_vel, behavior_result = self.behavior.step(current_pose=None)
        return behavior_result
