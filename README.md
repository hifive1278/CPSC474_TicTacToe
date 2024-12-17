# CPSC474_TicTacToe
Henry Chen, Matt Neissen \
December 17, 2024

## PROJECT OVERVIEW

### Overview of our agents developed:

1. **Random**: randomly picks a valid position (out of the 64 maximum possible) to place piece. 
2. **Simple Greedy**: if there's a 4-in-a-row available, play it to win. Otherwise, play randomly.
3. **Advanced Greedy**: follows the static evaluator heuristic defined in our video. Essentially, it counts the # of n-in-a-rows and weights them accordingly based on the relative magnitude of n. Opponent's values are weighted slightly higher to encourage 'blocking' behavior.
4. **Alpha-Beta Pruning Minimax**: search to a depth of 4.
5. **MCTS**: standard MCTS that uses UCB formula for depth search. Uses dictionary rather than classes for slight time improvement.
6. **MCTS w/ AMAF + RAVE**: MCTS but with the all-moves-as-first (AMAF) enhancement that is weighted alongside UCB using the Rapid Action Value Estimation (RAVE) enhancement. 
7. **MCTS w/ MAST**: MCTS but with move averaging sampling technique (MCTS). Keeps track of reward statistics for certain moves and weights that when doing the simulation step.

### Simplifications since our video
Switched from 4x4x4 to 3x3x3 because otherwise the state space would be too large, and MCTS would need an overly long amount of time per move (5s+) in order to get reasonable results that beat the greedy baseline.

Switched to MAST and AMAF MCTS enhancements over UCT-2 because we thought it'd have more relevant impacts for a game like Qubic.

### Running our code
```
pypy3 simulate.py <# of game trials> <time limit for MCTS>
```
(Alpha-Beta is always set to a depth of 4)

example (that runs in ~5 minutes): `pypy3 simulate.py 25 0.25`

## RESEARCH QUESTION
1. How does MCTS compare to Minimax alpha-beta pruning for Qubic?
2. Follow-up after our preliminary results: Why does MCTS perform worse, and specifically what enhancements are relevant to make it perform better?

## PART 1: HOW DOES MCTS (+ ITS ENHANCEMENTS) STACK UP TO ALPHA-BETA PRUNING?
*For quick replication/testing: if you run like 20-25 trials with 0.25s time limit for MCTS and depth of 4 for Alpha-Beta it should take like ~3-5 min.*

