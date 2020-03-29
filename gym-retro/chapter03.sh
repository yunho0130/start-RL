# 소스코드 저장소 클론하기 
git clone https://github.com/yunho0130/start-RL
# OpenAI Gym Retro 환경설정 파일이 있는 경로로 이동합니다. 
cd gym-retro
# 해당 경로에서 파이썬 개발 환경 설정 정보가 들어있는 environment.yml 파일을 참조하여 새로운 콘다 환경을 생성합니다. 
conda env create -f environment.yml
# 생성한 콘다 환경을 활성화 합니다.
source activate rl-gym-retro
# Airstriker 실행해보기
python -m retro.examples.interactive --game Airstriker-Genesis
# Random Agent를 통해 Airstriker 실행해보기
python -m random_agent
# Random Agent의 플레이 데이터 출력
python -m retro.examples.random_agent --game Airstriker-Genesis
