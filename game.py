import pyxel
from utils import *


class App:
	def __init__(self):
		self.width = 160
		self.height = 120
		self.tetrimino = self.create_new_tetrimino()
		self.game_over = False

		pyxel.init(self.width, self.height)
		pyxel.run(self.update, self.draw)

	def create_new_tetrimino(self):
		shape = random.choice(list(TETROMINOES.values()))
		return Tetrimino(shape, width = 90)

	def update(self):
		if self.game_over:
			return

		if pyxel.btnp(pyxel.KEY_DOWN):
			pass
			#if not check_collision(self.tetrimino, "down"):
			#	move_tetrimino(self.tetrimino, "down")

		# キー入力による左右、回転の操作をここに追加

	def draw(self):
		pyxel.cls(7)
		pyxel.rect(0,0,10,10,1)
		self.draw_tetrimino(self.tetrimino)
		
	def draw_tetrimino(self, tetrimino):
		for y, row in enumerate(tetrimino.shape):
			# print(tetrimino.shape)
			for x, cell in enumerate(row):
				if cell:
					print("cell:", cell)
					pyxel.rect((tetrimino.x + x *10 ), (tetrimino.y + y * 10), 10, 10, 1)

if __name__ == "__main__":
    App()
