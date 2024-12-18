# CPSC 474 Final Project: Qubic
Henry Chen, Matt Neissen \
December 17, 2024

## PROJECT OVERVIEW

### Running our code
```
pypy3 simulate.py <# of game trials> <time limit for MCTS>
```
(Alpha-Beta is always set to a depth of 3)

example (that runs in ~4 minutes): `pypy3 simulate.py 25 0.25` 

or alternatively, use the test script (which will run the 4 min ex. above): if it's your first time `chmod +x test_qubic.sh`. Regardless of if it's your first time, run 
```
./test_qubic.sh
```

### Overview of the agents we developed:

1. **Random**: randomly picks a valid position (out of the 64 maximum possible) to place piece. 
2. **Simple Greedy**: if there's a 4-in-a-row available, play it to win. Otherwise, play randomly.
3. **Advanced Greedy**: follows the static evaluator heuristic defined in our video. Essentially, it counts the # of n-in-a-rows and weights them accordingly based on the relative magnitude of n. Opponent's values are weighted slightly higher to encourage 'blocking' behavior.
4. **Alpha-Beta Pruning Minimax**: search to a depth of 3.
5. **MCTS**: standard MCTS that uses UCB formula for depth search. Uses dictionary rather than classes for slight time improvement.
6. **MCTS w/ AMAF + RAVE**: MCTS but with the all-moves-as-first (AMAF) enhancement that is weighted alongside UCB using the Rapid Action Value Estimation (RAVE) enhancement. 
7. **MCTS w/ MAST**: MCTS but with move averaging sampling technique (MAST). Keeps track of reward statistics for certain moves and weights that when doing the simulation step.

### Simplifications since our video
- Switched from 4x4x4 to 3x3x3 because otherwise the state space would be too large, and MCTS would need an overly long amount of time per move (5s+) in order to get reasonable results that beat the greedy baseline.

- Switched to MAST and AMAF MCTS enhancements over UCT-2 because we thought it'd have more relevant impacts for a game like Qubic.

## RESEARCH QUESTION
1. How does MCTS compare to Minimax alpha-beta pruning for Qubic?
2. Follow-up after our preliminary results: Why does MCTS perform worse compared to Alpha-Beta, and specifically what enhancements are relevant to make it perform better?
3. 2nd follow-up: How much does depth of search affect Alpha-Beta pruning results?

## PART 1: HOW DOES MCTS (+ ITS ENHANCEMENTS) STACK UP TO ALPHA-BETA PRUNING?
*For quick replication/testing: if you run like 20-25 trials with 0.25s time limit for MCTS and depth of 3 for Alpha-Beta it should take like ~3-5 min.*

`pypy3 simulate.py 25 0.25`

