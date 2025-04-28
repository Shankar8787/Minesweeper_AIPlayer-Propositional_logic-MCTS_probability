# Minesweeper AI

A Minesweeper-playing artificial intelligence agent that leverages **propositional logic**, **constraint satisfaction**, and **probabilistic reasoning** to efficiently navigate the Minesweeper game board, minimizing the risk of triggering mines.

---

## Overview

This project implements a Minesweeper AI agent capable of autonomously playing the game.  
The agent utilizes a combination of logical inference, advanced constraint-solving techniques, and probabilistic analysis to make optimal decisions throughout gameplay.

---

## How the AI Works

1. **Safe First Move:**
   - The AI always initiates gameplay by selecting a guaranteed safe cell.

2. **Logical Inference:**
   - The agent identifies safe cells and mines through propositional logic based on revealed information.
   - It applies **Constraint Satisfaction Problem (CSP)** techniques to deduce further information from the current knowledge base.

3. **Overlap-Based Reasoning:**
   - When sentences in the knowledge base overlap, the agent infers additional mines by analyzing the relationships between overlapping sets.

4. **Probabilistic Decision Making:**
   - If logical moves are exhausted:
     - **Bayesian Inference** estimates the probability of each unrevealed cell containing a mine.
     - **Monte Carlo Simulation** runs numerous simulated game states to statistically determine the safest available move.

5. **Endgame Handling:**
   - If the number of unrevealed cells equals the number of undiscovered mines, the AI marks all remaining cells as mines.

---

## Project Structure

| Component        | Description                                                       |
|------------------|-------------------------------------------------------------------|
| `Minesweeper`     | Represents the game board, mine placement, and game logic.        |
| `Sentence`        | Represents logical statements about sets of cells and mine counts. |
| `MinesweeperAI`   | Implements the AI agent, including logic inference and decision-making strategies. |

---

## Key AI Methods

- `make_safe_move()`: Selects a move from cells already identified as safe.
- `csp_move()`: Applies constraint satisfaction to infer safe cells or mines.
- `infer_overlap_mines()`: Identifies additional mines through overlap analysis.
- `bayesian_inference()`: Estimates mine probabilities based on current knowledge.
- `monte_carlo_search()`: Simulates numerous board states to evaluate safest moves.
- `choose_move()`: Executes the complete decision-making pipeline to select the next move.

---

## Instructions for Use

1. Start the game by triggering the AI to play.
2. The AI will perform an initial safe move.
3. The AI continues to play by applying logical reasoning or probabilistic models when necessary.
4. The final result (win/loss) is displayed at the end of the game.
5. To play again, reset the game board.

---

## Rule Summary

- Click the **Play** button to begin.
- The AI starts with a guaranteed safe move.
- It applies logical reasoning to deduce safe cells and mines.
- If necessary, it uses probability to minimize risk.
- The game result is presented upon completion; reset the board to start a new game.

---

## Techniques Employed

- **Propositional Logic** for safe and mine deduction.
- **Constraint Propagation** to infer additional knowledge.
- **Subset-Superset Analysis** for overlap inference of mines.
- **Partial Overlap Analysis** for overlap cells from centence to determine safe cells.
- **Bayesian Reasoning** to estimate risk.
- **Monte Carlo Simulation** for probabilistic decision-making.
- **Integration with graphical user interfaces (e.g., Tkinter, Pygame).

---

## Results

- Begginer     -   Upto 80% success rate (9*9 board with 10 mines)
- Intermittent -   Upto 50% success rate (16*16 board with 40 mines)
- Expert       -   Upto 10% success rate (30*16 board with 99 mines)

---

## Potential Future Enhancements

- Optimization for larger, more complex boards.
- Incorporation of reinforcement learning for adaptive gameplay.

---
