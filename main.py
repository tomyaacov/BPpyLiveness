import gym
import os
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.dqn import MlpPolicy
from stable_baselines3 import DQN
from stable_baselines3.common.monitor import Monitor
from bp_env import BPEnv
from bp_action_space import BPActionSpace
import numpy as np

def gym_env_generator(state_mode, reward_mode, n):
    mapper = {
        0: "H",
        1: "C"
    }
    env = BPEnv()
    env.bprogram_generator = init_bprogram
    env.action_space = BPActionSpace(mapper)
    env.action_mapper = mapper
    env.state_mode = state_mode
    env.reward_mode = reward_mode
    dim = 4
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
    if len(values) <= 1:#reward_sum < 0 or len(values) <= 1:
        print("bad episode")
        print(values)
        print([env.action_space.action_mapper[a] for a in actions])
        print(reward_sum)
    return (1, used_optimal) if reward_sum == 0 else (0, used_optimal)


def evaluate_model(model, state_mode, reward_mode, n):
    results = {}
    env = gym_env_generator(state_mode, reward_mode, n)
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
    #print("optimal reward: ", reward_sum)
    results["optimal"] = (reward_sum, 1)
    num_success = 0
    num_used_optimal = 0
    for threshold in np.arange(-1.2, -0.1, 0.1):
        for i in range(100):
            success, used_optimal = q_compatible_run(env, model, threshold)
            num_success += success
            num_used_optimal += used_optimal
        print("q compatible success rate for threshold", threshold, ":", num_success/100)
        results[threshold] = (num_success/100, num_used_optimal/100)
        num_success = 0
        num_used_optimal = 0
    return results


experiments = [
    {
        "name": "a-r",
        "n": [10, 20], 
        "k": [3, 6],
        "total_timesteps": [2*(10**6), 4*(10**6)],
        "state_mode": "a",
        "reward_mode": "r"
    },
{
        "name": "r-r",
        "n": [10, 20], 
        "k": [3, 6],
        "total_timesteps": [2*(10**6), 4*(10**6)],
        "state_mode": "r",
        "reward_mode": "r"
    },
{
        "name": "ar-r",
        "n": [10, 20], 
        "k": [3, 6],
        "total_timesteps": [2*(10**6), 4*(10**6)],
        "state_mode": "ar",
        "reward_mode": "r"
    },
{
        "name": "a-a",
        "n": [10, 20], 
        "k": [3, 6],
        "total_timesteps": [2*(10**6), 4*(10**6)],
        "state_mode": "a",
        "reward_mode": "a"
    },
{
        "name": "r-a",
        "n": [10, 20], 
        "k": [3, 6],
        "total_timesteps": [2*(10**6), 4*(10**6)],
        "state_mode": "r",
        "reward_mode": "a"
    },
{
        "name": "ar-a",
        "n": [10, 20], 
        "k": [3, 6],
        "total_timesteps": [2*(10**6), 4*(10**6)],
        "state_mode": "ar",
        "reward_mode": "a"
    },
]


from hot_cold import init_bprogram, params

all_results = {}
for e in experiments[:1]:
    print(e)
    all_results[e["name"]] = {}
    # Create log dir
    for i in range(len(e["n"])):
        for j in range(len(e["k"])):
            log_dir = "output/" + e["name"] + "/n_" + str(e["n"][i]) + "_k_" + str(e["k"][i]) + "/"
            os.makedirs(log_dir, exist_ok=True)
            params["n"] = e["n"][i]
            params["k"] = e["k"][i]
            env = gym_env_generator(e["state_mode"], e["reward_mode"], params["n"])
            env = Monitor(env, log_dir)
            model = DQN("MlpPolicy", env, verbose=0)
            model.learn(total_timesteps=e["total_timesteps"][i])
            model.exploration_rate = 0
            model.action_space.bprogram = None
            model.save(log_dir + e["name"])
            del model  # remove to demonstrate saving and loading
            model = DQN.load(log_dir + e["name"])
            print(model.exploration_rate)
            all_results[e["name"]][e["n"][i]] = evaluate_model(model, e["state_mode"], e["reward_mode"], e["n"][i])
            env.close()

print("Q compatible runs success rate")
for k, v in all_results.items():
    print(k)
    for n, a in v.items():
        print(n, end=",")
        for k2, v2 in a.items():
            print(v2[0], end=",")
        print()

print("Q compatible runs used optimal rate")
for k, v in all_results.items():
    print(k)
    for n, a in v.items():
        print(n, end=",")
        for k2, v2 in a.items():
            print(v2[1], end=",")
        print()