~4 min example:
```
hjc43@raven:~/cs474/final_proj$ time pypy3 simulate.py 25 0.25
Running simulations with 25 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 127 (1.27%)
Simple Greedy Agent wins: 9873 (98.73%)
Draws: 0 (0.00%)
First Mover wins: 5115 (51.15%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 26 (0.26%)
Advanced Greedy Agent wins: 9974 (99.74%)
Draws: 0 (0.00%)
First Mover wins: 5026 (50.26%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 10000 (100.00%)
Draws: 0 (0.00%)
First Mover wins: 5000 (50.00%)

Alpha Beta Agent vs Advanced Greedy Agent (25 games):
Alpha Beta Agent wins: 13 (52.00%)
Advanced Greedy Agent wins: 12 (48.00%)
Draws: 0 (0.00%)
First Mover wins: 25 (100.00%)

Alpha Beta Agent vs Simple Greedy Agent (25 games):
Alpha Beta wins: 25 (100.00%)
Simple Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 15 (60.00%)

MCTS Agent vs Advanced Greedy Agent (25 games):
MCTS wins: 13 (52.00%)
Advanced Greedy Agent wins: 12 (48.00%)
Draws: 0 (0.00%)
First Mover wins: 25 (100.00%)

MCTS Agent vs Simple Greedy Agent (25 games):
MCTS wins: 24 (96.00%)
Simple Greedy Agent wins: 1 (4.00%)
Draws: 0 (0.00%)
First Mover wins: 14 (56.00%)

Alpha Beta Agent vs MCTS Agent (25 games):
Alpha Beta Agent wins: 25 (100.00%)
MCTS Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 13 (52.00%)

Alpha Beta Agent vs MAST Agent (25 games):
Alpha Beta Agent wins: 23 (92.00%)
MAST Agent wins: 2 (8.00%)
Draws: 0 (0.00%)
First Mover wins: 15 (60.00%)

Alpha Beta Agent vs AMAF Agent (25 games):
Alpha Beta Agent wins: 25 (100.00%)
AMAF Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 13 (52.00%)

MAST Agent vs Advanced Greedy Agent (25 games):
MAST wins: 13 (52.00%)
Advanced Greedy Agent wins: 12 (48.00%)
Draws: 0 (0.00%)
First Mover wins: 25 (100.00%)

AMAF Agent vs Advanced Greedy Agent (25 games):
AMAF wins: 7 (28.00%)
Advanced Greedy Agent wins: 18 (72.00%)
Draws: 0 (0.00%)
First Mover wins: 19 (76.00%)

real	3m49.574s
user	3m47.337s
sys	0m2.091s
```
### Observations:
* Adv. greedy always out performed simple greedy, which is expected. And both out perform the random agent, which is also expected.
* Alpha-Beta and MCTS both perform extremely well against the simple greedy baseline (as we expected considering they use so much more computational power than the greedy)
* When Alpha-Beta and MCTS were put up against adv. greedy, it was a coin-flip based on whoever moved first (likely implies there's significant first-mover advantage in Qubic)
* Alpha-Beta does much better compared to MCTS head-to-head, but not as much once you add the MAST enhancement to MCTS
* MAST enhancement outperforms AMAF enhancement, which makes sense logically (as explained later)

### Our Tests: The comparisons we made:
- **Baseline models (10,000 trials)**
    - Random vs. Simple Greedy
    - Random vs. Adv. Greedy
    - Simple vs. Adv. Greedy

- **New models against the baseline (100-375 trials)**
    - Alpha-Beta vs. Adv. Greedy
    - Alpha-Beta vs. Simple Greedy
    - MCTS vs. Adv. Greedy
    - MCTS vs. Simple Greedy

- **Head-to-head (100-375 trials)**
    - Alpha-Beta vs. MCTS 
    - Alpha-Beta vs. MAST
    - Alpha-Beta vs. AMAF

- **Comparing MAST to AMAF enhancements (100-375 trials) (explored in Part 2.)**
    - MAST vs. Adv. Greedy
    - AMAF vs. Adv. Greedy

*because MCTS/Alpha-Beta takes so long to run, we opted for less trials

### Our Tests: The trials we ran: 
- 3 depth, 0.25s, 25 games: 5 min (quick!)
- 3 depth, 0.50s, 100 games: ~30 min
- 3 depth, 1.00s, 375 games ~3 hrs

### Results 1a: "quick" 30 min testing (0.5s time limit each, 3-depth)
```
hjc43@raven:~/cs474/final_proj$ time pypy3 simulate.py 100 0.50
Running simulations with 100 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 114 (1.14%)
Simple Greedy Agent wins: 9886 (98.86%)
Draws: 0 (0.00%)
First Mover wins: 5096 (50.96%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 24 (0.24%)
Advanced Greedy Agent wins: 9976 (99.76%)
Draws: 0 (0.00%)
First Mover wins: 5024 (50.24%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 10000 (100.00%)
Draws: 0 (0.00%)
First Mover wins: 5000 (50.00%)

Alpha Beta Agent vs Advanced Greedy Agent (100 games):
Alpha Beta Agent wins: 50 (50.00%)
Advanced Greedy Agent wins: 50 (50.00%)
Draws: 0 (0.00%)
First Mover wins: 100 (100.00%)

Alpha Beta Agent vs Simple Greedy Agent (100 games):
Alpha Beta Agent wins: 100 (100.00%)
Simple Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 50 (50.00%)

MCTS Agent vs Advanced Greedy Agent (100 games):
MCTS wins: 49 (49.00%)
Advanced Greedy Agent wins: 51 (51.00%)
Draws: 0 (0.00%)
First Mover wins: 99 (99.00%)

MCTS Agent vs Simple Greedy Agent (100 games):
MCTS wins: 100 (100.00%)
Simple Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 50 (50.00%)

Alpha Beta Agent vs MCTS Agent (100 games):
Alpha Beta Agent wins: 50 (50.00%)
MCTS Agent wins: 50 (50.00%)
Draws: 0 (0.00%)
First Mover wins: 100 (100.00%)

Alpha Beta Agent vs MAST Agent (100 games):
Alpha Beta Agent wins: 77 (77.00%)
MAST Agent wins: 23 (23.00%)
Draws: 0 (0.00%)
First Mover wins: 73 (73.00%)

Alpha Beta Agent vs AMAF Agent (100 games):
Alpha Beta Agent wins: 100 (100.00%)
AMAF Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 50 (50.00%)

MAST Agent vs Advanced Greedy Agent (100 games):
MAST wins: 47 (47.00%)
Advanced Greedy Agent wins: 53 (53.00%)
Draws: 0 (0.00%)
First Mover wins: 97 (97.00%)

AMAF Agent vs Advanced Greedy Agent (100 games):
AMAF wins: 33 (33.00%)
Advanced Greedy Agent wins: 67 (67.00%)
Draws: 0 (0.00%)
First Mover wins: 83 (83.00%)

real	32m57.787s
user	32m45.501s
sys	0m11.862s
```

### Results 1b: More robust testing (like pset4) - 3hrs (1s time, 3-depth)
```
hjc43@peacock:~/cs474/final_proj$ time pypy3 simulate.py 375 1.0
Running simulations with 375 games each...

Random Agent vs Simple Greedy Agent (10,000 games):
Random Agent wins: 133 (1.33%)
Simple Greedy Agent wins: 9867 (98.67%)
Draws: 0 (0.00%)
First Mover wins: 5109 (51.09%)

Random Agent vs Advanced Greedy Agent (10,000 games):
Random Agent wins: 16 (0.16%)
Advanced Greedy Agent wins: 9984 (99.84%)
Draws: 0 (0.00%)
First Mover wins: 5016 (50.16%)

Simple Greedy Agent vs Advanced Greedy Agent (10,000 games):
Simple Greedy Agent wins: 0 (0.00%)
Advanced Greedy Agent wins: 10000 (100.00%)
Draws: 0 (0.00%)
First Mover wins: 5000 (50.00%)

Alpha Beta Agent vs Advanced Greedy Agent (375 games):
Alpha Beta Agent wins: 188 (50.13%)
Advanced Greedy Agent wins: 187 (49.87%)
Draws: 0 (0.00%)
First Mover wins: 375 (100.00%)

Alpha Beta Agent vs Simple Greedy Agent (375 games):
Alpha Beta Agent wins: 375 (100.00%)
Simple Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 188 (50.13%)

MCTS Agent vs Advanced Greedy Agent (375 games):
MCTS wins: 180 (48.00%)
Advanced Greedy Agent wins: 195 (52.00%)
Draws: 0 (0.00%)
First Mover wins: 367 (97.87%)

MCTS Agent vs Simple Greedy Agent (375 games):
MCTS wins: 375 (100.00%)
Simple Greedy Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 188 (50.13%)

Alpha Beta Agent vs MCTS Agent (375 games):
Alpha Beta Agent wins: 357 (95.20%)
MCTS Agent wins: 18 (4.80%)
Draws: 0 (0.00%)
First Mover wins: 206 (54.93%)

Alpha Beta Agent vs MAST Agent (375 games):
Alpha Beta Agent wins: 294 (78.40%)
MAST Agent wins: 81 (21.60%)
Draws: 0 (0.00%)
First Mover wins: 269 (71.73%)

Alpha Beta Agent vs AMAF Agent (375 games):
Alpha Beta Agent wins: 375 (100.00%)
AMAF Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 188 (50.13%)

MAST Agent vs Advanced Greedy Agent (375 games):
MAST wins: 179 (47.73%)
Advanced Greedy Agent wins: 196 (52.27%)
Draws: 0 (0.00%)
First Mover wins: 366 (97.60%)

AMAF Agent vs Advanced Greedy Agent (375 games):
AMAF wins: 176 (46.93%)
Advanced Greedy Agent wins: 199 (53.07%)
Draws: 0 (0.00%)
First Mover wins: 363 (96.80%)

real	183m13.378s
user	182m31.801s
sys	0m37.109s
```

### Observations/Insights:
- Both Alpha-Beta and MCTS beat the simple greedy 100% of the time. However, they only beat the adv. greedy around half the time. 
- Alpha-Beta almost always (95.20% of the time) beat the vanilla MCTS.
- However, with the MAST enhancement, MCTS was only beaten 78.40% of the time by Alpha-Beta
- First mover advantage is strong. In the trials against the adv. greedy (outside of simple vs. adv. greedy because those two are unevenly matched), the first mover won almost 100% of the time.

### Why is advanced greedy performing so well here?
One possible explanation is that advanced greedy runs the same heuristic as the Alpha-Beta agent. The only difference is that it does it only to a depth of 1 and does not prune any searches. In other words, it's running minimax to a depth of 1. Perhaps this is also a reflection of how strong the static evaluator heuristic that we used.

### First-mover advantage
As observed, the first mover won almost 100% of the time in the trials of {MCTS (+ its enhancements), Alpha-Beta} against the adv. greedy. This aligns with our initial hypothesis that player move order matters, and also aligns with Tic-Tac-Toe theory.

Maybe we can use this knowledge and tune P2's heurisitic to focus more on forcing a draw (i.e. 'blocking' opponent n-in-a-rows) rather than going for a win because we know that it starts at an inherent disadvantage.

### Why is MCTS performing worse than Alpha-Beta here?
We corroborate the same results as when you run the quick ~4 min test. Alpha-Beta has a better pruning step than MCTS and considering how big the state-size is, it means it can search more move possibilities in the limited computational time that we have. MCTS had to be limited to 0.5s for it to run in a reasonable time. Based on our testing/tuning, it would take a search time of roughly 5s or more for it to be competitive with Alpha-Beta (i.e. MCTS wins 20-30% of the time). But that also requires a large trade-off in terms of time and computational power. 

To support this, observe how in the 0.5s time limit run, vanilla MCTS has a 98% win rate against advanced greedy. However, in the 1.0s time limit run, we see that MCTS comes out with a 100% win rate against advanced greedy. This is an indicator that a longer search time for MCTS results in better-selected moves. We wonder how much better it could get if we had more computational resources available.

This is also what we originally hypothesized in our video presentation, so it's also reassuring to see the data back up our theoretical assumptions.

A follow-up question is: if MCTS performs worse than Alpha-Beta, what enhancements to it work best? That leads us to part 2 of our study.


## PART 2: EXPLORATION OF MCTS ENHANCEMENTS
After finding out Alpha-Beta and MCTS had similar-ish results (compared to the greedy agents) but Alpha-Beta out-performed MCTS head-to-head, we decided to further explore MCTS and how the different enhancements might affect it?

Recall from above (part 1) that Alpha-Beta almost always beat the vanilla MCTS (Alpha-Beta won 95.20% of the time). However, with the MAST enhancement, MCTS was only beaten 78.40% of the time by Alpha-Beta. Clearly, the MAST enhancement is beneficial to MCTS in the context of Qubic. But why is that? And how do the other enhancements stand up to that? These questions are the foundation of the following two experiments:

We decide to use 2.0s for the time limit of MCTS because now that we're just focusing on MCTS, we want the runs of it to be as thorough as possible, even if that means sacrificing some runtime. 

### Results 2a: when we 50 trials (2s time limit, 3-depth)
```
hjc43@raven:~/cs474/final_proj$ time pypy3 simulate.py 50 2.0
Running simulations with 50 games each...

MCTS Agent vs Advanced Greedy Agent (50 games):
MCTS wins: 21 (42.00%)
Advanced Greedy Agent wins: 29 (58.00%)
Draws: 0 (0.00%)
First Mover wins: 46 (92.00%)

MAST Agent vs Advanced Greedy Agent (50 games):
MAST wins: 22 (44.00%)
Advanced Greedy Agent wins: 28 (56.00%)
Draws: 0 (0.00%)
First Mover wins: 47 (94.00%)

AMAF Agent vs Advanced Greedy Agent (50 games):
AMAF wins: 16 (32.00%)
Advanced Greedy Agent wins: 34 (68.00%)
Draws: 0 (0.00%)
First Mover wins: 41 (82.00%)

real	18m44.628s
user	18m34.802s
sys	0m9.287s
```

### Results 2b: and when we ran 125 trials (2s time limit, 3-depth):
```
hjc43@raven:~/cs474/final_proj$ time pypy3 simulate.py 125 2.0
Running simulations with 125 games each...

MCTS Agent vs Advanced Greedy Agent (125 games):
MCTS wins: 61 (48.80%)
Advanced Greedy Agent wins: 64 (51.20%)
Draws: 0 (0.00%)
First Mover wins: 123 (98.40%)

MAST Agent vs Advanced Greedy Agent (125 games):
MAST wins: 62 (49.60%)
Advanced Greedy Agent wins: 63 (50.40%)
Draws: 0 (0.00%)
First Mover wins: 124 (99.20%)

AMAF Agent vs Advanced Greedy Agent (125 games):
AMAF wins: 41 (32.80%)
Advanced Greedy Agent wins: 84 (67.20%)
Draws: 0 (0.00%)
First Mover wins: 103 (82.40%)

real	45m52.793s
user	45m33.418s
sys	0m18.647s
```

### Observations:
- MAST does on par with MCTS when the search time per move is adequately high (2s in our case)
- MAST outperforms AMAF when compared to the adv. greedy agent. (49.6% win rate vs. 32.80%)

### Does this make sense? Why does MAST perform better than AMAF?

These results make sense logically because AMAF (with RAVE) is not really built for Qubic. Move order is highly critical, making the AMAF assumption that moves have similar values regardless of when they're played potentially misleading.

Move Averaging Sampling Technique (MAST), on the other hand, learns to bias moves that are better (i.e. taking the corners or centers). It can potentially rapidly identify generally good moves, leading to faster convergence on optimal play. One drawback, though, is that it tends to favor games with a larger state space, so that it can adequately update its global statistics for move rewards to a useful level.

As a result, we shouldn't expect it to perform the vanilla MCTS by too much (once we are running with an adequate time-limit, which 2s meets). We see this in (2b) when MAST has the same win rate as MCTS and in (2a) when it differs by only 2%. 

## PART 3: HOW DOES DEPTH AFFECT ALPHA-BETA RESULTS?
Our advanced greedy agent follows the same heuristic used in Alpha-Beta, but just to a depth of 1. Essentially, it is minimax performed at a depth of 1. That said, it had surprisingly competitive results against both the MCTS and Alpha-Beta agents in part 1. The only difference that determined who would win seemed to be who had the first-move. 

Beyond this apparent first-mover advantage, we wanted to investigate how different depths would perform against each other. Could a higher depth eventually mitigate any first-mover advantage? Our results are below:
```
hjc43@raven:~/cs474/final_proj$ time pypy3 simulate.py 100
Running simulations with 100 games each...

Alpha Beta Depth-5 Agent vs Alpha Beta Depth-3 Agent (100 games):
Alpha Beta Depth-5 Agent wins: 100 (100.00%)
Alpha Beta Depth-3 Agent wins: 0 (0.00%)
Draws: 0 (0.00%)
First Mover wins: 50 (50.00%)

real	10m51.572s
user	10m49.723s
sys	0m1.676s
```
### Observations
A depth of 5 resulted in a substantially better performing agent compared to depth of 3, at least in a head-to-head comparison format.

This makes sense, as a depth of 5 has an exponentially larger search space than depth of 3, and would thus search everything from depth of 3 plus more. This means, it should be able to find all the same moves as depth of 3, and better!

The limit to having a super large depth is simply having the computational resources available. A simple 3-depth vs. 3-depth comparison at 100 games would only take 1 min to run. This 5-depth vs. 3-depth comparison took 10x that duration at almost 11 mins.

<!-- 
## PART 3: SURPRISINGLY THERE HAVEN'T BEEN ANY DRAWS -- BUT WHAT IF ALPHA-BETA PLAYS AGAINST ITSELF?
We noticed that we didn't get any draws yet, which we thought was odd considering that normal Tic-Tac-Toe should always end in a draw. Maybe this was because our agents just had varying levels of skill. To test this, we ran Alpha-Beta against itself. 

```
hjc43@raven:~/cs474/final_proj$ pypy3 simulate.py 100 
Running simulations with 100 games each...

Alpha-Beta Agent vs Alpha-Beta (100 games):
Alpha-Beta P1 wins: 100 (100.00%)
Alpha-Beta P2 wins: 0 (0.00%)
Draws: 0 (0.00%)
```
### Observations
Clear first-move advantage here, just like in Tic-Tac-Toe. We assume that based on how our search-depth works, moving first just always leads to a win — it's hard for P2 to defend as well with our heuristic (?). Maybe in the future, we can test how how much we should weight the opponents static eval score so that we can induce more "defensive-blocking" behavior? -->

## NEXT STEPS?
- Run our code/simulations with an even longer MCTS time on a more powerful system -- because theoretically, MCTS should converge to minimax.
- Try other MCTS enhancements like parallelism. As Prof. Glenn said, parallelism isn't the best in Python, which is why we opted to not include it for our project.
- Tune the static evaluator to be better. Right now, we have an (n+1)-in-a-row being weighted as 10x better than a n-in-a-row, but is this the most optimal value? If we did more testing, maybe our heuristics could improve.
- We didn't see any draws. Why is that? Investigate this further by maybe tuning P2's agent to not necessarily play for a win but rather for a draw (like how it is in game theory optimal Tic-Tac-Toe)
