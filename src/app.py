import pyxel
import random

TETROMINOES = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1],
          [1, 1]],
    'T': [[0, 1, 0],
          [1, 1, 1]],
    'S': [[0, 1, 1],
          [1, 1, 0]],
    'Z': [[1, 1, 0],
          [0, 1, 1]],
    'J': [[1, 0, 0],
          [1, 1, 1]],
    'L': [[0, 0, 1],
          [1, 1, 1]]
}

class Tetrimino:
    def __init__(self, shape, width):
        self.shape = shape
        self.x = width // 2
        self.y = 0


class App:
    def __init__(self):
        self.width = 120
        self.height = 160
        self.field = [[0] * self.width for _ in range(self.height)]
        self.tetrimino = self.create_new_tetrimino()
        self.game_over = False
        self.game_field = [[0 for _ in range(0, self.width, 10)] for _ in range(0, self.height, 10)]
        self.drop_speed = 45
        self.drop_counter = 0
        self.tetrimino_locked = False
        self.frame_count = 0
        self.frame_delay = 10  # テトリミノが固定されるまでのフレーム数
        self.tetriminos = []  # 画面上のテトリミノを保持するリスト
        

        pyxel.init(self.width, self.height, title = "テトリス")
        pyxel.run(self.update, self.draw)

    def create_new_tetrimino(self):
        letter = str(random.choice(list(TETROMINOES.keys())))
        shape = TETROMINOES[letter]
        color = TETROMINOES_COLORS[letter]
        return Tetrimino(shape, 100, color)


    
    def draw(self):
        pyxel.cls(7)
        #pyxel.rect(0,0,10,10,1)
        for tetrimino in self.tetriminos:
            self.draw_tetrimino(tetrimino)
        self.draw_tetrimino(self.tetrimino)

    def draw_tetrimino(self, tetrimino):
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    screen_x = tetrimino.x + x
                    screen_y = tetrimino.y + y
                    pyxel.rect((tetrimino.x + x *10 ), (tetrimino.y + y * 10), 10, 10, tetrimino.color)


    def check_collision(self, tetrimino, direction):
        self.collided = False
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
                if new_x < 0 or new_x >= self.width//10 or new_y >= self.height//10 or self.game_field[new_y][new_x]:
                    self.collided = True
                    return True
                if self.game_field[new_y][new_x]:  # ほかのテトリミノに衝突
                    return True
                else:
                    pass
        
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
            return
        
        # テトリミノの下矢印キーの落下処理
        self.drop_counter += 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.drop_speed = 15
        else:
            self.drop_speed = 45
        
        # テトリミノの自動落下処理
        self.drop_counter += 1
        if self.drop_counter > self.drop_speed:
            if not self.check_collision(self.tetrimino, "down"):
                self.move_tetrimino(self.tetrimino, "down")
            else:
                # 衝突があった場合、テトリミノを固定して新しいテトリミノを生成
                # この部分はゲームのロジックに応じて実装
                pass
            self.drop_counter = 0

        # テトリミノを左に移動
        if not self.tetrimino_locked:
            if pyxel.btnp(pyxel.KEY_LEFT):
                if not self.check_collision(self.tetrimino, "left"):
                    self.move_tetrimino(self.tetrimino, "left")
            # テトリミノを右に移動
            if pyxel.btnp(pyxel.KEY_RIGHT):
                if not self.check_collision(self.tetrimino, "right"):
                    self.move_tetrimino(self.tetrimino, "right")
        # テトリミノが床に達した時の確認
        if self.check_collision(self.tetrimino,"down"):
            # テトリミノが底に達したので固定する
            self.tetrimino_locked = True
            # 新しいテトリミノの生成などの処理
            #for y, row in enumerate(tetrimino.shape):
            #    for x, cell in enumerate(row):
            #        if cell:
            #            self.field[tetrimino.y + y][tetrimino.x + x] = 1
            self.place_tetrimino(self.tetrimino)
            self.tetrimino = self.create_new_tetrimino()
            self.tetrimino_locked = False
            self.tetriminos.append(self.tetrimino)
    #    """ テトリミノをゲームフィールドに固定する """
    #    def place_tetrimino(self):
    #        for y, row in enumerate(self.tetrimino.shape):
    #            for x, cell in enumerate(row):
    #                if cell:
    #                    field_x = self.tetrimino.x + x
    #                    field_y = self.tetrimino.y + y
    #                    if 0 <= field_x < self.width and 0<= field_y < self.height:
    #                        self.field[field_y][field_x] = 1  # フィールドにテトリミノを追加
    
    def place_tetrimino(self,tetrimino):
        """テトリミノをゲームフィールドに固定"""
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    self.game_field[(tetrimino.y + y)//10][(tetrimino.x + x)//10] = 1
                    print(self.game_field)
    
    



if __name__ == "__main__":
    App()
