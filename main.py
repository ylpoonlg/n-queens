import sys, time
import pygame
from solver import nQueens

class button():
	def __init__(self, win, color, x, y , width, height, text=''):
		self.color = color
		fade = 0.8
		self.color2 = (color[0]*fade, color[1]*fade, color[2]*fade)
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.text = text
		self.win = win

		self.draw(self.color)

	def draw(self, col):
		pygame.draw.rect(self.win, col, (self.x, self.y, self.width, self.height), 0)

		if self.text != '':
			font = pygame.font.SysFont('comicsans', int(self.height*0.8))
			text = font.render(self.text, 1, (0,0,0))
			self.win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

		pygame.display.update()

	def isOver(self, pos):
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True

		self.draw(self.color)
		return False

class ui():
	def __init__(self, **kwargs):
		self.BACKGROUND_COLOR = (50, 50, 50)
		self.GRID_COLOR = (255, 255, 230)

		self.sol = []
		self.soli = 0
		self.numsol = 0
		self.n = 1

		self.screen_init(600, 800)
		self.getDimensions()

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
						self.n = int(input())
						self.onStart(self.n)

				#----------button click-----------
				pos = pygame.mouse.get_pos()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if self.sol_next.isOver(pos):
						if self.soli+1 < self.numsol:
							self.soli+=1
							self.showSolution(self.soli)
					if self.sol_prev.isOver(pos):
						if self.soli-1 >= 0:
							self.soli-=1
							self.showSolution(self.soli)

					if self.n_inc.isOver(pos):
						self.n = min(self.n+1, 10)
						self.screen_init(self.width, self.height)
					if self.n_dec.isOver(pos):
						self.n = max(self.n-1, 1)
						self.screen_init(self.width, self.height)

					if self.go_but.isOver(pos):
						print(f'Starting... N = {self.n}')
						self.onStart(self.n)

				#----------button hover------------
				if event.type == pygame.MOUSEMOTION:
					if self.sol_next.isOver(pos) or self.soli >= self.numsol-1:
						self.sol_next.draw(self.sol_next.color2)
					if self.sol_prev.isOver(pos) or self.soli == 0:
						self.sol_prev.draw(self.sol_prev.color2)

					if self.n_inc.isOver(pos) or self.n == 10:
						self.n_inc.draw(self.n_inc.color2)
					if self.n_dec.isOver(pos) or self.n == 1:
						self.n_dec.draw(self.n_dec.color2)

					if self.go_but.isOver(pos):
						self.go_but.draw(self.go_but.color2)

			pygame.display.update()

	def screen_init(self, w, h):
		pygame.init()
		pygame.display.set_caption('N Queens')
		self.screen = pygame.display.set_mode((w, h), pygame.RESIZABLE)
		self.screen.fill(self.BACKGROUND_COLOR)

		# Line 1
		self.blit_text("N Queens Simulator", (255,255,255), 50, 0, 10, 0, w)

		# Line 2
		line2y = 70
		# column 1
		line2c1 = 0
		self.n_dec = button(self.screen, (255,255,255), line2c1, line2y, 50, 50)
		self.n_inc = button(self.screen, (255,255,255), line2c1+55, line2y, 50, 50)
		self.blit_text(f"N = {self.n}", (255,255,255), 50, line2c1+130, line2y+5)

		# column 2
		line2c2 = w - 300
		self.sol_prev = button(self.screen, (255,255,255), line2c2, line2y, 50, 50)
		self.sol_next = button(self.screen, (255,255,255), line2c2+55, line2y, 50, 50)
		self.blit_text(f"{min(self.soli+1, self.numsol)}/{self.numsol}", (255,255,255), 50, line2c2+130, line2y+5)

		self.go_but = button(self.screen, (0, 255, 0), 0, line2y+55, 100, 50, "GO!")

		pygame.display.update()

	def onStart(self, n):
		self.draw_grid([0] * (15), n, n)
		solver = nQueens(n, self)
		solver.solve()
		print('Finished solving...')
		self.sol = solver.solutions
		self.numsol = len(solver.solutions)
		print('sol is ', self.sol)
		if self.numsol > 0:
			self.showSolution(0)

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

	def blit_text(self, msg, color, size, x, y, align=-1, w=0):
		font = pygame.font.SysFont('comicsans', size)
		text = font.render(msg, 1, color)
		if align == 0:
			self.screen.blit(text, (x+(w-text.get_width())/2, y))
		else:
			self.screen.blit(text, (x, y))
		#pygame.display.update()

	def showSolution(self, i):
		self.screen_init(self.width, self.height)
		board = self.sol[i]
		self.draw_grid(board, self.n, self.n)

if __name__ == '__main__':
	display = ui()