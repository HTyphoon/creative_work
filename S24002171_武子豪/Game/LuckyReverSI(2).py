import os
import sys
# import random
import pygame
from pygame.locals import *
import numpy as np


# import numpy as np

# 駒のデータ設定
def black(x, y):
    a = 20
    b = 20
    c = 20
    for i in range(50):
        pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
        a += 1
        b += 1
        c += 1
    pygame.display.update()


def white(x, y):
    a = 249
    b = 240
    c = 240
    for i in range(50):
        pygame.draw.circle(screen, (a, b, c), [88 + 82 * x, 88 + 82 * y], 34)
        a += 1
        b += 1
        c += 1
    pygame.display.update()


# 左のボード構築。
# 　そして全ての座標点をBoard(8x8)内におく
def create_board():
    # ボードを描く


    # # 座標をボードに入れる。
    # board = [[[] for i in range(8)] for j in range(8)]
    # cell_size = 82
    # for x in range(47, 703):
    #     for y in range(47, 703):
    #         row = (y - 47) // cell_size
    #         col = (x - 47) // cell_size
    #         board[row][col].append((x, y))
    # print(np.shape(board))
    # pygame.display.update()

    return


# 　一時放置ボード情報をリセット
def restBoard(newboard):
    # 今後実装if buttom = "start"
    # もしstart bottomもしくはボードデータ初期値に戻す。
    for i in range(8):
        newboard.append(['None'] * 8)
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
    if not isONboard() or board[xstart][ystart] != 'none':
        return False
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
        # わかってない
        if isONboard(x, y) and board[x][y] == otherTile:
            x += xdirection
            y += ydirection
            if not isONboard(x, y):
                break
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


def isONboard(x, y):
    return 0 <= x <= 7 and 0 <= y <= 7


def getValidMoves(board, tile):
    validMoves = []
    for x in range(8):
        for y in range(8):
            if isValidMove(board, tile, x, y) != False:
                validMoves.append([x, y])
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
    print(score_bl)

    return {'black':score_bl,'white':score_wh}
# 　右のカウントボードを作る

def makeMove(board, tile, xstart, ystart):
    tilesToflip = isValidMove(board, tile, xstart, ystart)
    if tilesToflip == False:
        return False
    board[xstart][ystart] = tile
    for x, y in tilesToflip:
        board[x][y] = tile
    return True



def monitorBoard():
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

    # 　二つカウントブロックの生成

    rect1 = pygame.Rect(832, 188, 160, 74)
    rect2 = pygame.Rect(832, 188 + 148, 160, 74)
    pygame.draw.rect(screen, (196, 196, 196), rect1)
    pygame.draw.rect(screen, (196, 196, 196), rect2)
    global black_number, white_number
    number_color = (15, 15, 15)
    font1 = pygame.font.SysFont('Arial', 40)
    black_text = font1.render(str(black_number), True, number_color)
    white_text = font1.render(str(white_number), True, number_color)
    screen.blit(black_text, (905, 198))
    screen.blit(white_text, (905, 198 + 148))

    # 問題：これを変換し、目的はwhite_number.count()など、駒数を計算して、printする
    white_number += 1
    pygame.display.update()

    return black_number, white_number


# 　一時放置
def check_over_pos(x, y, over_pos):
    for val in over_pos:
        if val[0][0] == x and val[0][1] == y:
            return False
    return True


if __name__ == "__main__":
    pygame.init()
    mainClock = pygame.time.Clock()
    pygame.display.set_caption("LuckyReverSI")
    screen_width, screen_height = 1080, 740
    os.environ['SDL_VIDEO_CENTRED'] = '1'
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
    # Boardリストを導入し、それらをblack_numberに入れる。

    black_number = 2
    white_number = 2
    screen.blit(a, (27, 27))
    screen.blit(b, (47, 47))

    # 初期こまをどうやって入れるかを考える。
    for j in range(8):
        for i in range(8):
            screen.blit(e, (47 + 82 * i, 47 + 82 * j))
    pygame.draw.circle(screen, (15, 15, 15), [334, 334], 34)
    pygame.draw.circle(screen, (15, 15, 15), [416, 416], 34)
    pygame.draw.circle(screen, (240, 240, 240), [334, 416], 34)
    pygame.draw.circle(screen, (240, 240, 240), [416, 334], 34)



    # こまをボードに入れる
    alist = []
    for j in range(8):
        alison = []
        for i in range(8):
            alison.append(0)
        alist.append(alison)

    wb = "black"
    while True:
        black_num, white_num = monitorBoard()
        mainClock.tick(10)
        print(white_num)
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                x = round((x - 82) / 82)
                y = round((y - 82) / 82)

        #         if alist[x][y] == 0:
        #             # print(alist)
        #             eval(wb + "({},{})".format(x, y))
        #
        #             if wb == "black":
        #                 alist[x][y] = 1
        #                 wb1 = "黒駒"
        #                 wb = "white"
        #             elif wb == "white":
        #                 alist[x][y] = 2
        #                 wb1 = "白駒"
        #                 wb = "black"
        #
        #             xx = x
        #             yy = y
        #             while True:
        #                 if xx == 0:
        #                     break
        #                 elif alist[xx][yy] != alist[x][y]:
        #                     xx += 1
        #                     break
        #                 else:
        #                     xx -= 1
        #             num = 0
        #             while True:
        #                 if xx == 7:
        #                     break
        #                 elif alist[xx][yy] != alist[x][y]:
        #                     break
        #                 else:
        #                     xx += 1
        #                     num += 1
