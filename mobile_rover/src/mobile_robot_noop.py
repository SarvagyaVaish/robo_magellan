from behaviors import BehaviorResult, BehaviorType
from mobile_robot_base import MobileRobotBase


STEPS_PER_BEHAVIOR = 5


class MobileRobotNoop(MobileRobotBase):
    def __init__(self):
        self.behavior_step_count = 0

    def start_behavior(self, behavior_type: BehaviorType, **kwargs):
        self.behavior_step_count = 0

    def step(self) -> BehaviorResult:
        self.behavior_step_count += 1

        if self.behavior_step_count < STEPS_PER_BEHAVIOR:
            return BehaviorResult.RUNNING
        else:
            return BehaviorResult.SUCCESS
