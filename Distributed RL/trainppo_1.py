# 파일이름을 trainppo.py로 변경 후 실행하세요.
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
import ray

ray.init(address="auto")
tune.run(PPOTrainer, config={"env": "CartPole-v0"})
