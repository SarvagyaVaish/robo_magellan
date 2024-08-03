import datetime
import json
import os
import threading
import time

from pub_sub import get_subscriber_gps, Subscriber


def logger_thread(
    subscriber_name: str,
    subscriber: Subscriber,
    log_directory: str,
    stop_event: threading.Event,
):
    log_filename = os.path.join(log_directory, f"{subscriber_name}.data")
    subscriber.write_to_log(log_filename, stop_event)


def main():
    # Create a directory with the current timestamp to save all the data in
    directory_name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_directory = os.path.join("logs", directory_name)
    os.makedirs(log_directory, exist_ok=True)

    # List of subscribers to monitor
    subscribers = [
        ("gps", get_subscriber_gps()),
    ]

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
