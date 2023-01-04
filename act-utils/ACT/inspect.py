"""
This module will parse and load in the output of hacdump.sh tool
"""
import numpy as np
import pandas as pd


def __gen_tran__(log_file):
    """
    Read in a .out.events file, return event-transition table
    """

    tran_dt = np.dtype([("e_idx", np.uint), ("e_t", float), ("e_n", np.uint), ("c_idx", np.uint)])
    tran_list = np.loadtxt(log_file, dtype=tran_dt, skiprows=0)
    return tran_list


def __gen_states__(log_file):
    """
    Read in a .out.states file, return state-transition table
    """

    state_dt = np.dtype([("e_idx", np.uint), ("s_idx", np.uint), ("s_val", np.uint)])
    state_list = np.loadtxt(log_file, dtype=state_dt, skiprows=0)
    return state_list


def __gen_signal_map__(map_file):
    signal_map = pd.read_csv(
        map_file, sep="\s+", header=None, names=["s_idx", "s_name"], dtype={"s_idx": np.uint, "s_name": str}
    )
    return signal_map


def parse_state_transition(event_log_file, state_log_file, signal_map_file):
    """
    Parse event logs, state logs and signal maps.
    """

    tran_list = pd.DataFrame(__gen_tran__(event_log_file))
    state_list = pd.DataFrame(__gen_states__(state_log_file))
    signal_map = __gen_signal_map__(signal_map_file)

    df1 = state_list.join(tran_list.set_index("e_idx"), on="e_idx")
    df2 = df1.join(signal_map.set_index("s_idx"), on="s_idx")
    df3 = df2[["e_t", "s_name", "s_val"]]

    return {"transitions": df3, "signals": list(signal_map["s_name"])}
