import logging

import matplotlib as mpl
from matplotlib import pyplot as plt

from ACT import inspect

LOGGER = logging.getLogger(__name__)


def plot_transitions(process: str):
    """
    :param process: name of the top-level process as described in `{process}.hac`
    """
    res = inspect.parse_state_transition(f"{process}.out.events", f"{process}.out.states", f"{process}.out.map")

    t = res["transitions"]
    s = res["signals"]

    ts = {_s: t.loc[t.loc[:, "s_name"] == _s] for _s in s}

    num_r = len(s)
    cmap = mpl.cm.get_cmap("viridis", num_r)

    f1, axes = plt.subplots(num_r, 1, sharex=True)
    f2 = plt.figure()
    for _idx, (_s, _t) in enumerate(ts.items()):
        # Separate
        plt.figure(f1.number)
        _ax = axes[_idx]
        _edges = list(_t.loc[:, "e_t"])
        _edges.append(_edges[-1] + _edges[-1] - _edges[-2])

        plt.sca(_ax)
        plt.stairs(_t.loc[:, "s_val"], _edges, color=cmap(_idx), fill=True, alpha=0.6, label=_s)
        plt.ylabel(r"sig: $\bf{" + _s + r"}$")

        _ax.set_yticks([0.0, 1.0])
        _ax.grid("on")
        _ax.set_axisbelow(True)

        # Overlaid
        plt.figure(f2.number)
        plt.stairs(_t.loc[:, "s_val"], _edges, color=cmap(_idx), fill=True, alpha=0.6, label=_s)

    plt.figure(f1.number)
    plt.xlabel("Time (ns)")
    plt.tight_layout()
    plt.savefig(f"{process}.separate.png", dpi=300)
    LOGGER.info(f"Saved {process}.separate.png")

    plt.figure(f2.number)
    plt.xlabel("Time (ns)")
    plt.tight_layout()
    plt.legend()
    plt.gca().set_yticks([0.0, 1.0])
    plt.gca().grid("on")
    plt.gca().set_axisbelow(True)
    plt.savefig(f"{process}.overlaid.png", dpi=300)
    LOGGER.info(f"Saved {process}.overlaid.png")
