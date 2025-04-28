import itertools
import random

class Minesweeper:
    """
    Minesweeper game representation
    """
    def __init__(self, height=8, width=8, mines=5, safe_cell=(3, 3)):
        self.height = height
        self.width = width
        self.totalMines = mines
        self.safe_cell = safe_cell
        self.mines = set()
        self.board = []
        for i in range(self.height):
            row = [False] * self.width
            self.board.append(row)
        while len(self.mines) < self.totalMines:
            i = random.randrange(height)
            j = random.randrange(width)
            if (i, j) != self.safe_cell and not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True
        self.mines_found = set()

    def print(self):
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                print("|X" if self.board[i][j] else "| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1
        return count

    def won(self):
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    """
    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count
        self.mines = set()
        self.safes = set()

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __hash__(self):
        return hash((frozenset(self.cells), self.count))

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        return self.cells.intersection(self.mines)

    def known_safes(self):
        return self.cells.intersection(self.safes)

    def mark_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
            self.mines.add(cell)

    def mark_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.safes.add(cell)


class MinesweeperAI:
    def __init__(self, height, width, mines):
        self.height = height
        self.width = width
        self.movesMade = set()
        self.mines = set()
        self.totalMines = mines
        self.safeMoves = set()
        self.knowledge = []

    def mark_mine(self, cell):
        self.mines.add(cell)
        # Update all sentences to reflect the new mine
        for sentence in self.knowledge:
            if cell in sentence[0]:
                sentence[0].discard(cell)
                sentence[1] -= 1

    def mark_safe(self, cell):
        self.safeMoves.add(cell)
        # Update all sentences to reflect the new safe cell
        for sentence in self.knowledge:
            sentence[0].discard(cell)

    def add_knowledge(self, cell, count):
        self.movesMade.add(cell)
        self.mark_safe(cell)
        new_sentence = {(i, j) for i in range(cell[0] - 1, cell[0] + 2)
                        for j in range(cell[1] - 1, cell[1] + 2)
                        if 0 <= i < self.height and 0 <= j < self.width
                        and (i, j) not in self.movesMade}
        if new_sentence:
            self.knowledge.append([new_sentence, count])
        self.update_knowledge()

    def update_knowledge(self):
        updated = True
        while updated:
            updated = False
            for sentence in self.knowledge[:]:
                cells, count = sentence
                known_mines = cells & self.mines
                known_safes = cells & self.safeMoves
                cells = cells - known_mines - known_safes
                count -= len(known_mines)
                if count < 0 or count > len(cells):
                    self.knowledge.remove(sentence)
                    updated = True
                    continue
                if not cells:
                    self.knowledge.remove(sentence)
                    updated = True
                    continue
                # Collect cells to mark instead of modifying during iteration
                if len(cells) == count and count > 0:
                    cells_to_mark = set(cells)  # Copy to avoid iteration issues
                    self.knowledge.remove(sentence)
                    updated = True
                    for cell in cells_to_mark:
                        self.mark_mine(cell)
                elif count == 0 and cells:
                    cells_to_mark = set(cells)  # Copy to avoid iteration issues
                    self.knowledge.remove(sentence)
                    updated = True
                    for cell in cells_to_mark:
                        self.mark_safe(cell)
                else:
                    # Update the sentence only if no immediate action was taken
                    sentence[0] = cells
                    sentence[1] = count

    def get_unrevealed(self):
        return [(i, j) for i in range(self.height) for j in range(self.width)
                if (i, j) not in self.movesMade and (i, j) not in self.mines]

    def make_safe_move(self):
        safe_choices = self.safeMoves - self.movesMade
        return random.choice(tuple(safe_choices)) if safe_choices else None

    def csp_move(self):
        safes = set()
        mines = set()
        for cells, count in self.knowledge:
            if count == 0:
                safes.update(cells)
            elif len(cells) == count:
                mines.update(cells)
        for s1, c1 in self.knowledge:
            for s2, c2 in self.knowledge:
                if s1 == s2:
                    continue
                if s1.issubset(s2):
                    new_cells = s2 - s1
                    new_count = c2 - c1
                    if new_count == 0:
                        safes.update(new_cells)
                    elif len(new_cells) == new_count:
                        mines.update(new_cells)
        newly_safe = safes - self.movesMade - self.safeMoves
        newly_mine = mines - self.movesMade - self.mines
        for cell in newly_safe:
            self.mark_safe(cell)
        for cell in newly_mine:
            self.mark_mine(cell)
        self.update_knowledge()
        available_safes = self.safeMoves - self.movesMade
        return random.choice(tuple(available_safes)) if available_safes else None

    def partial_overlap_inference(self):
        """
        Analyze pairs of sentences with partial overlap to create new sentences
        for non-overlapping cells, which may lead to new safe or mine inferences.
        """
        new_sentences = []
        for (s1, c1), (s2, c2) in itertools.combinations(self.knowledge, 2):
            if s1 == s2 or not (s1 & s2):
                continue
            overlap = s1 & s2
            s1_only = s1 - s2
            s2_only = s2 - s1
            new_cells = s1_only | s2_only
            new_count = c1 + c2 - 2 * len(overlap)
            if new_count >= 0 and new_cells:
                new_sentences.append([new_cells, new_count])
        for cells, count in new_sentences:
            if count == 0:
                for cell in cells:
                    self.mark_safe(cell)
            elif len(cells) == count:
                for cell in cells:
                    self.mark_mine(cell)
            else:
                self.knowledge.append([cells, count])
        self.update_knowledge()

    def infer_overlap_mines(self):
        new_mines = set()
        for s1, c1 in self.knowledge:
            for s2, c2 in self.knowledge:
                if s1 == s2:
                    continue
                if s1.issubset(s2):
                    diff_cells = s2 - s1
                    diff_count = c2 - c1
                    if diff_count == len(diff_cells):
                        new_mines.update(diff_cells)
        for cell in new_mines:
            self.mark_mine(cell)
        if new_mines:
            print(f"Inferred mines from overlap logic: {new_mines}")

    def overlapping_mine(self):
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
                            for sentence, count in self.knowledge:
                                if neighbor in sentence and count == 1:
                                    return cell
        return None

    def bayesian_inference(self, unrevealed):
        if not unrevealed:
            return None
        totalMines_left = self.totalMines - len(self.mines)
        prior = totalMines_left / len(unrevealed)
        cell_probs = {cell: prior for cell in unrevealed}
        for sentence, count in self.knowledge:
            if not sentence:
                continue
            unknown_cells = sentence - self.mines - self.safeMoves
            if not unknown_cells:
                continue
            likelihood = count / len(unknown_cells)
            for cell in unknown_cells:
                cell_probs[cell] = (cell_probs[cell] + likelihood) / 2
        safest_cell = min(cell_probs, key=lambda cell: cell_probs[cell])
        if cell_probs[safest_cell] >= 0.8 or len(unrevealed) == 63:
            return None
        return safest_cell

    def monte_carlo_search(self, unrevealed, simulations=10000):
        if not unrevealed:
            return None
        move_scores = {cell: 0 for cell in unrevealed}
        mines_left = self.totalMines - len(self.mines)
        known_mines = set(self.mines)
        known_safes = set(self.safeMoves    )
        candidates = [cell for cell in unrevealed if cell not in known_mines and cell not in known_safes]
        if not candidates:
            return None
        for _ in range(simulations):
            try:
                simulated_mines = set(random.sample(candidates, mines_left))
            except ValueError:
                continue
            simulated_mines.update(known_mines)
            consistent = True
            for sentence, count in self.knowledge:
                mines_in_cells = len([cell for cell in sentence if cell in simulated_mines])
                if mines_in_cells != count:
                    consistent = False
                    break
            if not consistent:
                continue
            for cell in unrevealed:
                if cell not in simulated_mines:
                    move_scores[cell] += 1
        for safe in known_safes:
            if safe in move_scores:
                return safe
        if all(score == 0 for score in move_scores.values()):
            return random.choice(candidates)
        safest_cell = max(move_scores, key=lambda cell: move_scores[cell])
        return safest_cell

    def smart_move(self):
        """
        AI Agent:
        Logical moves
            1. Safe moves - propositional logic
            2. CSP-based logical inference
            3. Partial overlap inference
        If no unrevealed cells or unrevealed cells + mines = total mines, return None
            4. Overlapping mine - Infer more mines using overlap neighbors and return safe
        If no unrevealed cells or unrevealed cells + mines = total mines, return None
        Probabilistic moves when no logical move exists
            1. Bayesian inference, return None when probability is high
            2. Monte Carlo search, return cell after 10000 simulations
        """
        #Try a known safe move
        move = self.make_safe_move()
        if move:
            return move

        #Try CSP logical inference
        move = self.csp_move()
        if move:
            return move

        #Try partial overlap inference
        self.partial_overlap_inference()
        move = self.make_safe_move()
        if move:
            return move

        #Check unrevealed cells
        unrevealed = self.get_unrevealed()
        if not unrevealed or len(unrevealed) + len(self.mines) == self.totalMines:
            for cell in unrevealed:
                self.mark_mine(cell)
            return None

        # Try to infer mines and find low-risk nearby move
        self.infer_overlap_mines()
        move = self.overlapping_mine()
        if move:
            return move

        #Check unrevealed cells again
        unrevealed = self.get_unrevealed()
        if not unrevealed or len(unrevealed) + len(self.mines) == self.totalMines:
            for cell in unrevealed:
                self.mark_mine(cell)
            return None

        #Use Bayesian inference
        move = self.bayesian_inference(unrevealed)
        if move:
            return move

        #Use Monte Carlo search
        move = self.monte_carlo_search(unrevealed)
        if move:
            return move

        return None