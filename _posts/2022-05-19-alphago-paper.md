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
The game is represented mathematically as a tuple, $(\mathcal{S}, \mathcal{T}, A, u)$, where:
- $\mathcal{S}$ is a set of **states**
- $\mathcal{T} \subseteq \mathcal{S}$ is the subset of the states in which the game ends, called **terminal states**
- $A$ is a set-valued function such that $A(s)$ is the set of feasiable **actions** from state, $s \in \mathcal{S}$
- $u: \mathcal{T} \rightarrow \lbrace 0, 1\rbrace$ is a **utility function**, defined so that $u(s) = 1$ if $s$ is a winning state for our agent, and $u(s) = 0$ otherwise.

Each state, $s \in \mathcal{S}$ represents a board configuration and a player, called the **turn-taker**. When an action, $a \in A(s)$ is played by the turn-taker, the result is a new state, $a(s) \in \mathcal{S}$, which is called a **successor** of $s$. The set of all successors of $s$ is $S(s) = \left\lbrace a(s), a \in A(s) \right\rbrace$.

## The Goal of AlphaGo
The goal of AlphaGo was to develop an agent that can decide the best move to play from any board configuration in the sense that its choice maximizes the probability that it will win. Mathematically, we seek a policy function, $p: \mathcal{S} \rightarrow \mathcal{A}$ such that $p(s)$ is the action which maximizes the probability that $u = 1$ when a terminal state is reached.

Given some initial board configuration, $s_0$, we can represent all potential games as a tree:

![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/go_tree.svg)
*The root of the tree, $s_0$, represents the initial board configuration. Each leaf of the tree represents the board configuration after a game has ended. Each path from the root to a leaf represents one possible realization of the game; the leaf is annotated with a utility value of either $1$ or $0$, depending on whether the agent would have won or not if that game was indeed realized.*

When developing an agent, it is fairly common to assume that the adversary will also play the move that will maximize their probability of winning. In other words, the adversary will always play a move that causes our agent to lose over one that causes our agent to win. Similarly, our agent should always play a move that causes it to win over one that causes it to lose. Thus, the utility of non-terminal states is determinisitc and can be computed via the following recurrence:

\\[u(s) = \begin{cases}
\displaystyle\max_{s' \in S(s)}\lbrace u(s') \rbrace, \text{ if our agent is the turn-taker} \\\\\\
\displaystyle\min_{s' \in S(s)}\lbrace u(s') \rbrace, \text{ otherwise.}
\end{cases}\tag{1}\label{eq_mm_recurrence}\\]

To compute these utilities, the agent must traverse the tree until a state, $s$, is reached whose successors are all leaves. Then, using $\ref{(eq_mm_recurrence)}$, the agent can compute $u(s)$ working back up the tree.  
