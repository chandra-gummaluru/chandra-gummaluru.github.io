---
layout: post
title: "Understanding AlphaGo"
author: "Chandra Gummaluru"
---

## The Game of Go
Go is a 2-player strategic board game in which the aim is to surround the most territory. It is played on a grid of $N \times N$ points. Players take turns placing stones, one at a time, on the board:

- the unoccupied points that are orthogonally adjacent to a stone are called its "liberties"

- orthogonally adjacent stones of the same colour are called a "chain"; chains share liberties 

- if a chain encloses a set of points, those points form a "territory"

.
![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/liberties_chains_territories.svg)
*Black has a chain of length 3 with 6 liberties, White has a chain of length 1 with 3 liberties.*

Whenever a player places a stone on the board, any stone without liberties is captured and consequently removed from the board.
![](https://raw.githubusercontent.com/chandra-gummaluru/chandra-gummaluru.github.io/master/media/go/stone_capture.svg)
*White places a stone causing Black's stones to have no liberties. Thus, black's stones are captured and removed. Whtie then has a territory of size 2.*

In general, players may place stones anywhere on the board except where doing so would return the board to a previously encountered configuration.
![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/cyclic_stone.svg)
*Black places a stone capturing one of White's pieces. White can no longer play at the highlighted point since this would return the board back to the state before Black played.*

A player need not place a stone during their turn. If both players skip their turn, or neither player can legally place a stone, the game ends. The score for each player is the number of points within their territories plus the number of stones they captured.

## Mathematical Representation
The game is represented mathematically as a tuple, $(\mathcal{S}, \mathcal{T}, \mathcal{A}, u)$, where:
- $\mathcal{S}$ is a set of **states**
- $\mathcal{T} \subseteq \mathcal{S}$ is the subset of the states in which the game ends, called **terminal states**
- $\mathcal{A}$ is a set-valued function such that $\mathcal{A}(s)$ is the set of feasiable **actions** from state, $s \in \mathcal{S}$
- $u: \mathcal{T} \rightarrow \lbrace -1, 0, 1\rbrace$ is a **utility function**, defined so that $u(s) = 1$ if $s$ is a winning state for our agent, $u(s) = -1$ if $s$ is a losing state for our agent, and $u(s) = 0$ if $s$ is a tie state.

Each state, $s \in \mathcal{S}$ includes the board configuration and the player whose turn it is. When an action, $a \in \mathcal{A}(s)$ is played by the turn-taker, the result is a new state, $a(s) \in \mathcal{S}$, which is called a **successor** of $s$. The set of all successors of $s$ is $\mathcal{S}(s) = \left\lbrace a(s), a \in \mathcal{A}(s) \right\rbrace$.

## The Goal of AlphaGo
The goal of AlphaGo was to develop an agent that can decide the best move to play from any board configuration in the sense that its choice maximizes the probability that it will win. Mathematically, we seek a policy function, $p: \mathcal{S} \rightarrow \mathcal{A}$ such that $p(s)$ is the action which maximizes the probability that $u = 1$ when a terminal state is reached.

Given some initial state, $s_0$, we can represent all possible realizations of the game from that state as a tree whose nodes represent states and edges represent actions:

![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/go_tree.svg)
*Each node in the tree is coloured according to the turn-taker in the associated state. The root of the tree, $s_0$, represents the initial state. Each leaf of the tree represents the state once a game has ends. Each path from the root to a leaf represents one possible realization of the game from $s_0$; the leaf is annotated with a utility value of either $-1$, $0$, or $1$, depending on whether the agent would have won, lost, or tied, if that game was indeed realized.*

When developing an agent, it is fairly common to assume that the adversary will also play the move that will maximize their probability of winning. In other words, the adversary will always play a move that causes our agent to lose over one that causes our agent to win. Similarly, our agent should always play a move that causes it to win over one that causes it to lose. Thus, the utility of non-terminal states is determinisitc and can be computed via the following recurrence:

\\[u(s) = \begin{cases}
\displaystyle\max_{s' \in S(s)}\lbrace u(s') \rbrace, \text{ if our agent is the turn-taker} \\\\\\
\displaystyle\min_{s' \in S(s)}\lbrace u(s') \rbrace, \text{ otherwise.}
\end{cases}\tag{1}\label{eq_mm_recurrence}\\]

To compute these utilities, the agent must traverse the tree until a state, $s$, is reached whose successors are all leaves. Then, using $\ref{(eq_mm_recurrence)}$, the agent can compute $u(s)$ working back up the tree.

<img src="https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/minmax_search.gif"/>*Computing utilities via the min-max algorithm on a binary game tree of depth 3.*

A big problem with the min-max algorithm is that the agent must traverse the entire tree to compute the utility of the root. With Go, this is computationally infeasible because the tree is so large. In these situations, one option is to use an iterative approach. To do this, we will need a heuristic function, $h: \mathcal{S} \rightarrow \mathbb{R}$ that can estimate $u$ for any $s \in \mathcal{S}$. In each iteration, $i$, we expand a node in the tree, estimate its utility using the heuristic, and propagate the consequences back up the tree via the min-max algorithm.

<img src="https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/minmax_search_heur.gif"/>*Running the min-max algorithm iteratively on a binary game tree of depth 3. In each iteration, $i$, the agent selects and expands a part of the tree, estimates its utility via $h$, and then propagates the consequences back up the tree. It also keeps track of the best successor found thus far so that if time runs out, it can play the action that yields that successor.*

The assumption here is that the estimate from $h$ gets closer to $u$ as $s$ gets closer to a terminal state. This is why it is still useful to search the tree despite being able to compute $h$ for any $s \in \mathcal{S}$.

Finding a good $h$ is very difficult and even if could, there is no obvious way to select which part of the tree should be explored further if we have time to run another iteration.

![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/minmax_ee.svg)
*In this case, $s_2$ has a lower estimated utility than $s_1$, but we are more confident in the estimate for $s_1$ since it was based on deeper exploration. If we had enough time to explore the tree further, we could either explore $s_1$ more since it is more likely to be a good state, or we could explore $s_2$ since we haven't explored it as much and thus, could potentially be much better.*

This is called the **exploration versus exploitation dilemma**.

## Monte-Carlo Tree Search
It turns out that we can simultaneously resolve the exploration versus exploitation dilemma and remove the need for a heuristic function at the same time using a technique called **Monte-Carlo Tree Search** (MCTS).

Suppose we had a simulation policy function, $p: \mathcal{S} \times A \rightarrow \mathcal{A}$ so that $p(s,a)$ is the probability that the turn-taker chooses the action, $a$ from state, $s$. Under perfect play, we would expect:

\\[p(s,a) = p\^*(s,a) := \begin{cases} 1, \text{ if } a = A\^*(s) \\\\\\ 0, \text{ otherwise}\end{cases}\\]

where $A^*(s) = \text{arg max}_{a \in \mathcal{A}(s)}\lbrace u(s) \rbrace$. However, $p$ may model imperfect play or be an inaccurate model of perfect play.

In any case, we can then estimate the utility of a state, $s$, by repeatedly simulating the game from that state using $p$. If $\mu(s,n)$ is the utility obtained after the $n$th simulation, then an estimate for $u(s)$ after $N_s$ simulations is

\\[\hat{u}(s,N_s) = \frac{\sum_{n=1}^{N_s}\mu(s,i)}{N_s}.\\]

If $p \equiv p^*$, then $\hat{u}(s,N_s) = u(s)$ for any $N$. Otherwise, we can upper bound the probability that difference between $\hat{u}(s,N_s)$ and $\mu(s)$ exceeds some threshold, $\varepsilon$ using Hoeffding's inequality:

\\[\text{Pr}\left\lbrace |\hat{\mu}(i,N_s) - \mu(s)| \geq \varepsilon \right\rbrace \leq \exp\left\lbrace \frac{-N_s\varepsilon^2}{2} \right\rbrace\tag{2}\\]

Setting the right side of (2) to equal $\delta$ and solving for $\varepsilon$ yields

\\[\varepsilon = \sqrt{-\frac{\log{\delta}}{N_s}} := \text{CR}_\{\delta\}\left(\hat{u}(s,N_s)\right)\\]

which we call the $\delta$ **confidence radius** of $\hat{\mu}(s,N_s)$. Intuitively, $\hat{\mu}(s,N_s)$ is at most $\text{CR}_{\delta}\left(\hat{\mu}(s,N_s)\right)$ away from $\mu(s)$ with probability $\delta$.

## The AlphaGo Pipeline
Conventionally, MCTS is used where $p$ is uniform, i.e., we have no knowledge of how good moves are aprori. However, AlphaGo uses a simulation policy that has been learned via a dataset of expert moves, and refined using self-play reinforcement learning. Moreover, instead of estimating $\hat{u}(s,N_s)$ as sample mean of simulation results, it also 


The techniques used by AlphaGo are fairly standard; the novelity is in how these techniques are combined. The appraoch can be summarized as follows:

1. Using supervised learning, a model, $\rho$, is trained to predict the distribution of made by expert Go players for any given board configuration.
2. Through self-play reinforcement learning, $\rho$ is refined.
3. 

### Training the Value-Function
To compute the value-function, the authors began with an initial estimate of it. For now,  

### Initializing the Value-Function
The first goal of AlphaGo was to decide on an initial value-function, $h: \mathcal{S} \rightarrow \mathbb{R}$. Of course, one could pick any arbitrary function. However,  
