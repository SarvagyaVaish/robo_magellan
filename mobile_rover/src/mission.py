from custom_logger import get_logger
from utils.gps import GPSWaypoint


logger = get_logger("mission")


class Mission:
    def __init__(self):
        self.waypoints = []
        self.current_waypoint_idx = -1

    def load_from_file(self, filename):
        # Reset
        self.waypoints = []
        self.current_waypoint_idx = -1

        # Sample data:
        #   37.5712, -122.3006, route
        with open(filename, "r") as f:
            for line in f:
                lat, lon, waypoint_type = line.strip().split(",")
                waypoint = GPSWaypoint(float(lat), float(lon), waypoint_type.strip())
                self.waypoints.append(waypoint)

        logger.info(f"Loaded {len(self.waypoints)} waypoints from '{filename}'")
        for i, waypoint in enumerate(self.waypoints):
            if waypoint.is_route:
                logger.info(f"Waypoint {i}: 📍 {waypoint.gps.lat}, {waypoint.gps.lon}")
            elif waypoint.is_bonus:
                logger.info(f"Waypoint {i}: ⭐ {waypoint.gps.lat}, {waypoint.gps.lon}")
            elif waypoint.is_goal:
                logger.info(f"Waypoint {i}: 🏁 {waypoint.gps.lat}, {waypoint.gps.lon}")

    def get_current_waypoint(self) -> GPSWaypoint:
        return self.waypoints[self.current_waypoint_idx]

    def go_to_next_waypoint(self):
        self.current_waypoint_idx += 1

    def is_mission_complete(self) -> bool:
        return self.current_waypoint_idx >= len(self.waypoints)

    def visualize_mission(self, output_file="mission.html"):
        import folium

        # Calculate the center of the map
        center_lat = sum(wp.gps.lat for wp in self.waypoints) / len(self.waypoints)
        center_lon = sum(wp.gps.lon for wp in self.waypoints) / len(self.waypoints)

        # Create a map centered on the average coordinates
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=21,
            max_zoom=22,
            tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
            attr="Google",
            name="Google Satellite",
        )

        # Add the OpenStreetMap tile layer
        folium.TileLayer("OpenStreetMap").add_to(m)
        folium.LayerControl().add_to(m)

        # Add markers for each waypoint
        # Icons: https://getbootstrap.com/docs/3.3/components/#glyphicons
        for wp in self.waypoints:
            if wp.is_route:
                icon = folium.Icon(color="red", icon="pushpin")
                popup = "Route Waypoint"
            elif wp.is_bonus:
                icon = folium.Icon(color="orange", icon="star")
                popup = "Bonus Waypoint"
            elif wp.is_goal:
                icon = folium.Icon(color="black", icon="flag")
                popup = "Goal Waypoint"
            else:
                icon = folium.Icon(color="gray", icon="question-sign")
                popup = "Unknown Waypoint"

            folium.Marker(location=[wp.gps.lat, wp.gps.lon], popup=popup, icon=icon).add_to(m)

        # Add lines connecting the waypoints in order
        folium.PolyLine(locations=[(wp.gps.lat, wp.gps.lon) for wp in self.waypoints], color="blue", weight=3).add_to(m)

        # Save the map to an HTML file
        m.save(output_file)
        print(f"Map saved to {output_file}")


if __name__ == "__main__":
    mission = Mission()
    mission.load_from_file()
    mission.visualize_mission()
