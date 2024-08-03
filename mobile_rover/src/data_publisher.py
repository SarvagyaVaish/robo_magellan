import os

import click

from pub_sub import get_publisher_gps


@click.command()
@click.option("-d", "--log-directory", required=True, help="Path to directory to load log files from")
def main(log_directory):
    subscriber_name = "gps"
    log_filename = os.path.join(log_directory, f"{subscriber_name}.data")

    gps_publisher = get_publisher_gps()
    gps_publisher.read_from_logs(filename=log_filename, rate=5)


if __name__ == "__main__":
    main()
