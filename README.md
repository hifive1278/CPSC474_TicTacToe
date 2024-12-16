# CPSC474_TicTacToe
Henry Chen
Matt Neissen

when we ran pypy3 simulate.py 2:
```
Running simulations with 2 games each...

Random Agent vs Simple Greedy Agent:
Random Agent wins: 0 (0.00%)
Simple Greedy Agent wins: 2 (100.00%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent:
Random Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 2 (100.00%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent:
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 2 (100.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent:
MCTS wins: 1 (50.00%)
Advanced Greedy Agent wins: 1 (50.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent:
MAST wins: 2 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent:
AMAF wins: 0 (0.00%)
Advanced Greedy Agent wins: 2 (100.00%)
Draws: 0 (0.00%)
```

makes sense because AMAF not really built for Tic tac toe, whereas MAST is better for a game like TCT.