import math

from custom_logger import get_logger
from behaviors import BehaviorResult, BehaviorType, NavToPose
from utils.gps import GPSPose, Pose

logger = get_logger(__name__)
dt = 0.1  # seconds


class MobileRobot:
    def __init__(self, x, y, th):
        self.pose = Pose(x, y, th)
        self.behavior = None
        self.path = []  # type: list[Pose]

    def start_behavior(self, behavior_type, **kwargs):
        if behavior_type == BehaviorType.NAV_TO_POSE:
            target_pose = kwargs.get("target_pose")
            distance_threshold = kwargs.get("distance_threshold")
            self.behavior = NavToPose(target_pose, distance_threshold)

        elif behavior_type == BehaviorType.TURN_IN_PLACE:
            pass

        else:
            raise ValueError(f"Invalid behavior type: {behavior_type}")

    def step(self) -> BehaviorResult:
        cmd_vel, behavior_result = self.behavior.step(self.pose)
        self.pose.update(cmd_vel, dt)

        # Keep track of the path
        p = self.pose.copy()
        p.th
        self.path.append(self.pose.copy())

        return behavior_result

    def visualize_path(self, output_file="path.html"):
        import folium
        from branca.colormap import LinearColormap

        # Convert Poses to GPS Poses.
        path_gps = [GPSPose(pose) for pose in self.path]

        # Calculate the center of the map
        center_lat = sum(gp.lat for gp in path_gps) / len(path_gps)
        center_lon = sum(gp.lon for gp in path_gps) / len(path_gps)

        # Create a map centered on the average coordinates
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=21,
            max_zoom=35,
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satellite",
        )

        # Add the OpenStreetMap tile layer
        folium.TileLayer("OpenStreetMap").add_to(m)
        folium.LayerControl().add_to(m)

        # Create a color map
        colormap = LinearColormap(colors=["red", "yellow", "green", "blue", "red"], vmin=0, vmax=360)

        # Prepare data for PolyLine
        points = [(gp.lat, gp.lon) for gp in path_gps]
        headings = [math.degrees(gp.th) for gp in path_gps]

        # Add colored line segments to the map
        for i in range(len(points) - 1):
            color = colormap(headings[i])
            folium.PolyLine(
                locations=[points[i], points[i + 1]],
                tooltip=f"Heading: {headings[i]:.2f}°",
                color=color,
                weight=4,
            ).add_to(m)

        # Add a color bar legend
        colormap.add_to(m)
        colormap.caption = "Heading (degrees)"

        # Save the map to an HTML file
        m.save(output_file)
        print(f"Map saved to {output_file}")
