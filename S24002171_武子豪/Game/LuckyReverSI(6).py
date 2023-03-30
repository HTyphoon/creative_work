# 3.5
# Version0.5
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
# 8右上の文字の入れ替え機能を作成して
# 9相手の番なのに自分も行けるアルゴリズム問題を阻止する
# *10入れられるところを色で示す
# 11行けない時に相手のターンになる
# *12Lucky要素１ボード(2x2)内はランダムに変化する*
# 13
# *13開始ボタンを押した後ランダムする


import os
import sys
import random
import pygame
from pygame.locals import *
import numpy as np


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
    # for i in range(50):
    pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
    # a += 1
    # b += 1
    # c += 1
    pygame.display.update()


# ヒント駒を提示する
def hint(x, y):
    a = 188
    b = 44
    c = 44
    pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
    pygame.display.update()


# 　一時放置ボード情報をリセット
def resetBoard(newboard):
    # 今後実装if buttom = "start"
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


# ****
# 行動が合理的なのか
def isValidMove(board, tile, xstart, ystart):
    if not isOnBoard(xstart, ystart) or board[xstart][ystart] != 'none':
        # print("It's not on the board", xstart, ystart)
        return False
    board[xstart][ystart] = tile
    # print("board[xstart][ystart]", xstart, ystart)
    # print(tile)
    if tile == 'black':
        # print("Next is white")
        otherTile = 'white'
    else:
        # print("Next is black")
        otherTile = 'black'

    # Reveseこま
    tilesToflip = []
    for xdirection, ydirection in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        # クリックしたところ周囲の点を探す
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


def isOnBoard(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


# こまの入れるところを見つける
def getValidMoves(board, tile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
                # 色表示でプレイヤに示す
                # hint(x,y)
    return validMoves


# 毎回駒数を計算する
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


# 誰がいくかを提示する。
def whoGoesFirst(score_bl, score_wh):
    if score_bl == score_wh:
        return 'player1'
    if score_bl < score_wh:
        return 'player1'
    if score_bl > score_wh:
        return 'player2'


def makeMove(board, tile, xstart, ystart):
    # リバーサされた駒を示す
    tilesToflip = isValidMove(board, tile, xstart, ystart)
    if tilesToflip == False:
        return False

    board[xstart][ystart] = tile
    for x, y in tilesToflip:
        board[x][y] = tile
    return True


# Copy board
# 将来は置き換えするために置く
def getBoardCopy(board):
    dupeBoard = getNewBoard()

    for x in range(8):
        for y in range(8):
            dupeBoard[x][y] = board[x][y]
    return dupeBoard


def isOncorner(x, y):
    return (x == 0 and y == 0) or (x == 7 and y == 0) or (x == 0 and y == 7) or (x == 7 and y == 7)


def isGameOver(board):
    for x in range(8):
        for y in range(8):
            if board[x][y] == 'none':
                return False
    return True


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


# リバーシした後ボードに入れる駒は必ず異なる色の駒に規定する
# def isTileTurn():


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
    black_score = getScoreBoard(mainBoard)[playerTile_1]
    white_score = getScoreBoard(mainBoard)[playerTile_2]
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


# ラッキースタートボタンの設定
def startButton(x, y, black_score, white_score):
    # Set Lucky start button
    font = pygame.font.SysFont('Arial', 28)
    # button daxiao
    button_rect = pygame.Rect(850, 550, 120, 80)
    text = font.render("Start", True, (15, 15, 15))
    text_rect = text.get_rect()
    text_rect.center = (910, 590)
    pygame.draw.rect(screen, (200, 200, 200), button_rect)
    screen.blit(text, text_rect)

    # 判断条件
    done = False
    button_pressed = False
    if button_rect.collidepoint(x, y) and event.type == MOUSEBUTTONDOWN:
        button_pressed = True
        # *****
        # button一時しか消えない問題
        coverStartButton()
        #pygame.display.update()
        #player1 and 2 サイコロを投げる＋演出効果
        dice_Pl1 = random.randint(1, 6)
        dice_Pl2 = random.randint(1, 6)
        print("dice_Pl1, dice_Pl2", dice_Pl1, dice_Pl2)
        if dice_Pl1 > dice_Pl2:
            # white -> black
            black_score += 1
            white_score -= 1
        elif dice_Pl1 < dice_Pl2:
            # black -> white
            black_score -= 1
            white_score += 1
        # else:
        #     pass
        print("black_score, white_score", black_score, white_score)
        # pygame.display.update()

    # pygame.display.update()
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

    turn = whoGoesFirst(black_score, white_score)
    if turn == 'player1':
        playerTile_1 = 'black'
        playerTile_2 = 'white'
    else:
        playerTile_1 = 'white'
        playerTile_2 = 'black'
    gameOver = False

    while True:
        # 黒と白の駒数をモニターに示す。
        black_num, white_num = monitorBoard()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            fps = int(pygame.mouse.get_pos()[0] / 10)
            mainClock.tick(fps)
            x, y = pygame.mouse.get_pos()
            col = round((x - 82) / 82)
            row = round((y - 82) / 82)
            black_score, white_score = startButton(x, y, black_score, white_score)

            if gameOver == False and turn == 'player1' and event.type == MOUSEBUTTONDOWN and event.button == 1:
                # 文字の切り替え
                # 黒の駒が入れたら次は白が入れられる
                if makeMove(mainBoard, playerTile_1, col, row):
                    if getValidMoves(mainBoard, playerTile_1):
                        nextIsWhoseText(playerTile_2)
                        turn = 'player2'
                        pygame.display.update()

            if gameOver == False and turn == 'player2' and event.type == MOUSEBUTTONDOWN and event.button == 1:
                # 文字の切り替え
                # 白の駒が入れたら次は黒が入れられる
                if makeMove(mainBoard, playerTile_2, col, row):
                    if getValidMoves(mainBoard, playerTile_1):
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
            scorePlayer_1 = getScoreBoard(mainBoard)[playerTile_1]
            scorePlayer_2 = getScoreBoard(mainBoard)[playerTile_2]

        # こまを入れる。
