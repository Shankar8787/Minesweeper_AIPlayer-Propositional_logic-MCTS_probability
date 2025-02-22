# Minesweeper AI

Welcome to Minesweeper! In this project, we've built an AI that can play the classic puzzle game Minesweeper. The goal of Minesweeper is to identify the locations of hidden mines on a grid while avoiding detonating any of them.

## How Minesweeper Works

Minesweeper consists of a grid of cells, where some cells contain hidden mines. Clicking on a cell with a mine causes the game to end. Safe cells reveal a number indicating how many neighboring cells contain mines.

For example, in a 3x3 Minesweeper game, the numbers indicate how many neighboring cells are mines. Armed with this information, a logical player can deduce which cells contain mines and which are safe.

## Propositional Logic

Our AI represents its knowledge about the Minesweeper game using propositional logic. Each cell is treated as a propositional variable that is true if the cell contains a mine and false otherwise.

The AI gains knowledge as safe cells are clicked and numbers are revealed. For instance, if a cell with the number 1 is revealed, the AI knows that one of its neighboring cells must be a mine. We represent this knowledge as a logical sentence, e.g., {A, B, C} = 1, indicating that out of cells A, B, and C, exactly one of them is a mine.

## Knowledge Representation

We represent AI knowledge using the Sentence class. Each sentence contains a set of cells involved and a count of how many of those cells are mines. The AI's knowledge base is a collection of such sentences.

The MinesweeperAI class maintains the AI's knowledge and performs inferences based on that knowledge. The class keeps track of safe cells, known mines, and moves made. The AI uses logical deductions to make safe moves whenever possible.

## Getting Started

To play Minesweeper or let the AI play for you:

1. Clone this repository to your local machine using `git clone`.

2. Open `minesweeper.py` to explore the provided classes and complete the AI's logic.

3. Once all required functions in `minesweeper.py` are implemented, run `python runner.py`.

4. Enjoy playing Minesweeper or watch the AI in action!

### Functionality 1
1. `known_mines`: This function returns a set of all the cells in the sentence that are known to be mines.

2. `known_safes`: This function returns a set of all the cells in the sentence that are known to be safe.

3. `mark_mine`: This function updates the sentence to indicate that a cell is a mine.

4. `mark_safe`: This function updates the sentence to indicate that a cell is safe.

The MinesweeperAI class maintains the AI's knowledge and performs inferences based on that knowledge. The class keeps track of safe cells, known mines, and moves made. The AI uses logical deductions to make safe moves whenever possible.

### Functionality 2

1. `add_knowledge`: This function updates the AI's knowledge based on a new cell and its count. It marks the cell as one of the moves made, a safe cell, and updates any relevant sentences to reflect this information.

2. `make_safe_move`: This function returns a move that is known to be safe. If no safe move can be guaranteed, it returns None.

3. `make_random_move`: This function returns a random move that has not been made and is not known to be a mine. If no such moves are possible, it returns None.


## AI Strategy

The AI will update its knowledge base by inferring new sentences based on the revealed cells. It will make safe moves whenever possible and resort to random moves if no safe move can be guaranteed.


## License

This project is open-source and released under the [MIT License](https://opensource.org/licenses/MIT).

Get ready to challenge your logical thinking and try your hand at Minesweeper! Can you successfully flag all the mines? Have fun! 💣💡
