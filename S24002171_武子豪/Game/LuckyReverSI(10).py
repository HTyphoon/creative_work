# 3.10
# Version0.8
# 更新履歴
# 1:Board複製機能 Func(getBoardCopy)
# 2：角にあるか判定機能 Func(isOnCorner)
# 3；ゲーム終了判定機能　Func(isGameOver)
# 4：ゲームのこまはボードリストに添付した。
# 5：駒がボード上に置くが成功、問題：ある時点で一部のこまがうまくリバーシできず、原因調べ。
# ---------
# 6:ReverSI基本プレイの完成。
# 7:誰の番を決める
# --------
# 8:右上の文字の入れ替え機能を作成して
# 9:相手の番なのに自分も行けるアルゴリズム問題を阻止する
# *10:入れられるところをヒントとして示す
# 11:行けない時に相手のターンになる
# 12:Lucky要素１ボード(2x2)内はランダムに色が変化する
# 13:開始ボタンを押した後開始ボタンが消失
# **14:ランダムの具現化エフェクトを考慮する
# 15:Startボタンを押した後に誰の番かを教える
# 16白が最初の時に黒が先に動き出す問題
# 17最後の時に白がに連続で駒が入れない状態に入る func isOnvalid ????
# 18詰まった時、番を相手に譲る
# 19一番外の輪において押したら、中Reverse駒は一定の確率でReverseしない
# *game over提示修正
# ***20 サイコロの演出
# *21両方が立ち止まった時にゲームは終わる
# *22ゲームが終わった時に何ができる（もう一回？）

import os
import sys
import random
import pygame
from pygame.locals import *
import time
import subprocess

# 駒のデータ設定
def black(x, y):
    a = 30
    b = 30
    c = 30
    pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
    pygame.display.update()


def white(x, y):
    a = 240
    b = 240
    c = 240
    pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
    pygame.display.update()


# ヒント駒を提示する
# def hint(x, y):
#     a = 188
#     b = 44
#     c = 44
#     pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
#     pygame.display.update()
#
#
# def gray(x, y):
#     a = 128
#     b = 128
#     c = 128
#     pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
#     pygame.display.update()


# 　一時放置ボード情報をリセット
def resetBoard(newboard):
    # もしstart bottomもしくはボードデータ初期値に戻す。
    for x in range(8):
        for y in range(8):
            newboard[x][y] = 'none'

    newboard[3][3] = 'black'
    newboard[3][4] = 'white'
    newboard[4][4] = 'black'
    newboard[4][3] = 'white'


def getNewBoard():
    board = []
    for i in range(8):
        for j in range(8):
            board.append(['none'] * 8)
    return board


# 行動が合理的なのか
def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != 'none':
        return False
    board[xstart][ystart] = tile
    if tile == 'black':
        otherTile = 'white'
    else:
        otherTile = 'black'

    # Reveseこま
    tilesToflip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = xstart, ystart
        x += xdirection
        y += ydirection
        # ***
        # マウス座標点周りの全ての点を調査ボード範囲内か
        if isOnBoard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isOnBoard(x, y):
                continue
            while board[x][y] == otherTile:
                x += xdirection
                y += ydirection
                if not isOnBoard(x, y):
                    break
            if not isOnBoard(x, y):
                continue
            if board[x][y] == tile:
                while True:
                    x -= xdirection
                    y -= ydirection
                    if x == xstart and y == ystart:
                        break
                    tilesToflip.append([x, y])
    board[xstart][ystart] = 'none'
    if len(tilesToflip) == 0:
        return False
    return tilesToflip


# ボード内にあるのか
def isOnBoard(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


# 規則：入れるところを探す
def getValidMoves(board, tile, col, row):
    validMoves = []

    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y):
                validMoves.append([x, y])
            # 色表示でプレイヤに示す
            # if tile == 'black':
            #     # (x,y)に入れられるところがあったら、ValidMovesに入れる
            #     if isValidMove(board, tile, x, y):
            #         validMoves.append([x, y])
            #         hint(x, y)
            # if tile == 'white':
            #     # (x,y)に入れられるところがあったら、ValidMovesに入れる
            #     if isValidMove(board, tile, x, y):
            #         validMoves.append([x, y])
            #         gray(x, y)
    return validMoves


