# CPSC474_TicTacToe
Henry Chen
Matt Neissen


After finding out Alpha-Beta and MCTS had similar-ish results, we decided to further explore MCTS and how the different enhancements might affect it?

when we 50 trails:
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

and when we ran 100 trials:
```
hjc43@rattlesnake:~/cs474/final_proj$ pypy3 simulate.py 100
Running simulations with 100 games each...

Random Agent vs Simple Greedy Agent:
Random Agent wins: 5 (5.00%)
Simple Greedy Agent wins: 95 (95.00%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent:
Random Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 100 (100.00%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent:
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 100 (100.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent:
MCTS wins: 99 (99.00%)
Advanced Greedy Agent wins: 1 (1.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent:
MAST wins: 100 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent:
AMAF wins: 92 (92.00%)
Advanced Greedy Agent wins: 8 (8.00%)
Draws: 0 (0.00%)
```

These results make sense logically because AMAF (with RAVE) is not really built for Qubic. Move order is highly critical, making the AMAF assumption that moves have similar values regardless of when they're played potentially misleading.

Move Averaging Sampling Technique (MAST), on the other hand, learns to bias moves that are better (i.e. taking the center or corners?). It can potentially rapidly identify generally good moves, leading to faster convergence on optimal play. One draw back, though, is that it tends to favor games with a larger state space, so that it can adequately update its global statistics for move rewards to a useful level.