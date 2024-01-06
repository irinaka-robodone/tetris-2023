import pyxel
from utils import *
import time


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
        self.score = 0
        self.start_time = time.time()
        

        pyxel.init(self.width, self.height, title = "テトリス")
        pyxel.run(self.update, self.draw)

    def create_new_tetrimino(self):
        letter = str(random.choice(list(TETROMINOES.keys())))
        shape = TETROMINOES[letter]
        color = TETROMINOES_COLORS[letter]
        return Tetrimino(shape, 100, color)


    
    def draw(self):
        pyxel.cls(0)
        #pyxel.rect(0,0,10,10,1)
        for tetrimino in self.tetriminos:
            self.draw_tetrimino(tetrimino)
        self.draw_tetrimino(self.tetrimino)
        # スコアとプレイ時間の描画
        self.draw_score_and_time()
    
    def draw_score_and_time(self):
        # 現在のプレイ時間を計算
        current_time = time.time()
        play_time = int(current_time - self.start_time)
        
        # スコアとプレイ時間を右サイドに表示
        pyxel.text(5, 5, f"Score: {self.score}", pyxel.COLOR_WHITE)
        pyxel.text(5, 15, f"Time: {play_time} sec", pyxel.COLOR_WHITE)
    

    def draw_tetrimino(self, tetrimino):
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if cell:
                    screen_x = tetrimino.x + x
                    screen_y = tetrimino.y + y
                    pyxel.rect((tetrimino.x + x *10 ), (tetrimino.y + y * 10), 10, 10, tetrimino.color)


    def check_collision(self, tetrimino, direction, rotated_shape=None):
        self.collided = False
        future_x = tetrimino.x //10
        future_y = tetrimino.y //10
        shape_to_check = rotated_shape if rotated_shape is not None else tetrimino.shape

        if direction == "down":
            future_y += 1
        elif direction == "left":
            future_x -= 1
        elif direction == "right":
            future_x += 1

        for y, row in enumerate(shape_to_check):
            for x, cell in enumerate(row):
                if cell == 1:
                    new_x = future_x + x
                    new_y = future_y + y
                    if new_x < 0 or new_x >= self.width//10 or new_y >= self.height//10 or self.game_field[new_y][new_x]:
                        self.collided = True
                        return True
                    if self.game_field[new_y][new_x]:  # ほかのテトリミノに衝突
                        #self.collided = True
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
    
    def rotate_tetrimino(self, tetrimino, direction):
        """ テトリミノを回転させる """
        if direction == "right":
            # 右回転 (時計回り)
            rotated_shape = list(zip(*tetrimino.shape[::-1]))
        elif direction == "left":
            # 左回転 (反時計回り)
            rotated_shape = list(zip(*tetrimino.shape))[::-1]
        
        # 回転後の衝突をチェック
        if not self.check_collision(tetrimino, None, rotated_shape):
            tetrimino.shape = rotated_shape
        
    def check_and_clear_rows(self):
        # 埋まった行を探す
        rows_to_clear = []
        for y, row in enumerate(self.game_field):
            if all(cell for cell in row):
                rows_to_clear.append(y)
        
        for y in reversed(rows_to_clear):
            # 埋まった行を削除し、上の行を下にずらす
            del self.game_field[y]
            self.game_field.insert(0, [0 for _ in range(self.widh // 10)])
            # スコアを更新する
            self.score += 150

    def update(self):
        if self.game_over:
            return
        
        self.check_and_clear_rows()
        
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
            for key in pyxel.input_keys:
                print(key)
            if pyxel.btnp(pyxel.KEY_LEFT):
                if not self.check_collision(self.tetrimino, "left"):
                    self.move_tetrimino(self.tetrimino, "left")
            # テトリミノを右に移動
            if pyxel.btnp(pyxel.KEY_RIGHT):
                if not self.check_collision(self.tetrimino, "right"):
                    self.move_tetrimino(self.tetrimino, "right")
            # テトリミノを右回転
            if pyxel.btnp(pyxel.KEY_RSHIFT):
                if not self.check_collision(self.tetrimino, "rotate"):
                    self.rotate_tetrimino(self.tetrimino, "right")
            # テトリミノを左回転
            if pyxel.btnp(pyxel.KEY_SLASH):
                if not self.check_collision(self.tetrimino, "rotate"):
                    self.rotate_tetrimino(self.tetrimino, "left")

        # テトリミノが床に達した時の確認
        if self.check_collision(self.tetrimino,"down"):
            # テトリミノが底に達したので固定する
            self.tetrimino_locked = True
            # 新しいテトリミノの生成などの処理
            #for y, row in enumerate(tetrimino.shape):
            #    for x, cell in enumerate(row):
            #        if cell:
            #            self.field[tetrimino.y + y][tetrimino.x + x] = 1
            self.tetriminos.append(self.tetrimino)
            self.place_tetrimino(self.tetrimino)
            self.tetrimino = self.create_new_tetrimino()
            self.tetrimino_locked = False
        """ テトリミノをゲームフィールドに固定する """
    # def place_tetrimino(self):
    #     for y, row in enumerate(self.tetrimino.shape):
    #         for x, cell in enumerate(row):
    #             if cell:
    #                 field_x = self.tetrimino.x + x
    #                 field_y = self.tetrimino.y + y
    #                 if 0 <= field_x < self.width and 0<= field_y < self.height:
    #                     self.field[field_y][field_x] = 1  # フィールドにテトリミノを追加
        
    def place_tetrimino(self,tetrimino):
        """テトリミノをゲームフィールドに固定"""
        for y, row in enumerate(tetrimino.shape):
            for x, cell in enumerate(row):
                if  cell == 1:
                    self.game_field[(tetrimino.y//10 + y)][(tetrimino.x//10 + x)] = 1
    
    



if __name__ == "__main__":
    App()
