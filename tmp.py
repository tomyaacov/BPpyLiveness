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

parser.add_argument("--total_timesteps", default=100000)
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
    env.observation_space = gym.spaces.Box(-1, 1, shape=(9,))
    return env

from tic_tac_toe import bp_gen

for i in range(200):
    env = gym_env_generator(args.state_mode, args.reward_mode)
    s, _ = env.reset()
    print(s)
    done = False
    while not done:
        a = env.action_space.sample()
        s, r, done, _, _ = env.step(a)
        print(env.action_space.action_mapper[a], s, r, done)
