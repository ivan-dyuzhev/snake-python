from collections import deque, namedtuple
import random
import pygame

BOARD_LENGTH = 32
OFFSET = 16
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


DIRECTIONS = namedtuple('DIRECTIONS',
        ['Up', 'Down', 'Left', 'Right'])(0, 1, 2, 3)


def find_food(spots):
    while True:
        food = random.randrange(BOARD_LENGTH), random.randrange(BOARD_LENGTH)
        if (not (spots[food[0]][food[1]] == 1 or
            spots[food[0]][food[1]] == 2)):
            break
    return food


def end_condition(board, coord):
    if (coord[0] < 0 or coord[0] >= BOARD_LENGTH or coord[1] < 0 or
            coord[1] >= BOARD_LENGTH):
        return True
    if (board[coord[0]][coord[1]] == 1):
        return True
    return False


def update_board(screen, snake, food):
    rect = pygame.Rect(0, 0, OFFSET, OFFSET)

    spots = [[] for i in range(BOARD_LENGTH)]
    num1 = 0
    num2 = 0
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)
            temprect = rect.move(num1 * OFFSET, num2 * OFFSET)
            pygame.draw.rect(screen, WHITE, temprect)
            num2 += 1
        num1 += 1
    spots[food[0]][food[1]] = 2
    temprect = rect.move(food[1] * OFFSET, food[0] * OFFSET)
    pygame.draw.rect(screen, BLACK, temprect)
    for coord in snake:
        spots[coord[0]][coord[1]] = 1
        temprect = rect.move(coord[1] * OFFSET, coord[0] * OFFSET)
        pygame.draw.rect(screen, coord[2], temprect)
    return spots

def rand_color():
    return (random.randrange(254), random.randrange(254), random.randrange(254))

# Return 0 to exit the program, 1 for a one-player game
def menu(screen):
    menu_message = pygame.font.Font(None, 30).render("Press enter to start", True, BLACK)
    screen.fill(WHITE)
    screen.blit(menu_message, (32, 32)) 
    pygame.display.update()
    while True: 
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    entered = True
                    return 1
        if done:
            break
    if done:
        pygame.quit()
        return 0

def quit(screen):
    return False

# Return false to quit program, true to go to
# gameover screen
def oneplayer(screen): 
    clock = pygame.time.Clock()

    spots = [[] for i in range(BOARD_LENGTH)]
    for row in spots:
        for i in range(BOARD_LENGTH):
            row.append(0)

    # Board set up
    tailmax = 4
    direction = DIRECTIONS.Right
    snake = deque()
    snake.append((0, 0, rand_color()))
    spots[0][0] = 1
    food = find_food(spots)

    while True:
        clock.tick(15)
        # Event processing
        done = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quit given")
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if direction != DIRECTIONS.Down:
                        direction = DIRECTIONS.Up
                elif event.key == pygame.K_DOWN:
                    if direction != DIRECTIONS.Up:
                        direction = DIRECTIONS.Down
                elif event.key == pygame.K_RIGHT:
                    if direction != DIRECTIONS.Left:
                        direction = DIRECTIONS.Right
                elif event.key == pygame.K_LEFT:
                    if direction != DIRECTIONS.Right:
                        direction = DIRECTIONS.Left
                break

        if done:
            return False

        # Game logic
        head = snake.pop()
        if (direction == DIRECTIONS.Up):
            next_head = (head[0] - 1, head[1], rand_color())
        elif (direction == DIRECTIONS.Down):
            next_head = (head[0] + 1, head[1], rand_color())
        elif (direction == DIRECTIONS.Left):
            next_head = (head[0], head[1] - 1, rand_color())
        elif (direction == DIRECTIONS.Right):
            next_head = (head[0], head[1] + 1, rand_color())
        if (end_condition(spots, next_head)):
            print(next_head)
            print("end condition reached")
            return tailmax

        if spots[next_head[0]][next_head[1]] == 2:
            tailmax += 4
            food = find_food(spots)

        snake.append(head)
        snake.append(next_head)

        if len(snake) > tailmax:
            tail = snake.popleft()

        # Draw code
        screen.fill(WHITE)  # makes screen white

        spots = update_board(screen, snake, food)

        pygame.display.update()

def game_over(screen, eaten):
    message1 = "You ate %d foods" % eaten
    game_over_message1 = pygame.font.Font(None, 30).render(message1, True, BLACK)
    message2 = "Press enter to play again, esc to quit."
    game_over_message2 = pygame.font.Font(None, 30).render(message2, True, BLACK)

    screen.blit(game_over_message1, (32, 32))
    screen.blit(game_over_message2, (62, 62))
    pygame.display.update()

    while True: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_RETURN:
                    return True

 


def main():
    pygame.init()
    screen = pygame.display.set_mode([BOARD_LENGTH * OFFSET,
        BOARD_LENGTH * OFFSET])
    pygame.display.set_caption("Snaake")

    first = True
    playing = True
    while playing:
        if first:
            pick = menu(screen)

        options = {0 : quit,
                1 : oneplayer}
        now = options[pick](screen)
        if now == False:
            break
        else:
            eaten = now / 4 - 1
            playing = game_over(screen, eaten)
            first = False

    pygame.quit()

if __name__ == "__main__":
    main()
