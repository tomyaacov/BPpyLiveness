import gym
from stable_baselines3 import PPO
env = gym.make('MountainCar-v0')




model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=100000, log_interval=4)


observation = env.reset()
env.render()
for _ in range(1000):
   action, _states = model.predict(observation, deterministic=True)
   #action = env.action_space.sample()
   print(action)
   observation, reward, terminated, done = env.step(action)
   print(observation, reward)
   env.render()
   if done:
      observation = env.reset()
env.close()