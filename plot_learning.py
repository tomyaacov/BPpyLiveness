from stable_baselines3.common import results_plotter
from stable_baselines3.common.monitor import load_results
import numpy as np
from matplotlib import pyplot as plt
folder = "output/n_10_k_3_m_1_total_timesteps_2000000_state_mode_a_reward_mode_a"

title = "k_3_m_1"
EPISODES_WINDOW = 100
data_frame = load_results(folder)
xy_list = [results_plotter.ts2xy(data_frame, results_plotter.X_TIMESTEPS)]
plt.figure(title, figsize=(8, 2))
max_x = max(xy[0][-1] for xy in xy_list)
min_x = 0
for _, (x, y) in enumerate(xy_list):
    plt.scatter(x, y, s=2)
    # Do not plot the smoothed curve at all if the timeseries is shorter than window size.
    if x.shape[0] >= EPISODES_WINDOW:
        # Compute and plot rolling mean with window of size EPISODE_WINDOW
        x, y_mean = results_plotter.window_func(x, y, EPISODES_WINDOW, np.mean)
        plt.plot(x, y_mean, color="orange")
plt.xlim(min_x, max_x)
plt.title(title)
plt.xlabel(results_plotter.X_TIMESTEPS)
plt.ylabel("Episode Rewards")
plt.tight_layout()
plt.show()