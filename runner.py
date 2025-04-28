import pygame
import sys
import time

from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 9
WIDTH = 9
MINES = 10
SAFE_Cell = (3, 3)

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 500,500
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 10)
mediumFont = pygame.font.Font(OPEN_SANS, 18)
largeFont = pygame.font.Font(OPEN_SANS, 20)

# Compute board size
BOARD_PADDING = 10
board_width = ((2 / 3) * width) - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES, safe_cell=SAFE_Cell)
ai = MinesweeperAI(height=HEIGHT, width=WIDTH, mines=MINES)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
lost = False

# Show instructions initially
instructions = True

while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    screen.fill(BLACK)

    # Show game instructions
    if instructions:

        # Title
        title = largeFont.render("Play Minesweeper", True, WHITE)
        titleRect = title.get_rect()
        titleRect.center = ((width / 2), 50)
        screen.blit(title, titleRect)

        # Rules
        rules = [
            "Click AI Play to start.",
            "AI makes a safe first move.",
            "It plays using logic to avoid mines.",
            "If stuck, it uses probability to pick a safe cell.",
            "Game results are shown at the end. ",
            "Reset to play again."
        ]
        for i, rule in enumerate(rules):
            line = (largeFont.render(rule, True, WHITE))
            lineRect = line.get_rect()
            lineRect.center = ((width / 2), 150 + 30 * i)
            screen.blit(line, lineRect)

        # Play game button
        buttonRect = pygame.Rect((width / 4), (3 / 4) * height, width / 2, 50)
        buttonText = mediumFont.render("Play Game", True, BLACK)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.center = buttonRect.center
        pygame.draw.rect(screen, WHITE, buttonRect)
        screen.blit(buttonText, buttonTextRect)

        # Check if play button clicked
        click, _, _ = pygame.mouse.get_pressed()
        if click == 1:
            mouse = pygame.mouse.get_pos()
            if buttonRect.collidepoint(mouse):
                instructions = False
                time.sleep(0.3)

        pygame.display.flip()
        continue

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):

            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and lost:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)

            row.append(rect)
        cells.append(row)

    # AI Play 100 games button
    ai100Play = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 200,
        (width / 3) - BOARD_PADDING * 1, 50
    )
    buttonText = mediumFont.render("AIPlay-100 Games", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = ai100Play.center
    pygame.draw.rect(screen, WHITE, ai100Play)
    screen.blit(buttonText, buttonRect)

    # AI Play button
    aiPlay = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height - 130,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("AI Play", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = aiPlay.center
    pygame.draw.rect(screen, WHITE, aiPlay)
    screen.blit(buttonText, buttonRect)

    # Reset button
    resetButton = pygame.Rect(
        (2 / 3) * width + BOARD_PADDING, (1 / 3) * height + 20,
        (width / 3) - BOARD_PADDING * 2, 50
    )
    buttonText = mediumFont.render("Reset", True, BLACK)
    buttonRect = buttonText.get_rect()
    buttonRect.center = resetButton.center
    pygame.draw.rect(screen, WHITE, resetButton)
    screen.blit(buttonText, buttonRect)

    # Display text
    text = "Lost" if lost else "Won" if game.mines == flags else ""
    text = mediumFont.render(text, True, WHITE)
    textRect = text.get_rect()
    textRect.center = ((5 / 6) * width, (2 / 3) * height)
    screen.blit(text, textRect)

    move = None
    first_move_done = False

    left, _, right = pygame.mouse.get_pressed()

    # Check for a right-click to toggle flagging
    if right == 1 and not lost:
        mouse = pygame.mouse.get_pos()
        for i in range(HEIGHT):
            for j in range(WIDTH):
                if cells[i][j].collidepoint(mouse) and (i, j) not in revealed:
                    if (i, j) in flags:
                        flags.remove((i, j))
                    else:
                        flags.add((i, j))
                    time.sleep(0.2)

    elif left == 1:
        mouse = pygame.mouse.get_pos()

        if aiPlay.collidepoint(mouse) and not lost:
                while not lost:
                    if not first_move_done:
                        move = SAFE_Cell
                        print("First Move.")
                        first_move_done = True
                    elif first_move_done:
                        move = ai.smart_move()
                    if move is None:
                        flags = ai.mines.copy()
                        print("No moves left to make.")
                        break
                    if move:
                        if game.is_mine(move):
                            lost = True
                            print("AI Lost ------------------------------")
                        else:
                            nearby = game.nearby_mines(move)
                            revealed.add(move)
                            ai.add_knowledge(move, nearby)

                pygame.display.flip()
                time.sleep(0.2)

        #If AIPlay-100 clicked, make an AI move
        elif ai100Play.collidepoint(mouse) :
            ai_wins = 0
            counter = 0
            for i in range(100):
                game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                ai = MinesweeperAI(height=HEIGHT, width=WIDTH, mines=MINES)
                revealed = set()
                flags = set()
                lost = False
                while not lost:
                    if not first_move_done:
                        move = SAFE_Cell
                        #print("First Move.")
                        first_move_done = True
                    elif first_move_done:
                        move = ai.smart_move()
                    if move is None:
                        flags = ai.mines.copy()
                        print("No moves left to make.")
                        break
                    if move:
                        if game.is_mine(move):
                            lost = True
                            if len(ai.get_unrevealed()) >=55:
                                print("Failed in early steps")
                            elif len(ai.get_unrevealed()) <=12:
                                print("Failed in final steps")
                            print("AI Lost ------------------------------ Identified Mines -", len(ai.mines))
                        else:
                            nearby = game.nearby_mines(move)
                            revealed.add(move)
                            ai.add_knowledge(move, nearby)

                if not lost:
                    ai_wins += 1
                    print(counter)
                first_move_done = False
                counter += 1
            print(f"AI won {ai_wins} out of 100 games.")
            time.sleep(1)


        # Reset game state
        elif resetButton.collidepoint(mouse):
            game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH,mines=MINES)
            revealed = set()
            flags = set()
            lost = False
            continue


    pygame.display.flip()

