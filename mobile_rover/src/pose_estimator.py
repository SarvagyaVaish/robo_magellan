import math

from scipy.spatial import distance
import utm

from pub_sub import get_subscriber_gps
from pub_sub import get_publisher_pose


def gps_to_pose(gps):
    easting, northing, _, _ = utm.from_latlon(gps["latitude"], gps["longitude"])
    gps_heading = gps["heading"]
    heading = math.pi / 2 - gps_heading
    return {"x": easting, "y": northing, "th": heading}


def main():
    print("Starting pose estimator")
    gps_subscriber = get_subscriber_gps()
    pose_publisher = get_publisher_pose()

    while True:
        # Get current pose from GPS
        gps_json = gps_subscriber.receive_json()
        if gps_json is None:
            continue
        current_pose = gps_to_pose(gps_json)

        pose_publisher.send_json(current_pose)
        th_deg = math.degrees(current_pose["th"])
        print(f"x: {current_pose['x']}, y: {current_pose['y']}, th: {th_deg}")


if __name__ == "__main__":
    main()
