# CPSC474_TicTacToe
Henry Chen, Matt Neissen

### Overview of our agents developed:

1. **Random**: randomly picks a valid position out of the 64 max. possible to place piece. 
2. **Simple Greedy**: if there's a 4-in-a-row available, play it to win. Otherwise, play randomly.
3. **Advanced Greedy**: follow the static evaluator heuristic 
4. **Alpha-Beta pruning Minimax**
5. **MCTS**
6. **MCTS w/ AMAF + RAVE**
7. **MCTS w/ MAST**

### Simplifications since our video
Switched from 4x4x4 to 3x3x3 because otherwise the state space would be too large, and MCTS would need an absurdly long amount of time per move (5+ sec) in order to get reasonable results that beat the greedy baseline.

### Running our code
```
pypy3 simulate.py <# of trials> <time limit for MCTS>
```
(Alpha-Beta is always set to a depth of 4)

## PART 1: HOW DOES MCTS (+ ITS ENHANCEMENTS) STACK UP TO ALPHA-BETA PRUNING?
*For quick replication/testing: if you run like 20-25 trials with 0.25s time limit for MCTS and depth of 4 for Alpha-Beta it should take like ~3-5 min.*
```
hjc43@peacock:~/cs474/final_proj$ time pypy3 simulate.py 20 0.25
Running simulations with 20 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 3 (0.30%)
Simple Greedy Agent wins: 997 (99.70%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 1 (0.10%)
Advanced Greedy Agent wins: 999 (99.90%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 1000 (100.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs Advanced Greedy Agent (20 games):
Alpha Beta Agent wins: 20 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent (20 games):
MCTS wins: 17 (85.00%)
Advanced Greedy Agent wins: 3 (15.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MCTS Agent (20 games):
Alpha Beta Agent wins: 20 (100.00%)
MCTS Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MAST Agent (20 games):
Alpha Beta Agent wins: 7 (35.00%)
MAST Agent wins: 13 (65.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent (20 games):
MAST wins: 19 (95.00%)
Advanced Greedy Agent wins: 1 (5.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent (20 games):
AMAF wins: 17 (85.00%)
Advanced Greedy Agent wins: 3 (15.00%)
Draws: 0 (0.00%)

real	3m21.225s
user	3m20.152s
sys	0m1.026s
```
```
hjc43@peacock:~/cs474/final_proj$ time pypy3 simulate.py 25 0.25
Running simulations with 25 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 2 (0.20%)
Simple Greedy Agent wins: 998 (99.80%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 1000 (100.00%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 1000 (100.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs Advanced Greedy Agent (25 games):
Alpha Beta Agent wins: 25 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent (25 games):
MCTS wins: 18 (72.00%)
Advanced Greedy Agent wins: 7 (28.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MCTS Agent (25 games):
Alpha Beta Agent wins: 25 (100.00%)
MCTS Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MAST Agent (25 games):
Alpha Beta Agent wins: 19 (76.00%)
MAST Agent wins: 6 (24.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs AMAF Agent (25 games):
Alpha Beta Agent wins: 25 (100.00%)
AMAF Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent (25 games):
MAST wins: 23 (92.00%)
Advanced Greedy Agent wins: 2 (8.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent (25 games):
AMAF wins: 10 (40.00%)
Advanced Greedy Agent wins: 15 (60.00%)
Draws: 0 (0.00%)

real	4m36.163s
user	4m34.645s
sys	0m1.481s
```
**Interpretation**: 
* Alpha-Beta and MCTS both perform extremely well against the adv. greedy baseline
* Alpha-Beta does much better compared to MCTS head-to-head, but not as much once you add the MAST enhancement to MCTS
* MAST enhancement outperforms AMAF enhancement, which makes sense logically (as explained later)

### The trials we ran: 
Baseline models (10,000 trials)
- Random vs. Simple Greedy
- Random vs. Adv. Greedy
- Simple vs. Adv. Greedy

New models against the baseline (100-375 trials)
- Alpha-Beta vs. Adv. Greedy
- MCTS vs. Adv. Greedy

Head-to-head (100-375 trials)
- Alpha-Beta vs. MCTS 
- Alpha-Beta vs. MAST
- Alpha-Beta vs. AMAF

Comparing MAST to AMAF enhancements (100-375 trials) (remove for later section)
- MAST vs. Adv. Greedy
- AMAF vs. Adv. Greedy

*because MCTS/Alpha-Beta takes so long to run, we opted for less trials

### Results 1: quick 20 min testing (0.5s time limit each, 4-depth)
```
hjc43@rattlesnake:~/cs474/final_proj$ time pypy3 simulate.py 100
Running simulations with 100 games each...

Random Agent vs Simple Greedy Agent:
Random Agent wins: 0 (0.00%)
Simple Greedy Agent wins: 100 (100.00%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent:
Random Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 100 (100.00%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent:
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 100 (100.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs Advanced Greedy Agent:
Alpha Beta Agent wins: 100 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent:
MCTS wins: 98 (98.00%)
Advanced Greedy Agent wins: 2 (2.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MCTS Agent:
Alpha Beta Agent wins: 100 (100.00%)
MCTS Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MAST Agent:
Alpha Beta Agent wins: 14 (14.00%)
MAST Agent wins: 86 (86.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent:
MAST wins: 99 (99.00%)
Advanced Greedy Agent wins: 1 (1.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent:
AMAF wins: 83 (83.00%)
Advanced Greedy Agent wins: 17 (17.00%)
Draws: 0 (0.00%)

real	22m11.706s
user	22m4.281s
sys	0m7.071s
```

### Results 2: More robust testing - 4hrs (1s time, 4-depth, just like in pset4)





### Why is MCTS performing worse than Alpha-Beta here?
We corroborate the same results as when you run the quick ~3.5 min test. 
Alpha-Beta has a better pruning step than MCTS and considering how much there is... 



## Part 2. EXPLORATION OF MCTS ENHANCEMENTS
After finding out Alpha-Beta and MCTS had similar-ish results, we decided to further explore MCTS and how the different enhancements might affect it?

### when we 50 trials (2s time limit each):
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

### and when we ran 100 trials (2s time limit each):
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