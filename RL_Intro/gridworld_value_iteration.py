import numpy as np

ACTIONS = ('U', 'D', 'L', 'R')
DELTA_THRESHOLD = 1e-3
GAMMA = 0.9

# 격자 공간의 클래스를 정의
class Grid: 
	def __init__(self, rows, cols, start):
		self.rows = rows
		self.cols = cols
		self.i = start[0]
		self.j = start[1]

	# 각 상태의 보상과 선택 가능한 행동을 설정
	def set(self, rewards, actions):
		self.rewards = rewards
		self.actions = actions

	def set_state(self, s):
		self.i = s[0]
		self.j = s[1]

	def current_state(self):
		return (self.i, self.j)

	def is_terminal(self, s):
		return s not in self.actions

	def move(self, action):
		if action in self.actions[(self.i, self.j)]:
			if action == 'U':
				self.i -= 1
			elif action == 'D':
				self.i += 1
			elif action == 'R':
				self.j += 1
			elif action == 'L':
				self.j -= 1
	    # 보상이 있을 경우 보상을 반환
		return self.rewards.get((self.i, self.j), 0)

	# 모든 상태를 반환
	def all_states(self):
		# possibly buggy but simple way to get all states
		# either a position that has possible next actions
		# or a position that yields a reward
		return set(self.actions.keys()) | set(self.rewards.keys())

# 격자 공간과 각 상태에서 선택 가능한 행동을 정의
def standard_grid():
	grid = Grid(3, 4, (2, 0))
	rewards = {(0, 3): 1, (1, 3): -1}
	actions = {
		(0, 0): ('D', 'R'),
		(0, 1): ('L', 'R'),
		(0, 2): ('L', 'D', 'R'),
		(1, 0): ('U', 'D'),
		(1, 2): ('U', 'D', 'R'),
		(2, 0): ('U', 'R'),
		(2, 1): ('L', 'R'),
		(2, 2): ('L', 'R', 'U'),
		(2, 3): ('L', 'U'),
	}
	grid.set(rewards, actions)
	return grid

def print_values(V, grid):
	for i in range(grid.rows):
		print("---------------------------")
		for j in range(grid.cols):
			value = V.get((i, j), 0)
			if value >= 0:
				print("%.2f | " % value, end = "")
			else:
				print("%.2f | " % value, end = "") # -ve sign takes up an extra space
		print("")

def print_policy(P, grid):
	for i in range(grid.rows):
		print("---------------------------")
		for j in range(grid.cols):
			action = P.get((i, j), ' ')
			print("  %s  |" % action, end = "")
		print("")

if __name__ == '__main__':
    # 격자 공간을 초기화
	grid = standard_grid()

	# 보상을 출력
	print("\n보상: ")
	print_values(grid.rewards, grid)

	# 초기 정책은 각 상태에서 선택 가능한 행동을 무작위로 선택
	policy = {}
	for s in grid.actions.keys():
		policy[s] = np.random.choice(ACTIONS)

	# 정책 초기화
	print("\n초기 정책:")
	print_policy(policy, grid)

	# 가치 함수 V(s) 초기화
	V = {}
	states = grid.all_states()
	for s in states:
		# V[s] = 0
		if s in grid.actions:
			V[s] = np.random.random()
		else:
			# 종단 상태
			V[s] = 0

	# 수렴할 때까지 반복
	i = 0
	while True:
		maxChange = 0
		for s in states:
			oldValue = V[s]

			# 종단 상태가 아닌 상태에 대해서만 V(s)를 계산
			if s in policy:
				newValue = float('-inf')
				for a in ACTIONS:
					grid.set_state(s)
					r = grid.move(a)
					# 벨만 방정식 계산
					v = r + GAMMA * V[grid.current_state()]
					if v > newValue:
						newValue = v
				V[s] = newValue
				maxChange = max(maxChange, np.abs(oldValue - V[s]))

		print("\n%i  번째 반복" % i, end = "\n")
		print_values(V, grid)
		i += 1 

		if maxChange < DELTA_THRESHOLD:
			break

	# 최적 가치 함수를 찾는 정책을 도출
	for s in policy.keys():
		bestAction = None
		bestValue = float('-inf')
		# 가능한 모든 행동에 대해 반복
		for a in ACTIONS:
			grid.set_state(s)
			r = grid.move(a)
			v = r + GAMMA * V[grid.current_state()]
			if v > bestValue:
				bestValue = v
				bestAction = a
		policy[s] = bestAction

	# 계산된 가치 함수와 정책을 출력
	print("\n가치 함수: ")
	print_values(V, grid)

	print("\n정책: ")
	print_policy(policy, grid)