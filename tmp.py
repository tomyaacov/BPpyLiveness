from bp_env import BPEnv
from bp_action_space import BPActionSpace
from hot_cold import init_bprogram, params
import gym

def gym_env_generator(state_mode, reward_mode, n, m):
    mapper = {
        0: "H"
    }
    for i in range(m):
        mapper[i+1] = "C" + str(i)
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


if __name__ == '__main__':
    params["n"] = 5
    params["k"] = 2
    params["m"] = 1
    env = gym_env_generator("a", "r", params["n"], params["m"])
    state = env.reset()
    print(state)
    done = False
    while not done:
        action = env.action_space.sample()
        print(action)
        state, reward, done, _ = env.step(action)
        print(state, reward, done)






