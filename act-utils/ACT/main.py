import argparse
import logging
import os

from .visualize import plot_transitions

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("process", help="Name of the top-level process as described in `<process>.hac`")
    parser.add_argument("--plot", action="store_true", default=True)
    args = parser.parse_args()

    if args.plot:
        LOGGER.info(f"Plotting transitions for process: {args.process}")
        plot_transitions(args.process)
