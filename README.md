# CPSC474_TicTacToe
Henry Chen
Matt Neissen

when we ran pypy3 simulate.py 50:
```
hjc43@rattlesnake:~/cs474/final_proj$ pypy3 simulate.py 50
Running simulations with 50 games each...

Random Agent vs Simple Greedy Agent:
Random Agent wins: 2 (4.00%)
Simple Greedy Agent wins: 48 (96.00%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent:
Random Agent wins: 1 (2.00%)
Advanced Greedy Agent wins: 49 (98.00%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent:
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 50 (100.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent:
MCTS wins: 48 (96.00%)
Advanced Greedy Agent wins: 2 (4.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent:
MAST wins: 50 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent:
AMAF wins: 44 (88.00%)
Advanced Greedy Agent wins: 6 (12.00%)
Draws: 0 (0.00%)
```

makes sense because AMAF not really built for Tic tac toe, whereas MAST is better for a game like TCT.