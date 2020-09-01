import time
class nQueens():
	def __init__(self, n, ui, **kwargs):
		self.n = n
		self.c = [0] * (15)
		self.ui = ui
		self.delay = 0.25
		self.solutions = []

	def check(self, row):
		#print('solving...')
		for i in range(1, self.n+1):
			ok = True
			for j in range(1, row):
				if (self.c[j] == i) or abs(self.c[j]-i) == (row-j):
					ok = False
					break

			tmp_c = self.c
			tmp_c[row] = i
			self.ui.draw_grid(tmp_c, self.n, row)
			time.sleep(self.delay)

			if ok:
				self.c[row] = i
				if row < self.n:
					self.check(row+1)
				else:
					tmp = [0]
					for j in range(1, self.n+1):
						tmp.append(self.c[j])
					self.solutions.append(tmp)

	def solve(self):
		if (self.n == 2) or (self.n == 3):
		    print('NIL')
		else:
		    self.check(1)