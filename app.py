import pyxel
from utils import *


class App:
    def __init__(self):
        self.width = 120
        self.height = 160
        self.tetrimino = self.create_new_tetrimino()
        self.game_over = False
        self.game_field = [[False for _ in range(0, self.width, 10)] for _ in range(0, self.height, 10)]

        pyxel.init(self.width, self.height)
        pyxel.run(self.update, self.draw)

    def create_new_tetrimino(self):
        shape = random.choice(list(TETROMINOES.values()))
        return Tetrimino(shape, width = 100)

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
    #pyxel.rect(0,0,10,10,1)
        self.draw_tetrimino(self.tetrimino)

    def draw_tetrimino(self, tetrimino):
        for y, row in enumerate(tetrimino.shape):
            # print(tetrimino.shape)
            for x, cell in enumerate(row):
                if cell:
                    print("cell:", cell)
                    pyxel.rect((tetrimino.x + x *10 ), (tetrimino.y + y * 10), 10, 10, 1)


    def check_collision(self, tetrimino, direction):
        _collided = False
        future_x = tetrimino.x //10
        future_y = tetrimino.y //10

        if direction == "down":
            future_y += 1
        elif direction == "left":
            future_x -= 1
        elif direction == "right":
            future_x += 1

        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                # if cell in [0, 1]:
                new_x = future_x + x
                new_y = future_y + y
                print(new_x, new_y, len(self.game_field[0]), len(self.game_field))
                if new_x < 0 or new_x >= self.width//10 or new_y >= self.height//10 or self.game_field[new_y][new_x]:
                    print(tetrimino, x, y)
                    _collided = True
                    return True
                else:
                    print("ok!")
        
        return False
    
    def move_tetrimino(self, tetrimino, direction):
        if direction == "left":
            tetrimino.x -= 10  # X座標を減らして左に移動
        elif direction == "right":
            tetrimino.x += 10  # X座標を増やして右に移動
        elif direction == "down":
            tetrimino.y += 10  # Y座標を増やして下に移動

    def update(self):
        if self.game_over:
            #return
            pass
        if pyxel.btnp(pyxel.KEY_DOWN):
            if not self.check_collision(self.tetrimino, "down"):
                self.move_tetrimino(self.tetrimino, "down")

        # テトリミノを左に移動
        if pyxel.btnp(pyxel.KEY_LEFT):
            if not self.check_collision(self.tetrimino, "left"):
                self.move_tetrimino(self.tetrimino, "left")
        # テトリミノを右に移動
        if pyxel.btnp(pyxel.KEY_RIGHT):
            if not self.check_collision(self.tetrimino, "right"):
                self.move_tetrimino(self.tetrimino, "right")



if __name__ == "__main__":
    App()
