import copy
import math
import json
import time

from scipy.spatial import distance
import click
import utm

from pub_sub import get_publisher_gps, get_subscriber_gps
from pub_sub import get_publisher_pose


def gps_to_pose(gps):
    easting, northing, _, _ = utm.from_latlon(gps["latitude"], gps["longitude"])
    heading = gps["heading"]
    return {"x": easting, "y": northing, "th": heading}


def distace_between_poses(pose1, pose2):
    xy1 = [pose1["x"], pose1["y"]]
    xy2 = [pose2["x"], pose2["y"]]

    return distance.euclidean(xy1, xy2)


def heading_between_poses(pose1, pose2):
    dx = pose2["x"] - pose1["x"]
    dy = pose2["y"] - pose1["y"]

    # Calculate the angle in radians
    angle_rad = math.atan2(dy, dx)

    # Normalize to 0-2π radians
    heading = angle_rad % (2 * math.pi)

    return heading


@click.command()
@click.option("--write-logs", is_flag=True, default=False, help="Subscribe and write data to log file")
@click.option("--replay-logs", is_flag=True, default=False, help="Publish data from log file")
@click.option("--log-filename", default="gps.data", help="Name of log file")
def main(write_logs, replay_logs, log_filename):
    # with open("pose_log.data", "w") as f:
    #     f.write("")

    if write_logs:
        print(f"Writing data to {log_filename}")
        gps_subscriber = get_subscriber_gps()
        gps_subscriber.write_to_logs(log_filename)

    elif replay_logs:
        print(f"Replaying data from {log_filename}")
        gps_publisher = get_publisher_gps()
        gps_publisher.read_from_logs(log_filename)

    else:
        print("Starting pose estimator")
        gps_subscriber = get_subscriber_gps()
        pose_publisher = get_publisher_pose()

        heading_pose = None
        current_pose = None
        prev_pose = None

        rate = 5

        while True:
            time.sleep(1 / rate)
            prev_pose = copy.deepcopy(current_pose)

            # Get current pose from GPS
            gps_json = gps_subscriber.receive_json()
            if gps_json is None:
                continue
            current_pose = gps_to_pose(gps_json)

            # # Initialize pose estimator
            # if heading_pose is None:
            #     heading_pose = copy.deepcopy(current_pose)
            #     print("Pose estimator initialized")

            # # If we moved, calculate heading
            # if distace_between_poses(current_pose, heading_pose) > 0.25:
            #     th = heading_between_poses(heading_pose, current_pose)
            #     current_pose["th"] = th
            #     if prev_pose is not None and prev_pose.get("th", None) is not None:
            #         current_pose["th"] = 0.5 * current_pose["th"] + 0.5 * prev_pose["th"]
            #     heading_pose = copy.deepcopy(current_pose)
            # elif prev_pose is not None:
            #     current_pose["th"] = prev_pose.get("th", None)

            pose_publisher.send_json(current_pose)
            th_deg = math.degrees(current_pose["th"])
            print(f"x: {current_pose['x']}, y: {current_pose['y']}, th: {th_deg}")

            # with open("pose_log.data", "a") as f:
            #     f.write(json.dumps(current_pose) + "\n")


if __name__ == "__main__":
    main()
