class CmdVel:
    def __init__(self, linear_vel=0, angular_vel=0):
        self.linear_vel = linear_vel
        self.angular_vel = angular_vel

    def __str__(self):
        return "CmdVel(linear_vel={}, angular_vel={})".format(self.linear_vel, self.angular_vel)
