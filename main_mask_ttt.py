import gymnasium as gym
import os
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.dqn import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from sb3_contrib import MaskablePPO
from bp_env_mask import BPEnvMask
from bp_callback_mask import BPCallbackMask
from bp_action_space import BPActionSpace
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--total_timesteps", default=10000000)
parser.add_argument("--state_mode", default="a")
parser.add_argument("--reward_mode", default="r")

args = parser.parse_args()


def gym_env_generator(state_mode, reward_mode):
    l = ['X' + str(i) + str(j) for i in range(3) for j in range(3)] + ['O' + str(i) + str(j) for i in range(3) for j in range(3)] + ['OWin', 'XWin', 'Draw']
    mapper = {i: l[i] for i in range(len(l))}
    env = BPEnvMask()
    env.bprogram_generator = bp_gen
    env.action_space = BPActionSpace(mapper)
    env.action_mapper = mapper
    env.state_mode = state_mode
    env.reward_mode = reward_mode
    env.observation_space = gym.spaces.Box(-1, 1, shape=(10,))
    return env

from tic_tac_toe import bp_gen


name = "ttt_" + "_".join([str(key) + "_" + str(value) for key, value in vars(args).items()])

log_dir = "output/" + name + "/"
print(log_dir)

steps = []

for i in range(10):
    env = gym_env_generator(args.state_mode, args.reward_mode)

    env = Monitor(env, log_dir)
    os.makedirs(log_dir, exist_ok=True)
    model = MaskablePPO("MlpPolicy", env, verbose=0)

    model.learn(total_timesteps=int(args.total_timesteps),
                callback=BPCallbackMask(repeat=1000))
    steps.append(model.num_timesteps)
    print(model.num_timesteps)

    model.action_space.bprogram = None
    model.save(log_dir + "model")

print("steps: ", steps)
print("average steps: ", sum(steps) / len(steps))