~5 min example:
```
hjc43@peacock:~/cs474/final_proj$ time pypy3 simulate.py 25 0.25
Running simulations with 25 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 17 (0.17%)
Simple Greedy Agent wins: 9983 (99.83%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 2 (0.02%)
Advanced Greedy Agent wins: 9998 (99.98%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 10000 (100.00%)
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
### Observations:
* Alpha-Beta and MCTS both perform extremely well against the advanced greedy baseline (as we expected)
* Alpha-Beta does much better compared to MCTS head-to-head, but not as much once you add the MAST enhancement to MCTS
* MAST enhancement outperforms AMAF enhancement, which makes sense logically (as explained later)

### The comparisons we made:
- **Baseline models (10,000 trials)**
    - Random vs. Simple Greedy
    - Random vs. Adv. Greedy
    - Simple vs. Adv. Greedy

- **New models against the baseline (100-375 trials)**
    - Alpha-Beta vs. Adv. Greedy
    - MCTS vs. Adv. Greedy

- **Head-to-head (100-375 trials)**
    - Alpha-Beta vs. MCTS 
    - Alpha-Beta vs. MAST
    - Alpha-Beta vs. AMAF

- **Comparing MAST to AMAF enhancements (100-375 trials) (explored in Part 2.)**
    - MAST vs. Adv. Greedy
    - AMAF vs. Adv. Greedy

*because MCTS/Alpha-Beta takes so long to run, we opted for less trials

### The trials we ran: 
- 4 depth, 0.25s, 25 games: quick! 5 min
- 4 depth, 0.50s, 100 games: ~30 min
- 4 depth, 1.00s, 375 games ~2.5 hrs

### Results 1a: "quick" 30 min testing (0.5s time limit each, 4-depth)
```
hjc43@peacock:~/cs474/final_proj$ time pypy3 simulate.py 100 0.50
Running simulations with 100 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 27 (0.27%)
Simple Greedy Agent wins: 9973 (99.73%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 10000 (100.00%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 10000 (100.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs Advanced Greedy Agent (100 games):
Alpha Beta Agent wins: 100 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent (100 games):
MCTS wins: 98 (98.00%)
Advanced Greedy Agent wins: 2 (2.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MCTS Agent (100 games):
Alpha Beta Agent wins: 100 (100.00%)
MCTS Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MAST Agent (100 games):
Alpha Beta Agent wins: 41 (41.00%)
MAST Agent wins: 59 (59.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs AMAF Agent (100 games):
Alpha Beta Agent wins: 100 (100.00%)
AMAF Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent (100 games):
MAST wins: 100 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent (100 games):
AMAF wins: 79 (79.00%)
Advanced Greedy Agent wins: 21 (21.00%)
Draws: 0 (0.00%)

real	29m38.983s
user	29m28.835s
sys	0m9.867s
```

### Results 1b: More robust testing - 2.5hrs (1s time, 4-depth - just like in pset4)
```
hjc43@rattlesnake:~/cs474/final_proj$ time pypy3 simulate.py 375 1.0
Running simulations with 375 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 24 (0.24%)
Simple Greedy Agent wins: 9976 (99.76%)
Draws: 0 (0.00%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 3 (0.03%)
Advanced Greedy Agent wins: 9997 (99.97%)
Draws: 0 (0.00%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 10000 (100.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs Advanced Greedy Agent (375 games):
Alpha Beta Agent wins: 375 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MCTS Agent vs Advanced Greedy Agent (375 games):
MCTS wins: 375 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MCTS Agent (375 games):
Alpha Beta Agent wins: 375 (100.00%)
MCTS Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

Alpha Beta Agent vs MAST Agent (375 games):
Alpha Beta Agent wins: 341 (90.93%)
MAST Agent wins: 34 (9.07%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent (375 games):
MAST wins: 375 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent (375 games):
AMAF wins: 360 (96.00%)
Advanced Greedy Agent wins: 15 (4.00%)
Draws: 0 (0.00%)

real	146m30.780s
user	145m59.827s
sys	0m26.975s
```

### Observations/Insights:
- Alpha-Beta always beat the vanilla MCTS.
- However, with the MAST enhancement, MCTS was only beaten 90.93% of the time by Alpha-Beta
- MAST performs better than AMAF against the baseline advanced greedy -- it wins 100% of the time compared to AMAF's 96%. (this will be explored more in part 2).

### Why is MCTS performing worse than Alpha-Beta here?
We corroborate the same results as when you run the quick ~3.5 min test. Alpha-Beta has a better pruning step than MCTS and considering how big the state-size is, it means it can search more move possibilities in the limited computational time that we have. MCTS had to be limited to 0.5s for it to run in a reasonable time. Based on our testing/tuning, it would take a search time of roughly 5s or more for it to be competitive with Alpha-Beta (i.e. MCTS wins 20-30% of the time). But that also requires a large trade-off in terms of time and computational power. 

To support this, observe how in the 0.5s time limit run, vanilla MCTS has a 98% win rate against advanced greedy. However, in the 1.0s time limit run, we see that MCTS comes out with a 100% win rate against advanced greedy. This is an indicator that a longer search time for MCTS results in better-selected moves. We wonder how much better it could get if we had more computational resources available.

This is also what we originally hypothesized in our video presentation, so it's also reassuring to see the data back up our theoretical assumptions.

A follow-up question is: if MCTS performs worse than Alpha-Beta, what enhancements to it work best? That leads us to part 2 of our study.



## PART 2. EXPLORATION OF MCTS ENHANCEMENTS
After finding out Alpha-Beta and MCTS had similar-ish results (compared to greedy) but Alpha-Beta out-performed MCTS head-to-head, we decided to further explore MCTS and how the different enhancements might affect it?

Recall from above (part 1) that Alpha-Beta always beat the vanilla MCTS. However, with the MAST enhancement, MCTS was only beaten 90.93% of the time by Alpha-Beta. Clearly, the MAST enhancement is beneficial to MCTS in the context of Qubic. But why is that? And how do the other enhancements stand up to that? These questions are the foundation of the following two experiments:

We decide to use 2.0s for the time limit of MCTS because now that we're just focusing on MCTS, we want the runs of it to be as thorough as possible, even if that means sacrificing some runtime. 

### Results 2a: when we 50 trials (2s time limit, 4-depth)
```
hjc43@peacock:~/cs474/final_proj$ time pypy3 simulate.py 50 2.0
Running simulations with 50 games each...

MCTS Agent vs Advanced Greedy Agent (50 games):
MCTS wins: 50 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent (50 games):
MAST wins: 48 (96.00%)
Advanced Greedy Agent wins: 2 (4.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent (50 games):
AMAF wins: 38 (76.00%)
Advanced Greedy Agent wins: 12 (24.00%)
Draws: 0 (0.00%)

real	18m26.317s
user	18m19.698s
sys	0m6.387s
```

### Results 2b: and when we ran 100 trials (2s time limit, 4-depth):
```
hjc43@peacock:~/cs474/final_proj$ time pypy3 simulate.py 100 2.0
Running simulations with 100 games each...

MCTS Agent vs Advanced Greedy Agent (100 games):
MCTS wins: 100 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

MAST Agent vs Advanced Greedy Agent (100 games):
MAST wins: 100 (100.00%)
Advanced Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)

AMAF Agent vs Advanced Greedy Agent (100 games):
AMAF wins: 87 (87.00%)
Advanced Greedy Agent wins: 13 (13.00%)
Draws: 0 (0.00%)

real	38m8.131s
user	37m57.717s
sys	0m10.093s
```

### Does this make sense -- why does MAST perform better than AMAF?

These results make sense logically because AMAF (with RAVE) is not really built for Qubic. Move order is highly critical, making the AMAF assumption that moves have similar values regardless of when they're played potentially misleading.

Move Averaging Sampling Technique (MAST), on the other hand, learns to bias moves that are better (i.e. taking the corners or centers). It can potentially rapidly identify generally good moves, leading to faster convergence on optimal play. One drawback, though, is that it tends to favor games with a larger state space, so that it can adequately update its global statistics for move rewards to a useful level.

As a result, we shouldn't expect it to perform the vanilla MCTS by too much (once we are running with an adequate time-limit, which 2s meets). We see this in (2b) when MAST has the same win rate as MCTS and in (2a) when it differs by only 2%. 

## NEXT STEPS?
- Vary depth of Alpha-Beta pruning minimax search, hopefully this can get us a more game theory optimal agent.
- Run our code/simulations with an even longer MCTS time on a more powerful system -- because theoretically, MCTS should converge to minimax.
- Try other MCTS enhancements like parallelism. As Prof. Glenn said, parallelism isn't the best in Python, which is why we opted to not include it for our project.
- Tune the static evaluator to be better. Right now, we have an (n+1)-in-a-row being weighted as 10x better than a n-in-a-row, but is this the most optimal value? If we did more testing, maybe our heuristics could improve.
