import gym
import os
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.dqn import MlpPolicy
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from bp_env import BPEnv
from bp_action_space import BPActionSpace
import numpy as np
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--n", default=3)
parser.add_argument("--k", default=1)
parser.add_argument("--m", default=1)
parser.add_argument("--total_timesteps", default=10000)
parser.add_argument("--state_mode", default="a")
parser.add_argument("--reward_mode", default="r")

args = parser.parse_args()


def gym_env_generator(state_mode, reward_mode, n, m):
    mapper = {
        0: "H"
    }
    for i in range(m):
        mapper[i + 1] = "C" + str(i)
    env = BPEnv()
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


def q_compatible_run(env, model, threshold):
    observation = env.reset()
    reward_sum = 0
    counter = 0
    values = []
    actions = []
    used_optimal = 0
    while True:
        # env.render()
        q_values = model.policy.q_net.forward(model.policy.obs_to_tensor(observation)[0])
        q_values = q_values.detach().cpu().numpy()[0]
        values.append(q_values)
        possible_actions = np.where(q_values + reward_sum > threshold)[0]
        if len(possible_actions) == 0:
            action, _states = model.predict(observation)
            action = action.item()
            used_optimal = 1
        else:
            action = np.random.choice(possible_actions)
        actions.append(action)
        observation, reward, done, info = env.step(action)
        reward_sum += reward
        counter += 1
        # print(action, observation, reward, done, info)
        if done:
            break
    if len(values) <= 1:  # reward_sum < 0 or len(values) <= 1:
        print("bad episode")
        print(values)
        print([env.action_space.action_mapper[a] for a in actions])
        print(reward_sum)
    return (1, used_optimal) if reward_sum == 0 else (0, used_optimal)


def evaluate_model(model, state_mode, reward_mode, n, m):
    results = {}
    env = gym_env_generator(state_mode, reward_mode, n, m)
    total_rewards = 0

    observation = env.reset()
    reward_sum = 0
    counter = 0
    values = []
    actions = []
    while True:
        # env.render()
        action, _states = model.predict(observation)
        actions.append(action)
        observation, reward, done, info = env.step(action.item())
        reward_sum += reward
        counter += 1
        # print(action, observation, reward, done, info)
        if done:
            break
    # print("optimal reward: ", reward_sum)
    results["optimal"] = (reward_sum, 1)
    num_success = 0
    num_used_optimal = 0
    for threshold in np.arange(-1.2, -0.1, 0.1):
        for i in range(100):
            success, used_optimal = q_compatible_run(env, model, threshold)
            num_success += success
            num_used_optimal += used_optimal
        print("q compatible success rate for threshold", threshold, ":", num_success / 100)
        results[threshold] = (num_success / 100, num_used_optimal / 100)
        num_success = 0
        num_used_optimal = 0
    return results


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
model = DQN("MlpPolicy", env, verbose=0)
model.learn(total_timesteps=args.total_timesteps)
model.exploration_rate = 0
model.action_space.bprogram = None
model.save(log_dir + "model")
del model  # remove to demonstrate saving and loading
model = DQN.load(log_dir + "model")
results = evaluate_model(model, args.state_mode, args.reward_mode, params["n"], params["m"])
env.close()

print("Q compatible runs success rate")
for k2, v2 in results.items():
    print(v2[0], end=",")
print()

print("Q compatible runs used optimal rate")
for k2, v2 in results.items():
    print(v2[1], end=",")
print()
