import os

import click

from pub_sub import get_publisher_gps


@click.command()
@click.option("-d", "--log-directory", required=True, help="Path to directory to load log files from")
@click.option("-r", "--rate", default=10, help="Rate at which to publish data")
def main(log_directory, rate):
    subscriber_name = "gps"
    log_filename = os.path.join(log_directory, f"{subscriber_name}.data")

    gps_publisher = get_publisher_gps()
    gps_publisher.read_from_logs(filename=log_filename, rate=rate)


if __name__ == "__main__":
    main()
