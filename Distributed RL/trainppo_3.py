# 파일이름을 trainppo.py로 변경 후 실행하세요.
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
import ray

ray.init(address="auto")
tune.run(PPOTrainer, stop={"episode_reward_mean": 200}, config={"env": "CartPole-v0", "num_workers":3, “monitor”: False})