# スコアをカウントする
def getScoreBoard(board):
    score_bl = 0
    score_wh = 0
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'black':
                score_bl += 1
            if board[x][y] == 'white':
                score_wh += 1
    # 計算されたscoreをボード上に反映する
    # print(score_bl)
    return {'black': score_bl, 'white': score_wh}


# 　スコアを表示
def getScore():
    black_score = getScoreBoard(mainBoard)[playerTile_1]
    white_score = getScoreBoard(mainBoard)[playerTile_2]
    return black_score, white_score


# 誰が先かを提示する。
def whoGoesFirst(score_bl, score_wh):
    if count == 0:
        if score_bl == score_wh:
            return 'player1'
        if score_bl < score_wh:
            return 'player1'
        if score_bl > score_wh:
            return 'player2'
    else:
        pass


# 　反転するかしないかの確率を判断する関数
def flipProbability(probability):
    if random.random() <= probability:
        return False
    else:
        return True


# 規則：moveの規則
def makeMove(board, tile, xstart, ystart):
    # リバーサされた駒を示す
    tilesToflip = isValidMove(board, tile, xstart, ystart)
    if tilesToflip == False:
        return False

    board_size = 8
    # 1/3の確率で変化しない
    probability = 1 / 3
    # 一番外の輪の座標を示す
    outer_circle = [(i, 0) for i in range(board_size)] + \
                   [(board_size - 1, i) for i in range(board_size)] + \
                   [(i, board_size - 1) for i in range(board_size)] + \
                   [(0, i) for i in range(1, board_size - 1)]
    # 現在の座標
    current_coodi = (xstart, ystart)

    # 今の選択は一番外の時に中のReverseのタイルは一定の確率で保持する
    if current_coodi in outer_circle:
        board[xstart][ystart] = tile
        for x, y in tilesToflip:
            if (x, y) in outer_circle:
                board[x][y] = tile
            elif flipProbability(probability):
                board[x][y] = tile
    else:
        board[xstart][ystart] = tile
        for x, y in tilesToflip:
            board[x][y] = tile
    return True


# Copy board将来は置き換えするために置く
# def getBoardCopy(board):
#     dupeBoard = getNewBoard()
#
#     for x in range(8):
#         for y in range(8):
#             dupeBoard[x][y] = board[x][y]
#     return dupeBoard


# 　角にあるかを判断
def isOncorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


# 　ゲームは終わりなのかを判断
def isGameOver(board):
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'none':
                return False
    return True


def endboard(black_score, white_score):
    if black_score > white_score:
        print('black and white',black_score, white_score)
        outputStr = "Winner is Player1 !!"
        text = basicFont.render(outputStr, True, (255, 255, 255), (0, 0, 255))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery
        screen.blit(text, textRect)
    elif black_score < white_score:
        print('black and white',black_score, white_score)
        outputStr = "Winner is Player2 !!"
        text = basicFont.render(outputStr, True, (255, 255, 255), (0, 0, 255))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery
        screen.blit(text, textRect)
    elif black_score == white_score:
        print('black and white', black_score,white_score)
        outputStr = "Draw"
        text = basicFont.render(outputStr, True, (255, 255, 255), (0, 0, 255))
        textRect = text.get_rect()
        textRect.centerx = screen.get_rect().centerx
        textRect.centery = screen.get_rect().centery
        screen.blit(text, textRect)

# tileによって次誰の番かを判定する
def nextIsWhoseText(playtile):
    coverText = pygame.Rect(830, 60, 930, 120)
    pygame.draw.rect(screen, (238, 154, 73), coverText)
    font = pygame.font.SysFont('Arial', 30)
    text_color = (15, 15, 15)
    text1 = font.render("White Round", True, text_color)
    text2 = font.render("Black Round", True, text_color)

    if playtile == 'white':
        screen.blit(text1, (830, 60))
    else:
        screen.blit(text2, (830, 60))


