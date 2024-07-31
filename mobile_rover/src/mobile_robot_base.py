from abc import ABC, abstractmethod

from behaviors import BehaviorResult, BehaviorType


class MobileRobotBase(ABC):
    @abstractmethod
    def start_behavior(self, behavior_type: BehaviorType, **kwargs):
        pass

    @abstractmethod
    def step(self) -> BehaviorResult:
        pass
