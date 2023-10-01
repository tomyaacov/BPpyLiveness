import gymnasium as gym
from bp_env_ttt import BPEnvTTT
from bp_action_space import BPActionSpace
from tic_tac_toe import bp_gen

def get_env():
    l = ['O' + str(i) + str(j) for i in range(3) for j in range(3)] + ['OWin', 'XWin', 'Draw']
    mapper = {i: l[i] for i in range(len(l))}
    env = BPEnvTTT()
    env.bprogram_generator = bp_gen
    env.action_space = BPActionSpace(mapper)
    env.action_mapper = mapper
    env.state_mode = "a"
    env.reward_mode = "r"
    env.observation_space = gym.spaces.Box(-1, 1, shape=(10,))
    return env

def get_action_space():
    l = ['O' + str(i) + str(j) for i in range(3) for j in range(3)] + ['OWin', 'XWin', 'Draw']
    mapper = {i: l[i] for i in range(len(l))}
    return BPActionSpace(mapper)

def get_bprogram():
    return bp_gen()