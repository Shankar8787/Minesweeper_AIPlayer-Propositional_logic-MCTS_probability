Minesweeper AI
A Minesweeper-playing artificial intelligence agent that leverages propositional logic, constraint satisfaction, and probabilistic reasoning to efficiently navigate the Minesweeper game board, minimizing the risk of triggering mines.

Overview
This project implements a Minesweeper AI agent capable of autonomously playing the game.
The agent utilizes a combination of logical inference, advanced constraint-solving techniques, and probabilistic analysis to make optimal decisions throughout gameplay.

How the AI Works
Safe First Move:
The AI always initiates gameplay by selecting a guaranteed safe cell.

Logical Inference:
The agent identifies safe cells and mines through propositional logic based on revealed information.
It applies Constraint Satisfaction Problem (CSP) techniques to deduce further information from the current knowledge base.

Overlap-Based Reasoning:
When sentences in the knowledge base overlap, the agent infers additional mines by analyzing the relationships between overlapping sets.

Probabilistic Decision Making:
If logical moves are exhausted:
Bayesian Inference estimates the probability of each unrevealed cell containing a mine.
Monte Carlo Simulation runs numerous simulated game states to statistically determine the safest available move.

Endgame Handling:
If the number of unrevealed cells equals the number of undiscovered mines, the AI marks all remaining cells as mines.

Project Structure
Component	        Description
Minesweeper	      Represents the game board, mine placement, and game logic.
Sentence	        Represents logical statements about sets of cells and mine counts.
MinesweeperAI	      Implements the AI agent, including logic inference and decision-making strategies.

Key AI Methods
make_safe_move(): Selects a move from cells already identified as safe.
csp_move(): Applies constraint satisfaction to infer safe cells or mines.
infer_overlap_mines(): Identifies additional mines through overlap analysis.
bayesian_inference(): Estimates mine probabilities based on current knowledge.
monte_carlo_search(): Simulates numerous board states to evaluate safest moves.
choose_move(): Executes the complete decision-making pipeline to select the next move.

Instructions for Use
Start the game by triggering the AI to play.
The AI will perform an initial safe move.
The AI continues to play by applying logical reasoning or probabilistic models when necessary.
The final result (win/loss) is displayed at the end of the game.
To play again, reset the game board.

Rule Summary
Click the Play button to begin.
The AI starts with a guaranteed safe move.
It applies logical reasoning to deduce safe cells and mines.
If necessary, it uses probability to minimize risk.
The game result is presented upon completion; reset the board to start a new game.

Techniques Employed
Propositional Logic for safe and mine deduction.
Constraint Propagation to infer additional knowledge.
Subset-Superset Analysis for overlap inference.
Bayesian Reasoning to estimate risk.
Monte Carlo Simulation for probabilistic decision-making.
Integration with graphical user interfaces (Pygame).

Potential Future Enhancements
Integration with graphical user interfaces (e.g., Tkinter, Pygame).
Optimization for larger, more complex boards.

Incorporation of reinforcement learning for adaptive gameplay.


## License

This project is open-source and released under the [MIT License](https://opensource.org/licenses/MIT).

Get ready to challenge your logical thinking and try your hand at Minesweeper! Can you successfully flag all the mines? Have fun! 💣💡
