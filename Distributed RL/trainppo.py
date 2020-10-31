from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
import ray

ray.init(address="auto")
tune.run(PPOTrainer, config={"env": "CartPole-v0"})
