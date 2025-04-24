import itertools
import random
from itertools import product


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=5,safe_cell=(3, 3)):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.total_mines = mines
        self.safe_cell = safe_cell
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) < self.total_mines:
            i = random.randrange(height)
            j = random.randrange(width)

            if (i, j) != self.safe_cell and not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True


        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()


    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        # The hash of a Sentence is based on the frozenset of cells and the count
        return hash((frozenset(self.cells), self.count))

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        return self.cells.intersection(self.mines)

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        return self.cells.intersection(self.safes)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1  # Decrease the count when a mine is marked.
            self.mines.add(cell)

def mark_safe(self, cell):
    """
    Updates internal knowledge representation given the fact that
    a cell is known to be safe.
    """
    if cell in self.cells:
        self.cells.remove(cell)
        self.safes.add(cell)


class MinesweeperAI:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safe_moves = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)

    def mark_safe(self, cell):
        self.safe_moves.add(cell)

    def add_knowledge(self, cell, count):
        self.moves_made.add(cell)
        self.mark_safe(cell)

        new_sentence = {(i, j) for i in range(cell[0] - 1, cell[0] + 2)
                        for j in range(cell[1] - 1, cell[1] + 2)
                        if (0 <= i < self.height and 0 <= j < self.width)
                        and (i, j) not in self.moves_made}

        if len(new_sentence) > 0:
            self.knowledge.append((new_sentence, count))

        self.update_knowledge()

    def update_knowledge(self):
        updated = True
        while updated:
            updated = False
            for sentence, count in self.knowledge[:]:
                known_mines = {cell for cell in sentence if cell in self.mines}
                known_safes = {cell for cell in sentence if cell in self.safe_moves}

                if len(known_mines) == count:
                    for cell in sentence - known_mines:
                        self.mark_safe(cell)
                    self.knowledge.remove((sentence, count))
                    updated = True
                elif len(sentence) == count:
                    for cell in sentence:
                        self.mark_mine(cell)
                    self.knowledge.remove((sentence, count))
                    updated = True

    def make_safe_move(self):
        safe_choices = self.safe_moves - self.moves_made
        return random.choice(tuple(safe_choices)) if safe_choices else None

    def make_random_move(self):
        choices = [(i, j) for i, j in product(range(self.height), range(self.width))
                   if (i, j) not in self.moves_made and (i, j) not in self.mines]

        if not choices:
            return None

        move_scores = {move: 0 for move in choices}
        simulations = 100
        num_mines = len(self.mines)

        for move in choices:
            for _ in range(simulations):
                if len(choices) < num_mines:
                    continue
                simulated_mines = random.sample(choices, len(self.mines))
                if move not in simulated_mines:
                    move_scores[move] += 1

        best_move = max(move_scores, key=move_scores.get)
        return best_move


