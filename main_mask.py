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

parser.add_argument("--n", default=10)
parser.add_argument("--k", default=1)
parser.add_argument("--m", default=1)
parser.add_argument("--total_timesteps", default=100000)
parser.add_argument("--state_mode", default="a")
parser.add_argument("--reward_mode", default="r")

args = parser.parse_args()


def gym_env_generator(state_mode, reward_mode, n, m):
    mapper = {
        0: "H"
    }
    for i in range(m):
        mapper[i + 1] = "C" + str(i)
    env = BPEnvMask()
    env.bprogram_generator = init_bprogram
    env.action_space = BPActionSpace(mapper)
    env.action_mapper = mapper
    env.state_mode = state_mode
    env.reward_mode = reward_mode
    dim = 3 + m  # number of bthreads + 1
    if state_mode == "r":
        dim -= 1
    if state_mode == "ar":
        dim += 1
    if reward_mode == "a":
        dim += 1
    env.observation_space = gym.spaces.Box(0, n, shape=(dim,))
    return env

from hot_cold import init_bprogram, params

params["n"] = int(args.n)
params["k"] = int(args.k)
params["m"] = int(args.m)
name = "_".join([str(key) + "_" + str(value) for key, value in vars(args).items()])

log_dir = "output/" + name + "/"
print(log_dir)
env = gym_env_generator(args.state_mode, args.reward_mode, params["n"], params["m"])

env = Monitor(env, log_dir)
os.makedirs(log_dir, exist_ok=True)
model = MaskablePPO("MlpPolicy", env, verbose=0)


model.learn(total_timesteps=int(args.total_timesteps),
            callback=BPCallbackMask())

model.action_space.bprogram = None
model.save(log_dir + "model")