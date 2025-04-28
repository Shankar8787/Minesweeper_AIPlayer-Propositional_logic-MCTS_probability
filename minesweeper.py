import itertools
import random
from itertools import product
import math


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
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.total_mines = mines
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

    def get_unrevealed(self):
        """
        Returns a list of all cells that are not revealed and not marked as mines.
        """
        return [
            (i, j) for i in range(self.height) for j in range(self.width)
            if (i, j) not in self.moves_made and (i, j) not in self.mines
        ]


    def make_safe_move(self):
        safe_choices = self.safe_moves - self.moves_made
        return random.choice(tuple(safe_choices)) if safe_choices else None

    def csp_move(self):
        safes = set()
        mines = set()

        #Direct inference: safe or mine from known counts
        for sentence, count in self.knowledge:
            if count == 0:
                safes.update(sentence)
            elif len(sentence) == count:
                mines.update(sentence)

        #Subset inference: If one sentence subset of another
        for (s1, c1) in self.knowledge:
            for (s2, c2) in self.knowledge:
                if s1 == s2:
                    continue
                if s1.issubset(s2):
                    new_cells = s2 - s1
                    new_count = c2 - c1
                    if new_count == 0:
                        safes.update(new_cells)
                    elif len(new_cells) == new_count:
                        mines.update(new_cells)

        #Mark inferred safes/mines immediately
        newly_safe = safes - self.moves_made - self.safe_moves
        newly_mine = mines - self.moves_made - self.mines

        for cell in newly_safe:
            self.mark_safe(cell)

        for cell in newly_mine:
            self.mark_mine(cell)

        #Update knowledge base after inference
        self.update_knowledge()

        #Return a new safe move if available
        available_safes = self.safe_moves - self.moves_made
        if available_safes:
            move = available_safes.pop()
            #print("CSP Move: Found logical safe move:", move)
            return move

        return None


    def infer_overlap_mines(self):
        """
        Try to find certain mines by analyzing overlaps between nearby revealed cells.
        Only called when few cells remain and mines are still missing.
        """

        new_mines = set()

        # Compare all sentences with each other
        for (cells1, count1) in self.knowledge:
            for (cells2, count2) in self.knowledge:
                if cells1 == cells2:
                    continue

                # If one sentence is subset of another
                if cells1.issubset(cells2):
                    diff_cells = cells2 - cells1
                    diff_count = count2 - count1

                    if diff_count == len(diff_cells):
                        # All different cells must be mines
                        new_mines.update(diff_cells)

        # Mark the inferred mines
        for cell in new_mines:
            self.mark_mine(cell)

        if new_mines:
            print(f"Inferred mines from overlap logic: {new_mines}")

    def overlapping_mine(self):
        """
        Find an unrevealed cell adjacent to a known mine where the nearby knowledge count is 1.
        """

        unrevealed = self.get_unrevealed()

        for cell in unrevealed:
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    ni, nj = cell[0] + dx, cell[1] + dy
                    neighbor = (ni, nj)

                    if 0 <= ni < self.height and 0 <= nj < self.width:
                        if neighbor in self.mines:
                            # Check knowledge about the neighbor
                            for sentence, count in self.knowledge:
                                if neighbor in sentence and count == 1:
                                    #print(f"Overlapping mine move found: {cell}")
                                    return cell

        return None

    def bayesian_inference(self, unrevealed):
        """
        Use Bayesian inference when few choices remain.
        """
        if not unrevealed:
            return None

        total_mines_left = self.total_mines - len(self.mines)
        prior = total_mines_left / len(unrevealed)

        cell_probs = {cell: prior for cell in unrevealed}

        # Adjust probabilities based on known knowledge
        for sentence, count in self.knowledge:
            if not sentence:
                continue

            unknown_cells = sentence - self.mines - self.safe_moves
            if not unknown_cells:
                continue

            likelihood = count / len(unknown_cells)
            for cell in unknown_cells:
                cell_probs[cell] = (cell_probs[cell] + likelihood) / 2

        safest_cell = min(cell_probs, key=lambda cell: cell_probs[cell])
        #print(cell_probs[safest_cell])
        if cell_probs[safest_cell] >=0.8 or len(unrevealed) ==63:
            return None
        else:
            return safest_cell

    def monte_carlo_search(self, unrevealed, simulations=10000):
        """
        Use Monte Carlo simulations to estimate mine probabilities,
        considering known mines, safe moves, and knowledge constraints.
        """
        if not unrevealed:
            return None

        move_scores = {cell: 0 for cell in unrevealed}
        mines_left = self.total_mines - len(self.mines)

        known_mines = set(self.mines)
        known_safes = set(self.safe_moves)

        # Candidates are unrevealed cells not already known to be safe/mine
        candidates = [cell for cell in unrevealed if cell not in known_mines and cell not in known_safes]

        if not candidates:
            return None

        for _ in range(simulations):
            try:
                # Randomly select mines among candidates
                simulated_mines = set(random.sample(candidates, mines_left))
            except ValueError:
                # Skip invalid simulations
                continue

            # Add known mines
            simulated_mines.update(known_mines)

            # Check if the simulated mine assignment is consistent with all knowledge
            consistent = True
            for sentence, count in self.knowledge:
                cells = sentence
                count = count
                if not cells:
                    continue

                # How many of these cells are mines in this simulation?
                mines_in_cells = len([cell for cell in cells if cell in simulated_mines])

                # If the number of mines doesn't match the knowledge, it's invalid
                if mines_in_cells != count:
                    consistent = False
                    break

            if not consistent:
                continue  # discard inconsistent simulation

            # Otherwise, update move scores
            for cell in unrevealed:
                if cell not in simulated_mines:
                    move_scores[cell] += 1

        # Prefer returning a known safe move if available
        for safe in known_safes:
            if safe in move_scores:
                return safe

        # If no consistent simulations were found (scores are all zero), fallback randomly
        if all(score == 0 for score in move_scores.values()):
            return random.choice(candidates)

        # Pick the cell with the highest score (highest chance of being safe)
        safest_cell = max(move_scores, key=lambda cell: move_scores[cell])
        return safest_cell



    def choose_move(self):
        """
        AI Agent:
        Logical moves
            1. Safe moves - propositional logic
            2. CSP-based logical inference
        If no unrevealed cell or unrevealed cell+mines = total Mines the return None
            3. overlapping mine - Infer more mines using overlap neighbors and return safe by using it
        If no unrevealed cell or unrevealed cell+mines = total Mines the return None
        Probability move when no logical move exist
            1. Bayesian inference and return none when probability is high
            2. Monte Carlo search return cell after 10000 simulation
        """

        # 1. Try a known safe move first
        move = self.make_safe_move()
        if move:
            #print("Choosing known safe move:", move)
            return move

        # 2. Try CSP logical inference
        move = self.csp_move()
        if move:
            #print("Choosing CSP logical move:", move)
            return move

        # 3. Prepare unrevealed cells
        unrevealed = self.get_unrevealed()

        #print(len(unrevealed), len(self.mines))

        if not unrevealed or len(unrevealed)+len(self.mines) == self.total_mines:
            for cell in unrevealed:
                self.mines.add(cell)
            return None

        # 4. If few cells left, use low risk nearby move

        # FIRST: Try to infer mines if possible
        self.infer_overlap_mines()
        move = self.overlapping_mine()
        if move:
            #print(f"Choosing low risk nearby move from {len(unrevealed)} options:", move)
            return move

        unrevealed = self.get_unrevealed()
        if not unrevealed or len(unrevealed)+len(self.mines) == self.total_mines:
            for cell in unrevealed:
                self.mines.add(cell)
            return None

        # 5. Else use bayesian inference
        move = self.bayesian_inference(unrevealed)
        if move:
            #print(f"Choosing Bayesian move from {len(unrevealed)} options:", move)
            return move

        # 6. Else use Monte Carlo search
        move = self.monte_carlo_search(unrevealed)
        if move:
            #print("Choosing Monte Carlo move:", move)
            return move

        return None  # No move possible