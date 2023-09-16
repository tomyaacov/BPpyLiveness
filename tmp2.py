import gymnasium as gym
import os
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.dqn import MlpPolicy
from sb3_contrib import MaskablePPO
from stable_baselines3.common.monitor import Monitor
from bp_env_mask import BPEnvMask
from bp_callback import BPCallback
from bp_action_space import BPActionSpace
import numpy as np
import argparse

from hot_cold import init_bprogram, params



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

name = "n_100_k_4_m_3_total_timesteps_10000000_state_mode_a_reward_mode_r"
params["n"] = 100
params["k"] = 4
params["m"] = 3
log_dir = "output/" + name + "/"
env = gym_env_generator("a", "r", params["n"], params["m"])
#env = Monitor(env, log_dir)
os.makedirs(log_dir, exist_ok=True)
model = MaskablePPO("MlpPolicy", env, verbose=0)
model = MaskablePPO.load(log_dir + "model")

observation, _ = env.reset()
reward_sum = 0
counter = 0
values = []
actions = []
while True:
    # env.render()
    action_masks = env.action_masks()
    action, _states = model.predict(observation, deterministic=True, action_masks=action_masks)
    actions.append(action)
    observation, reward, done, _, info = env.step(action.item())
    reward_sum += reward
    counter += 1
    # print(action, observation, reward, done, info)
    if done:
        break
print(sum([x.item() for x in actions]))
print(len([x.item() for x in actions]))
print("optimal actions: ", [env.action_mapper[x.item()] for x in actions])
print("optimal reward: ", reward_sum)
