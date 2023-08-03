from bp_env import BPEnv
from bp_action_space import BPActionSpace
from hot_cold import init_bprogram, params

if __name__ == '__main__':
    params["n"] = 3
    mapper = {
        0: "H",
        1: "C"
    }
    env = BPEnv()
    env.bprogram_generator = init_bprogram
    env.action_space = BPActionSpace(mapper)
    env.action_mapper = mapper
    env.state_mode = "a"
    env.reward_mode = "a"
    state = env.reset()
    print(state)
    done = False
    while not done:
        action = env.action_space.sample()
        print(action)
        state, reward, done, _ = env.step(action)
        print(state, reward, done)
