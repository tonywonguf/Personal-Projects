import pygame as pg
from random import randint

def inbounds(a:tuple, H:int, W:int) -> bool:
    return a[0] >= 0 and a[0] < H and a[1] < W and a[1] >= 0

def direction(dx:int,dy:int) -> str:
    if dy == 1:
        return 'L'
    elif dy == -1:
        return 'R'
    elif dx == 1:
        return 'U'
    elif dx == -1:
        return 'D'

def bfs(curr:tuple, board:[[str]]) -> [[str]]:
    q = []
    q.append(curr)
    while len(q) != 0:
        front = q.pop(0)
        for dx,dy in zip((0,0,-1,1),(1,-1,0,0)):
            next = (dx + front[0], dy + front[1])
            if inbounds(next, len(board),len(board[0])) and (board[next[0]][next[1]] == '.' or board[next[0]][next[1]] == 'O'):
                if board[next[0]][next[1]] == 'O':
                    board[next[0]][next[1]] = direction(dx, dy) + 'O'
                    return board
                board[next[0]][next[1]] = direction(dx,dy)
                q.append(next)
    return board

def get_tas_movements(snack,board) -> [tuple]:
    tas = []
    tas.append(snack)
    while board[tas[-1][0]][tas[-1][1]] != '#':
        movement = (0,0)
        if board[tas[-1][0]][tas[-1][1]][0] == 'U':
            movement = (-1,0)
        if board[tas[-1][0]][tas[-1][1]][0] == 'D':
            movement = (1,0)
        if board[tas[-1][0]][tas[-1][1]][0] == 'L':
            movement = (0,-1)
        if board[tas[-1][0]][tas[-1][1]][0] == 'R':
            movement = (0,1)
        tas.append((tas[-1][0]+movement[0],tas[-1][1]+movement[1]))
    return tas

def get_height() -> int:
    H = -1
    while True:
        try:
            H = int(input("what is ye height selected "))
            if (H > 49):
                print("Please put a number at most 49 :( ")
            elif (H <= 0):
                print("please put a number greater than 0 :(")
            else:
                break;
        except ValueError:
            print("Invalid input - please put a number")
    return H

def get_width() -> int:
    W = -1
    while True:
        try:
            W = int(input("what is ye width selected "))
            if (W > 94):
                print("Please put a number at most 94 :( ")
            elif (W <= 6):
                print("please put a number greater than 6 :(")
            else:
                break;
        except ValueError:
            print("Invalid input - please put a number")
    return W

def main():
    pg.init()
    clock = pg.time.Clock()

    # H = get_height()
    # W = get_width()
    H = 7
    W = 7

    screen = pg.display.set_mode((W*20,H*20))
    surface_snake = pg.Surface((20,20),flags=0)
    surface_snack = pg.Surface((20,20),flags=0)

    surface_snack.fill((0,255,0))
    surface_snake.fill((255,0,0))

    snake = [(randint(0,H-1),randint(0,W-1))]
    snack = (randint(0,H-1),randint(0,W-1))
    while snack in snake:
        snack = (randint(0, H - 1), randint(0, W - 1))

    screen.fill((6 * 16 + 11, 7 * 16 + 13, 7 * 16 + 13))

    screen.blit(surface_snake, (snake[0][1] * 20, snake[0][0] * 20))
    screen.blit(surface_snack, (snack[1] * 20, snack[0] * 20))

    max_size = min(1,W,H)

    movement = (0,0,0,0)

    pg.display.flip()

    running = True;
    while running:
        board = [['.' for i in range(W)] for j in range(H)]
        board[snake[-1][0]][snake[-1][1]] = '#'
        board[snack[0]][snack[1]] = 'O'
        if len(snake) >= W*H:
            print("YOU WIN!")
            break
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN:
                if (event.key == pg.K_LEFT or event.key == pg.K_a) and movement != (0,0,0,1):
                    movement = (0, -1, 0, 0)
                elif (event.key == pg.K_RIGHT or event.key == pg.K_d) and movement != (0,-1,0,0):
                    movement = (0,0,0,1)
                elif (event.key == pg.K_UP or event.key == pg.K_w) and movement != (0,0,1,0):
                    movement = (-1,0,0,0)
                elif (event.key == pg.K_DOWN or event.key == pg.K_s) and movement != (-1,0,0,0):
                    movement = (0,0,1,0)

        if movement != (0,0,0,0):
            next_segment = ((snake[-1][0]+movement[0]+movement[2]) % (H),(snake[-1][1]+movement[1]+movement[3]) % (W))
            snake.append(next_segment)

            if next_segment == snack:
                max_size += 1
                while snack in snake:
                    snack = (randint(0, H - 1), randint(0, W-1))

            if len(snake) > max_size:
                board[snake[0][0]][snake[0][1]] = '.'
                snake.pop(0)

            for segments in snake[:-1]:
                if next_segment == segments:
                    for s in snake:
                        board[s[0]][s[1]] = '#'
                    board[snack[0]][snack[1]] = 'O'
                    while len(snake) > 0:
                        clock.tick(max_size)
                        board[snake[-1][0]][snake[-1][1]] = '.'
                        snake.pop(-1)
                        screen.fill((6 * 16 + 11, 7 * 16 + 13, 7 * 16 + 13))
                        for r in range(H):
                            for c in range(W):
                                if board[r][c] == '#':
                                    screen.blit(surface_snake, (c * 20, r * 20))
                                elif board[r][c] == 'O':
                                    screen.blit(surface_snack, (c * 20, r * 20))

                        pg.display.flip()
                    running = False
                    print("Game Over! You Lose!")
                    break

        for segments in snake:
            board[segments[0]][segments[1]] = '#'
        board[snack[0]][snack[1]] = 'O'

        board = bfs(snake[-1],board)

        TAS_MOVEMENTS = get_tas_movements(snack,board)

        screen.fill((6 * 16 + 11, 7 * 16 + 13, 7 * 16 + 13))
        for r in range(H):
            for c in range(W):
                if board[r][c] == '#':
                    screen.blit(surface_snake, (c * 20, r * 20))
                elif board[r][c][-1] == 'O':
                    screen.blit(surface_snack, (c * 20, r * 20))
        print(*board,sep="\n")
        print(*TAS_MOVEMENTS,sep=" | ")
        print("-"*len(board[0])*5)
        pg.display.flip()
        clock.tick(1)
        # clock.tick(min(20,max(W,H)))


if __name__ == '__main__':
    main()