import datetime
import os
import threading
import time

import click

from pub_sub import get_subscriber_gps, get_subscriber_pose, Subscriber


def logger_thread(
    subscriber_name: str,
    subscriber: Subscriber,
    log_directory: str,
    stop_event: threading.Event,
):
    log_filename = os.path.join(log_directory, f"{subscriber_name}.data")
    subscriber.write_to_log(log_filename, stop_event)


@click.command()
@click.option("--gps", is_flag=True, default=False, help="Record published gps data")
@click.option("--pose", is_flag=True, default=False, help="Record published pose data")
@click.option("-a", "--all_data", is_flag=True, default=True, help="Record published pose data")
def main(gps, pose, all_data):
    if gps or pose:
        all_data = False

    # Create a directory with the current timestamp to save all the data in
    directory_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_directory = os.path.join("logs", directory_name)
    os.makedirs(log_directory, exist_ok=True)

    # List of subscribers to monitor
    subscribers = []
    if gps or all_data:
        subscribers.append(("gps", get_subscriber_gps()))
    if pose or all_data:
        subscribers.append(("pose", get_subscriber_pose()))

    subscriber_threads = []
    stop_event = threading.Event()

    for subscriber_name, subscriber in subscribers:
        thread = threading.Thread(
            target=logger_thread,
            args=(
                subscriber_name,
                subscriber,
                log_directory,
                stop_event,
            ),
        )
        thread.start()
        subscriber_threads.append(thread)

    # Keep the main thread alive
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nShutting down...")
        stop_event.set()

    # Wait for all threads to complete (this will run indefinitely in this case)
    for thread in subscriber_threads:
        thread.join()


if __name__ == "__main__":
    main()
