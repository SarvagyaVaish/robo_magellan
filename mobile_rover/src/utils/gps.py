from __future__ import annotations
import math
import re
import utm

from scipy.spatial import distance

from cmd_vel import CmdVel
from geometry import normalize_th_2pi


class Pose:
    """
    Represents a 3D pose with x, y, and theta coordinates.
    """

    def __init__(self, x, y, th):
        self.x = x
        self.y = y
        self.th = th

    def __str__(self) -> str:
        return f"Pose(x={self.x:.2f}, y={self.y:.2f}, th={self.th})"

    def update(self, cmd_vel: CmdVel, dt: float):
        self.th += cmd_vel.angular_vel * dt
        self.x += cmd_vel.linear_vel * math.cos(self.th) * dt
        self.y += cmd_vel.linear_vel * math.sin(self.th) * dt

    def dist(self, second_pose):
        xy1 = [self.x, self.y]
        xy2 = [second_pose.x, second_pose.y]

        return distance.euclidean(xy1, xy2)

    def angle(self, second_pose):
        # Calculate angle from self to second_pose
        dx = second_pose.x - self.x
        dy = second_pose.y - self.y

        # Calculate the angle in radians, in the range [0, 2π]
        angle_rad = normalize_th_2pi(math.atan2(dy, dx))

        return angle_rad

    def copy(self) -> Pose:
        return Pose(self.x, self.y, self.th)


class GPSCoordinate:
    """
    Represents a GPS latitude and longitude coordinates.

    Note: UTM zone is hard coded to 10S: https://www.dmap.co.uk/utmworld.htm
          TODO: Generalize to all zones
    """

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def to_pose(self) -> Pose:
        easting, northing, _, _ = utm.from_latlon(self.lat, self.lon)
        return Pose(easting, northing, None)

    def __str__(self) -> str:
        return f"GPSCoordinate(lat={self.lat:.4f}, lon={self.lon:.4f})"

    @staticmethod
    def from_pose(pose) -> GPSCoordinate:
        lat, lon = utm.to_latlon(pose.x, pose.y, 10, "S")
        return GPSCoordinate(lat, lon)


class GPSPose:
    """
    A GPS Coordinate plus a Heading.
    Heading is stored in cartesian frame, not map frame. 0 radians points to the right and increases counterclockwise.

    To convert to map frame with 0 radians pointing North, use:
        map_th = math.pi / 2 - cart_th
    """

    def __init__(self, pose: Pose):
        lat, lon = utm.to_latlon(pose.x, pose.y, 10, "S")
        self.lat = lat
        self.lon = lon

        # Use heading as is
        self.th = pose.th

        # Normalize to 0-2π radians
        self.th = (self.th + 2 * math.pi) % (2 * math.pi)


class GPSWaypoint:
    """
    A GPS Coordinate plus a Waypoint Type.
    Types of Waypoints: | route | bonus | goal |
    """

    def __init__(self, lat, lon, waypoint_type):
        self.gps = GPSCoordinate(lat, lon)

        self.is_route = False
        self.is_bonus = False
        self.is_goal = False
        if waypoint_type == "route":
            self.is_route = True
        elif waypoint_type == "bonus":
            self.is_bonus = True
        elif waypoint_type == "goal":
            self.is_goal = True
        else:
            raise ValueError(f"Invalid waypoint type: {waypoint_type}. Must be 'route', 'bonus', or 'goal'.")

    def __str__(self) -> str:
        icon = "🏁" if self.is_goal else "⭐" if self.is_bonus else "📍"
        return f"GPSWaypoint(lat={self.gps.lat:.4f}, lon={self.gps.lon:.4f}) {icon}"


if __name__ == "__main__":
    gps1 = GPSCoordinate(37.57125784995419, -122.30067882311883)
    pose1 = gps1.to_pose()
    pose2 = Pose(pose1.x + 100, pose1.y, pose1.th)
    gps2 = GPSCoordinate.from_pose(pose2)
    print(gps1)
    print(gps2)


def dms_to_decimal(gps_str):
    # Regular expression to match the GPS format
    pattern = r"([NS])\s*(\d+)\s+(\d+\.\d+)\s+([EW])\s*(\d+)\s+(\d+\.\d+)"

    match = re.match(pattern, gps_str)
    if not match:
        raise ValueError("Invalid GPS format")

    lat_dir, lat_deg, lat_min, lon_dir, lon_deg, lon_min = match.groups()

    # Convert to decimal degrees
    lat = float(lat_deg) + float(lat_min) / 60
    lon = float(lon_deg) + float(lon_min) / 60

    # Adjust sign based on direction
    if lat_dir == "S":
        lat = -lat
    if lon_dir == "W":
        lon = -lon

    return f"{lat:.14f}, {lon:.14f}"

    # # Example usage
    # gps_str = "N 47 22.1245 W 122 32.0493"
    # result = dms_to_decimal(gps_str)
    # print(f"Input: {gps_str}")
    # print(f"Output: {result}")
