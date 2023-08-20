from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import load_results
import numpy as np
from matplotlib import pyplot as plt
folder = "output/a-r/n_10_k_1_m_2/"
data_frame = load_results(folder)
xy_list = results_plotter.ts2xy(data_frame, "timesteps")
results = results_plotter.window_func(xy_list[0], xy_list[1], window=100, func=np.mean)
results_plotter.plot_results(["output/a-r/n_10_k_1_m_2/"], None, results_plotter.X_TIMESTEPS, "a-r")

plt.figure(title, figsize=figsize)
max_x = max(xy[0][-1] for xy in xy_list)
min_x = 0
    for _, (x, y) in enumerate(xy_list):
        plt.scatter(x, y, s=2)
        # Do not plot the smoothed curve at all if the timeseries is shorter than window size.
        if x.shape[0] >= EPISODES_WINDOW:
            # Compute and plot rolling mean with window of size EPISODE_WINDOW
            x, y_mean = window_func(x, y, EPISODES_WINDOW, np.mean)
            plt.plot(x, y_mean)
    plt.xlim(min_x, max_x)
    plt.title(title)
