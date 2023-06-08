"""
Functions for anaylzing generated data:
    * `draw_scaled_prob_dist`.
    * `compute_f_xeb`.
    """

from typing import Iterable, Optional, Tuple

import numpy as np
import matplotlib.pyplot as plt

def compute_f_xeb(p1: Iterable[float], p2: Iterable[float], hilbert_dim: int) -> float:
    """TODO COMPLETE."""

    return (hilbert_dim * p1.dot(p2)) - 1

def draw_scaled_prob_dist(
    probs: Iterable[float],
    hilbert_dim: int,
    num_bins: Optional[int] = 70,
    exp_decay_plot: Optional[bool] = False,
    fig_title: Optional[str] = None,
    fig_size: Optional[Tuple[int, int]] = (12, 5),
    savefig_path: Optional[str] = None
) -> None:
    """TODO COMPLETE."""

    scaled_probs = hilbert_dim * probs
    plt.figure(figsize=fig_size)
    plt.hist(scaled_probs, num_bins, density=True, rwidth=0.9)

    plt.xlabel("Scaled probabilities")
    plt.ylabel("Density")

    if fig_title is not None:
        plt.title(fig_title)

    if exp_decay_plot:
        x = np.linspace(0, max(scaled_probs))
        plt.plot(x, np.e**-x)

    if savefig_path is not None:
        plt.savefig(savefig_path)