def monitorBoard():
    coverText_1 = pygame.Rect(830, 100, 930, 148)
    pygame.draw.rect(screen, (238, 154, 73), coverText_1)
    coverText_2 = pygame.Rect(830, 220, 930, 300)
    pygame.draw.rect(screen, (238, 154, 73), coverText_2)

    pygame.draw.line(screen, (15, 15, 15), (753, 0), (753, 740), 8)
    pygame.draw.circle(screen, (15, 15, 15), [850, 148], 20)
    pygame.draw.circle(screen, (240, 240, 240), [850, 296], 20)
    font = pygame.font.SysFont('Arial', 30)
    text_color = (15, 15, 15)
    text = font.render("Number", True, text_color)
    text1_rect = text.get_rect()
    text1_rect.center = (930, 148)
    text2_rect = text.get_rect()
    text2_rect.center = (930, 296)
    screen.blit(text, text1_rect)
    screen.blit(text, text2_rect)

    # 　Create 2 count block
    black_score, white_score = getScore()
    rect1 = pygame.Rect(832, 188, 160, 74)
    rect2 = pygame.Rect(832, 188 + 148, 160, 74)
    pygame.draw.rect(screen, (196, 196, 196), rect1)
    pygame.draw.rect(screen, (196, 196, 196), rect2)
    number_color = (15, 15, 15)
    font1 = pygame.font.SysFont('Arial', 40)
    black_text = font1.render(str(black_score), True, number_color)
    white_text = font1.render(str(white_score), True, number_color)
    screen.blit(black_text, (905, 198))
    screen.blit(white_text, (905, 198 + 148))
    pygame.display.update()

    return black_score, white_score


# Lucky Elements
class Dice:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.value = None
        self.images = [
            pygame.image.load("1_dots.png"),
            pygame.image.load("2_dots.png"),
            pygame.image.load("3_dots.png"),
            pygame.image.load("4_dots.png"),
            pygame.image.load("5_dots.png"),
            pygame.image.load("6_dots.png")
        ]

    def roll(self):
        self.value = random.randint(1, 6)

    def display(self, screen):
        image = self.images[self.value - 1]
        image = pygame.transform.scale(image, (self.size, self.size))
        screen.blit(image, (self.x, self.y))


def diceAnimetion():
    # 初始化Pygame
    pygame.init()

    # 定义窗口尺寸和标题
    window_width = 500
    window_height = 500
    window = pygame.display.set_mode((window_width, window_height))

    # 创建骰子对象
    dice_size = 100
    dice1_x = window_width // 3 - dice_size // 3
    dice1_y = window_height // 2 - dice_size // 2
    dice1 = Dice(dice1_x, dice1_y, dice_size)

    dice2_x = window_width * 2 // 3 - dice_size * 2 // 3
    dice2_y = window_height // 2 - dice_size // 2
    dice2 = Dice(dice2_x, dice2_y, dice_size)

    # 間隔時間と動画時間
    FPS = 5
    duration = 5
    EndRollTime = 3

    # タイマー
    timer = pygame.time.Clock()
    start_time = time.time()

    # 游戏循环
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # ボタンを押して、サイコロは停止する
        while (time.time() - start_time) < duration:
            window.fill((255, 255, 255))
            # 填充窗口背景
            while (time.time() - start_time) < EndRollTime:
                dice1.roll()
                dice1.display(window)

                dice2.roll()
                dice2.display(window)
                pygame.display.update()
                timer.tick(5)
            #print(dice1.value, dice2.value)
            dice_pl1 = dice1.value
            dice_pl2 = dice2.value
        running = False

    # 退出Pygame
    return dice_pl1, dice_pl2



# ラッキースタートボタンの設定
def startButton(x, y, black_score, white_score):
    # Set Lucky start button
    font = pygame.font.SysFont('Arial', 28)
    # button size
    button_rect = pygame.Rect(850, 550, 120, 80)
    text = font.render("Start", True, (15, 15, 15))
    text_rect = text.get_rect()
    text_rect.center = (910, 590)
    pygame.draw.rect(screen, (200, 200, 200), button_rect)
    screen.blit(text, text_rect)

    if button_rect.collidepoint(x, y) and event.type == MOUSEBUTTONDOWN:
        global button_pressed
        button_pressed = True
        # *****
        # player1 and 2 サイコロを投げる＋演出効果
        dice_Pl1, dice_Pl2 = diceAnimetion()
        # dice
        # print("dice_Pl1, dice_Pl2", dice_Pl1, dice_Pl2)
        if dice_Pl1 > dice_Pl2:
            # white -> black　[3,4][4,3]
            pos = random.choice([(3, 4), (4, 3)])
            mainBoard[pos[0]][pos[1]] = "black"
            nextIsWhoseText(playerTile_2)
        elif dice_Pl1 < dice_Pl2:
            # black -> white
            pos = random.choice([(3, 3), (4, 4)])
            mainBoard[pos[0]][pos[1]] = "white"
            nextIsWhoseText(playerTile_1)
        else:
            nextIsWhoseText(playerTile_1)
        #     pass
        black_score, white_score = getScore()
        # print("black_score, white_score", black_score, white_score)
        # pygame.display.update()
    if button_pressed:
        coverStartButton()

    # if the button is pressed 1):butoom disappear
    # 2):player1_dice = random(1,6)
    # 3):player2_dice = random(1,6)
    # 4):compare big and small
    # 5):random 1 tile color change
    return black_score, white_score


