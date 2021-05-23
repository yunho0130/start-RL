## 윈도우 원격 데스크톱 접속 환경 구성하기
MS Azure에서 생성한 인스턴스에 원격 데스크톱(Remote Desktop)으로 접근하기 위한 구성입니다.

원격 접속을 위한 doitrl 계정에 대한 비밀번호 설정도 포함되어 있습니다.

```
sudo apt-get update
sudo apt-get -y install xfce4
sudo apt-get -y install xrdp
sudo systemctl enable xrdp
echo xfce4-session >~/.xsession
sudo service xrdp restart
sudo passwd doitrl
sudo apt-get -y install firefox
```

## Ray 아키텍쳐 및 RLlib 설치 하기

단계별로 명령어 입니다.

#### **01 단계** 라이브러리 설치하기
아나콘다, Ray 아키텍처, RLlib 설치와 사용을 위해 필요한 라이브러리를 설치한 다음 아
나콘다를 설치합니다.
```
sudo apt-get -y install build-essential checkinstall gcc python3-dev libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev cmake
wget https://repo.anaconda.com/archive/Anaconda3-2020.07-Linux-x86_64.sh
sh Anaconda3-2020.07-Linux-x86_64.sh
```

#### **02 단계** 가상 환경 설정하고 Ray 아키텍처 설치하기
아나콘다를 설치했다면 Ray 아키텍처 설치를 위한 가상 환경을 설정합니다.
```
source .bashrc
conda create --name ray -y
conda activate ray
```

Ray 아키텍처는 pip로 설치합니다. pip, pytest를 설치하고 나서 Ray 아키텍처를 설치
합니다. 모두 설치했으면 pip list 명령어로 Ray 아키텍처 설치를 확인해 보세요.

```
conda install --name ray pip -y
pip install pytest
pip install ray
pip list
```

#### **03 단계** Ray 아키텍처 설치 확인하기
지금까지 설치한 내용을 확인해 봅니다. 
```
git clone https://github.com/ray-project/ray.git
cd ray
python -m pytest -v python/ray/tests/test_mini.py
```

#### **04 단계** RLlib 설치하기
```
conda install --name ray tensorflow -y
pip install 'ray[rllib]'
```

#### **05 단계** 카트폴 문제 풀어 보기
```
rllib train --run=PPO --env=CartPole-v0
```

## 분산환경에서 카트폴 실행 하기
'trainppo_1.py'파일을 Azure 인스턴스에 복사 한 후 이름을 'trainppo.py'로 변경 하여 수행합니다. 또는 아래 소스 코드를 복사해서 사용합니다.
```python
# 파일이름을 trainppo.py로 변경 후 실행하세요.
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
import ray

ray.init(address="auto")
tune.run(PPOTrainer, config={"env": "CartPole-v0"})
```

실행 명령어
```
python trainppo.py
```

#### Worker 1개 증가 하기
'trainppo_2.py'파일을 Azure 인스턴스에 복사 한 후 이름을 'trainppo.py'로 변경 하여 수행합니다. 또는 아래 소스 코드를 복사해서 사용합니다.
***num_workers*** 옵션을 추가 하여 worker 개수를 조정할 수 있습니다.
```python
# 파일이름을 trainppo.py로 변경 후 실행하세요.
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
import ray

ray.init(address="auto")
tune.run(PPOTrainer, config={"env": "CartPole-v0", "num_workers":3})
```

#### 학습 중단 조건 추가
'trainppo_3.py'파일을 Azure 인스턴스에 복사 한 후 이름을 'trainppo.py'로 변경 하여 수행합니다. 또는 아래 소스 코드를 복사해서 사용합니다.
***stop*** 옵션을 추가 하여 worker 개수를 조정할 수 있습니다.
```python
# 파일이름을 trainppo.py로 변경 후 실행하세요.
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer
import ray

ray.init(address="auto")
tune.run(PPOTrainer, stop={"episode_reward_mean": 200}, config={"env": "CartPole-v0", "num_workers":3, “monitor”: False})
```
