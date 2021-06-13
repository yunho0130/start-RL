import numpy as np

BOARD_ROWS = 3 
BOARD_COLS = 4 
WIN_STATE = (0, 3) # +1의 보상을 가지는 종단 상태 위치
LOSE_STATE = (1, 3) # -1의 보상을 가지는 종단 상태 위치
BLOCKED_STATE = (1, 1) # 이동할 수 없는 영역
START = (2, 0) # 시작 상태 위치
DETERMINISTIC = False # 상태 전이 함수의 확률을 적용하기 위한 플래그. False일 경우에 적용.

class State:
    def __init__(self, state = START):
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC

    def giveReward(self):
        if self.state == WIN_STATE:
            return 1
        elif self.state == LOSE_STATE:
            return -1
        else:
            return 0

    def isEndFunc(self):
        if (self.state == WIN_STATE) or (self.state == LOSE_STATE):
            self.isEnd = True

    def _chooseActionProb(self, action):
        if action == "U":
            return np.random.choice(["U", "L", "R"], p = [0.8, 0.1, 0.1])
        if action == "D":
            return np.random.choice(["D", "L", "R"], p = [0.8, 0.1, 0.1])
        if action == "L":
            return np.random.choice(["L", "U", "D"], p = [0.8, 0.1, 0.1])
        if action == "R":
            return np.random.choice(["R", "U", "D"], p = [0.8, 0.1, 0.1])
    
    # 격자 공간 내에서의 다음 상태를 반환
    def nxtPosition(self, action):
        if self.determine:
            if action == "U":
                nxtState = (self.state[0] - 1, self.state[1])
            elif action == "D":
                nxtState = (self.state[0] + 1, self.state[1])
            elif action == "L":
                nxtState = (self.state[0], self.state[1] - 1)
            else:
                nxtState = (self.state[0], self.state[1] + 1)
            self.determine = False
        else:
            # 상태 전이 함수를 적용
            action = self._chooseActionProb(action)
            self.determine = True
            nxtState = self.nxtPosition(action)

        # 벽을 뚫거나, 이동할 수 없는 영역으로 상태를 바꿀 수 없음
        if (nxtState[0] >= 0) and (nxtState[0] <= 2):
            if (nxtState[1] >= 0) and (nxtState[1] <= 3):
                if nxtState != BLOCKED_STATE:
                    return nxtState
        return self.state

class Agent:

    def __init__(self):
        self.states = []  # 위치와 행동을 기록 record position and action taken at the position
        self.actions = ["U", "D", "L", "R"]
        self.State = State()
        self.isEnd = self.State.isEnd
        self.lr = 0.2
        self.decay_gamma = 0.9 # 할인율은 0.9로 설정

        # 전체 상태에 대해 Q함수(행동 가치 함수) 값 초기화
        self.Q_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.Q_values[(i, j)] = {}
                for a in self.actions:
                    self.Q_values[(i, j)][a] = 0  # Q value is a dict of dict

    # Q값을 가장 극대화시키는 방향으로 다음 행동을 선택
    def chooseAction(self):
        max_nxt_reward = 0
        action = ""

        for a in self.actions:
            current_position = self.State.state
            nxt_reward = self.Q_values[current_position][a]
            if nxt_reward >= max_nxt_reward:
                action = a
                max_nxt_reward = nxt_reward
            #print("current pos: {}, greedy aciton: {}".format(self.State.state, action))
        return action

    # 행동 후 상태 업데이트
    def takeAction(self, action):
        position = self.State.nxtPosition(action)   
        return State(state = position)

    # 종단 상태 도달 후 에피소드 초기화
    def reset(self):
        self.states = []
        self.State = State()
        self.isEnd = self.State.isEnd

    # 에피소드 개수만큼 반복
    def play(self, episodes = 10):
        i = 0
        while i < episodes:
            # to the end of game back propagate reward
            if self.State.isEnd:
                # back propagate
                reward = self.State.giveReward()
                for a in self.actions:
                    self.Q_values[self.State.state][a] = reward
                #print("Game End Reward", reward)
                for s in reversed(self.states):
                    current_q_value = self.Q_values[s[0]][s[1]]
                    reward = current_q_value + self.lr * (self.decay_gamma * reward - current_q_value)
                    self.Q_values[s[0]][s[1]] = round(reward, 3)
                self.reset()
                i += 1
            else:
                action = self.chooseAction()
                # append trace
                self.states.append([(self.State.state), action])
                #print("current position {} action {}".format(self.State.state, action))
                # by taking the action, it reaches the next state
                self.State = self.takeAction(action)
                # mark is end
                self.State.isEndFunc()
                #print("nxt state", self.State.state)
                #print("---------------------")
                self.isEnd = self.State.isEnd

ag = Agent()

ag.play(1000)
print("latest Q-values ... \n")
print(ag.Q_values)
