import argparse
import logging
import os
import textwrap

from .visualize import animate_transitions, plot_transitions

LOGLEVEL = os.environ.get("LOGLEVEL", "INFO").upper()
logging.basicConfig(level=LOGLEVEL)
LOGGER = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Plot or step through events",
        usage='use "%(prog)s --help" for more information',
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "process",
        help=textwrap.dedent(
            """\
            Name of the top-level process as described in `<process>.hac`.
            If the `<process>.hac` is not in the current working directory,
            use `</path/to/process>` HAC file without the `.hac` extension.
            For example, use `python -m ACT /foo/bar` if the process is defined in `/foo/bar.hac`.
            """
        ),
    )
    parser.add_argument(
        "-p", "--plot", action="store_true", default=False, help="Plot and save the event transitions (default: False)"
    )
    parser.add_argument(
        "-s",
        "--step",
        action="store_true",
        default=True,
        help="Interactively step through even transitions (default: True)",
    )
    parser.add_argument(
        "-w",
        "--window",
        action="store",
        type=float,
        default=None,
        help=textwrap.dedent(
            """\
            Time window to show in interactive mode (i.e., with `-s`).
            If `None`, fit all events into the current window.
            (default: None)
            """
        ),
    )
    args = parser.parse_args()

    if args.plot:
        LOGGER.info(f"Plotting transitions for process: {args.process}")
        plot_transitions(args.process)
    elif args.step:
        LOGGER.info(f"Interactively step through event transitions for process: {args.process}")
        animate_transitions(args.process, args.window)