def coverStartButton():
    coverButton = pygame.Rect(850, 550, 120, 80)
    pygame.draw.rect(screen, (238, 154, 73), coverButton)


if __name__ == "__main__":
    pygame.init()
    mainClock = pygame.time.Clock()
    pygame.display.set_caption("LuckyReverSI")
    screen_width, screen_height = 1080, 740
    os.environ['SDL_VIDEO_CENTRED'] = '1'

    # create background and board
    Background_Col = (238, 154, 73)
    Board_Col = (38, 178, 44)
    screen = pygame.display.set_mode([screen_width, screen_height])
    screen.fill(Background_Col)
    a = pygame.Surface((696, 696), flags=pygame.HWSURFACE)
    a.fill(color='#121010')
    b = pygame.Surface((656, 656), flags=pygame.HWSURFACE)
    b.fill(color='#121010')
    e = pygame.Surface((81, 81), flags=pygame.HWSURFACE)
    e.fill(color=Board_Col)
    screen.blit(a, (27, 27))
    screen.blit(b, (47, 47))

    # 初期こまをどうやって入れるかを考える。
    for j in range(8):
        for i in range(8):
            screen.blit(e, (47 + 82 * i, 47 + 82 * j))
    mainBoard = getNewBoard()
    resetBoard(mainBoard)

    # ->score init_set func
    black_score = 2
    white_score = 2
    count = 0
    # スタートボタンを押さないと最初は黒が先に始まる
    turn = whoGoesFirst(black_score, white_score)
    if turn == 'player1':
        playerTile_1 = 'black'
        playerTile_2 = 'white'
    else:
        playerTile_1 = 'white'
        playerTile_2 = 'black'
    gameOver = False
    button_pressed = False
    done = True

    while True:
        # 黒と白の駒数をモニターに示す。

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            x, y = pygame.mouse.get_pos()
            col = round((x - 82) / 82)
            row = round((y - 82) / 82)

            # スタート押したらボタンが消える
            # ここでサイコロ動画を入れる
            if count == 0:
                black_score, white_score = startButton(x, y, black_score, white_score)
            else:
                coverStartButton()

            # スタートを押したら
            black_num, white_num = monitorBoard()
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and count == 0:

                turn = whoGoesFirst(black_score, white_score)
                if turn == 'player1':
                    playerTile_1 = 'black'
                    playerTile_2 = 'white'
                else:
                    playerTile_1 = 'black'
                    playerTile_2 = 'white'
                count += 1

            if gameOver == False and turn == 'player1' and event.type == MOUSEBUTTONDOWN and event.button == 1:
                # 文字の切り替え
                # 黒の駒が入れたら次は白が入れられる
                if makeMove(mainBoard, playerTile_1, col, row):
                    if getValidMoves(mainBoard, playerTile_2, col, row):
                        nextIsWhoseText(playerTile_2)
                        turn = 'player2'
                        pygame.display.update()

            if gameOver == False and turn == 'player2' and event.type == MOUSEBUTTONDOWN and event.button == 1:
                # 文字の切り替え
                # 白の駒が入れたら次は黒が入れられる
                if makeMove(mainBoard, playerTile_2, col, row):
                    if getValidMoves(mainBoard, playerTile_1, col, row):
                        nextIsWhoseText(playerTile_1)
                        turn = 'player1'
                        pygame.display.update()

        for x in range(8):
            for y in range(8):
                if mainBoard[x][y] == 'black':
                    black(x, y)

                elif mainBoard[x][y] == 'white':
                    white(x, y)

        if isGameOver(mainBoard):
            #getScoreBoard()
            basicFont = pygame.font.SysFont(None, 48)
            black_score,white_score = monitorBoard()
            endboard(black_score, white_score)
        pygame.display.update()
        mainClock.tick(40)

        # こまを入れる。
