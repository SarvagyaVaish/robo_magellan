import math

from scipy.spatial import distance
import click
import utm

from pub_sub import get_subscriber_pose
from motors import set_motor_speeds, stop_motors


def gps_to_xy(gps):
    easting, northing, _, _ = utm.from_latlon(gps["latitude"], gps["longitude"])
    return {"x": easting, "y": northing, "th": None}


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


def normalize_th(angle):
    return (angle + math.pi) % (2 * math.pi) - math.pi


def heading_error_to_motors(heading_error):
    left_speed = 0.5 - 0.25 / (math.pi / 2) * heading_error
    right_speed = 0.5 + 0.25 / (math.pi / 2) * heading_error

    return left_speed, right_speed


GOALS = [
    (37.571263696196944, -122.30068686975393),
    (37.571259444382996, -122.30079147589892),
    (37.5714847901911, -122.30074587833418),
]


@click.command()
@click.option("--goal-num", default=1, help="Which goal to go to")
def main(goal_num):

    # Set goal position
    goal = GOALS[goal_num - 1]
    goal_pose = gps_to_xy({"latitude": goal[0], "longitude": goal[1]})

    # Subscribe to pose and drive towards it
    pose_subscriber = get_subscriber_pose()
    while True:
        print("------")

        # Get current pose
        current_pose = pose_subscriber.receive_json()

        # Move till pose is initialized
        if current_pose["th"] is None:
            print("Waiting for pose...")
            set_motor_speeds(0.25, 0.25)
            continue

        # Check if we have reached the goal
        dist_to_goal = distace_between_poses(current_pose, goal_pose)
        print(f"Dist to goal: {dist_to_goal}")

        if dist_to_goal < 0.5:
            print("Goal reached")
            stop_motors()
            continue

        # Make progress towards goal
        heading_to_goal = heading_between_poses(current_pose, goal_pose)
        current_cartesian_heading = normalize_th(-1 * current_pose["th"] + math.pi / 2)

        print(f"Goal heading: {math.degrees(heading_to_goal)}")
        print("Current heading: ", math.degrees(current_pose["th"]))
        print("Current cartesian heading: ", math.degrees(current_cartesian_heading))

        heading_error = heading_to_goal - current_cartesian_heading
        heading_error = normalize_th(heading_error)
        print(f"Heading error: {math.degrees(heading_error)}")

        left_speed, right_speed = heading_error_to_motors(heading_error)
        print(f"Left speed: {left_speed}, right speed: {right_speed}")
        set_motor_speeds(left_speed, right_speed)


if __name__ == "__main__":
    main()
