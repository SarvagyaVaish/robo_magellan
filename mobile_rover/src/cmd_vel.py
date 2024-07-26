class CmdVel:
    def __init__(self, linear_vel=0, angular_vel=0):
        self.linear_vel = linear_vel
        self.angular_vel = angular_vel

    def __str__(self) -> str:
        return f"CmdVel(linear_vel={self.linear_vel:.4f}, angular_vel={self.angular_vel:.4f})"
