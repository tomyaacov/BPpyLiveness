import gymnasium as gym
import os
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.dqn import MlpPolicy
from stable_baselines3.common.monitor import Monitor
from sb3_contrib import MaskablePPO
from bp_env_ttt import BPEnvTTT
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
    l = ['O' + str(i) + str(j) for i in range(3) for j in range(3)] + ['OWin', 'XWin', 'Draw']
    mapper = {i: l[i] for i in range(len(l))}
    env = BPEnvTTT()
    env.bprogram_generator = bp_gen
    env.action_space = BPActionSpace(mapper)
    env.action_mapper = mapper
    env.state_mode = state_mode
    env.reward_mode = reward_mode
    env.observation_space = gym.spaces.Box(-1, 1, shape=(9,))
    return env

from tic_tac_toe import bp_gen
log_dir = "output/ttt_total_timesteps_10000000_state_mode_a_reward_mode_r/"
model = MaskablePPO.load(log_dir + "model")

for i in range(1000):
    env = gym_env_generator(args.state_mode, args.reward_mode)
    observation, _ = env.reset()
    print(observation)
    reward_sum = 0
    counter = 0
    values = []
    actions = []
    while True:
        action_masks = env.action_masks()
        action, _states = model.predict(observation, deterministic=True, action_masks=action_masks)
        action = action.item()
        # action = env.action_space.sample()
        actions.append(action)
        observation, reward, done, _, info = env.step(action)
        print(env.action_space.action_mapper[action], observation, reward, done, info)
        reward_sum += reward
        counter += 1
        # print(action, observation, reward, done, info)
        if done:
            break
    # print("optimal reward: ", reward_sum)
