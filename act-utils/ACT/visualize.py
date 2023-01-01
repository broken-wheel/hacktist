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


def animate_transitions(process: str):
    """
    :param process: name of the top-level process as described in `{process}.hac`
    """
    res = inspect.parse_state_transition(f"{process}.out.events", f"{process}.out.states", f"{process}.out.map")

    t = res["transitions"]
    s = res["signals"]
    smap = {_s: _idx for _idx, _s in enumerate(s)}

    num_t = len(t)
    num_r = len(s)
    cmap = mpl.cm.get_cmap("viridis", num_r)

    f1, axes = plt.subplots(num_r, 1, sharex=True)

    def animate(event_id):
        events = t.iloc[:event_id]
        e_edge = events.e_t.iloc[-1]
        for sig_name, sig_idx in smap.items():
            s_events = events[events["s_name"] == sig_name]
            s_val = list(s_events.s_val)
            t_edges = [*s_events.e_t, e_edge]
            ax = axes[sig_idx]
            ax.clear()
            plt.sca(ax)
            plt.stairs(
                s_val,
                t_edges,
                color=cmap(sig_idx),
                fill=True,
                alpha=0.6,
                label=sig_name,
            )
            plt.ylabel(r"sig: $\bf{" + sig_name + r"}$")

    min_idx = 3
    config = {"event_id": min_idx}

    def on_keyboard(event):
        if event.key == "right":
            if config["event_id"] < num_t:
                config["event_id"] += 1
            else:
                LOGGER.warning(f"Reached last event ({num_t})")
        elif event.key == "left":
            if config["event_id"] > min_idx:
                config["event_id"] -= 1
            else:
                LOGGER.warning(f"Reached earliest event ({min_idx})")

        LOGGER.info(f"Showing events up to {config['event_id']}")
        animate(config["event_id"])
        plt.draw()

    animate(config["event_id"])
    plt.draw()

    f1.canvas.mpl_connect("key_press_event", on_keyboard)
    plt.show()