import sys, time
import pygame

class ui():
	def __init__(self, **kwargs):
		self.BACKGROUND_COLOR = (50, 50, 50)
		self.GRID_COLOR = (255, 255, 230)

		self.screen_init(600, 800)

		while True:
			for event in pygame.event.get():
				if event.type == pygame.VIDEORESIZE:
					w, h = event.size
					self.screen_init(w, h)
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						pygame.quit()
						sys.exit()
					if event.key == pygame.K_SPACE:
						#start
						print('Enter N: ', end='')
						n = int(input())
						self.onStart(n)

	def screen_init(self, w, h):
		pygame.display.set_caption('N Queens')
		self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
		self.screen.fill(self.BACKGROUND_COLOR)
		
		pygame.display.update()

	def onStart(self, n):
		self.draw_grid([0] * (15), n, n)
		solver = nQueens(n, self)
		solver.solve()
		print('Finished solving...')

	def getDimensions(self):
		#generate dimensions
		self.left = 0
		self.top = 0
		self.width = pygame.display.get_surface().get_width()
		self.height = pygame.display.get_surface().get_height()
		self.gridsz = min(self.width, self.height * 0.8)
		if (self.width < self.height*0.8):
			self.left = 0
			self.top = self.height - self.gridsz
		else:
			self.left = (self.width - self.gridsz) // 2
			self.top = self.height - self.gridsz

	def draw_grid(self, board, n, r):
		self.getDimensions()

		#clear old grid
		pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (self.left, self.top, self.gridsz, self.gridsz))

		#draw n*n grid
		for i in range(n):
			for j in range(n):
				w = h = self.gridsz // n
				x = self.left + i*w
				y = self.top + j*w

				b = w*0.05	#border
				pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, (x, y, w, h))
				pygame.draw.rect(self.screen, self.GRID_COLOR, (x+b, y+b, w-b*2, h-b*2))

				if board[j+1] == i+1 and j+1 <= r:
					q = w*0.4
					pygame.draw.rect(self.screen, (150, 100, 20), (x+(w-q)//2, y+(w-q)//2, q, q))

		pygame.display.update()

class nQueens():
	def __init__(self, n, ui, **kwargs):
		self.n = n
		self.c = [0] * (15)
		self.ui = ui
		self.delay = 0.25
		self.solutions = []

	def check(self, row):
		print('solving...')
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
					tmp = []
					for j in range(1, self.n+1):
						tmp.append(self.c[j])
					self.solutions.append(tmp)

	def solve(self):
		if (self.n == 2) or (self.n == 3):
		    print('NIL')
		else:
		    self.check(1)


if __name__ == '__main__':
	display = ui()