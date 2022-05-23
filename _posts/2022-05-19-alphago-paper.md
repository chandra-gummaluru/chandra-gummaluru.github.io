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
- $\mu: \mathcal{T} \rightarrow \lbrace -1, 0, 1\rbrace$ is a **utility function**, defined so that $\mu(s) = 1$ if $s$ is a winning state for our agent, $\mu(s) = -1$ if $s$ is a losing state for our agent, and $\mu(s) = 0$ if $s$ is a tie state.

Each state, $s \in \mathcal{S}$ includes the board configuration and the player whose turn it is. When an action, $a \in \mathcal{A}(s)$ is played by the turn-taker, the result is a new state, $a(s) \in \mathcal{S}$, which is called a **successor** of $s$. The set of all successors of $s$ is $\mathcal{S}(s) = \left\lbrace a(s), a \in \mathcal{A}(s) \right\rbrace$.

We can model the behaviour of the players using a probability distribution, $p: \mathcal{S} \times \mathcal{A} \rightarrow [0,1]$, where $p(a\lvert s)$ is the probability that the turn-taker chooses action, $a$, from state, $s$. The possible realizations of the game from $s$ can be represented using a tree as a tree where each node represents a state and each edge represents an action (chosen according to $p$):

![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/go_tree.svg)
*Each node in the tree is coloured according to the turn-taker in the associated state. The root of the tree, $s_0$, represents the initial state. Each leaf of the tree represents the state once a game has ends. Each path from the root to a leaf represents one possible realization of the game from $s_0$; the leaf is annotated with a utility value of either $-1$, $0$, or $1$, depending on whether the agent would have won, lost, or tied, if that game was indeed realized.*

Let $u(s_0)$ be the utility obtained by a specific realization of the game from some initial state $s_0$; its value is stochastic. The goal is to develop an agent that can decide the best action $a^\*(s_0)$, to play from $s_0$, in the sense that its choice maximizes its expected utility over all possible realizations, i.e.,
\\[a^*(s) = \text{arg max}_{a \in \mathcal{A}(s)}\text{Ev}\lbrace u(a(s)) \rbrace, s \not\in \mathcal{T}\\]

where $\text{Ev}\lbrace u(s) \rbrace$ can be computed via the recurrence:

\\[\text{Ev}\lbrace u(s) \rbrace = \begin{cases} \displaystyle\mu(s), s \in \mathcal{T} \\\\\\
\displaystyle\sum_{a \in \mathcal{S}}p(a\lvert s)\text{Ev}\lbrace u(a(s)) \rbrace. s \not\in \mathcal{T} \end{cases}\\]
## Brute-Force Search Techniques
An obvious approach is to saearch the game tree explicitly for the best action during live play.
### The Ideal Algorithm
Whenever our agent is the turn-taker at $s$, we want $p(\cdot \lvert s)$ to satisfy:

\\[p(a\lvert s) = \begin{cases} 1, a=a^*(s) \\\\\\
0, \text{otherwise}
\end{cases}\tag{1}\\]

This leads to the following recurrence for computing $\text{Ev}\lbrace u(s) \rbrace$:

\\[\begin{aligned}\text{Ev}\lbrace u(s) \rbrace = \begin{cases}
\displaystyle \mu(s), &s \in \mathcal{T} \\\\\\
\displaystyle\max_{s' \in S(s)}\lbrace \text{Ev}\lbrace u(s') \rbrace \rbrace, & s \not\in \mathcal{T} \text{ and our agent is the turn-taker}\\\\\\
\displaystyle\sum_{a \in \mathcal{A}(s)}p(a|s)\text{Ev}\lbrace u(a(s)) \rbrace, & s \not\in \mathcal{T} \text{ and the adversary is the turn-taker}
\end{cases}\end{aligned}\tag{EM}\label{eq_em_recurrence}\\]

This is called the **expected-max** algorithm.

### Dealing with an Unknown Adversary
In most cases, we do not know $p(\cdot \lvert s)$ if the adversary is the turn-taker at $s$. Thus, it is often common to assume that the adversary plays perfectly, i.e., (1) is satisfied for all $s$, not just when our agent is the turn-taker. In these cases, (EM) reduces to:

\\[\begin{aligned}u(s) = \begin{cases}
\displaystyle \mu(s), &s \in \mathcal{T} \\\\\\
\displaystyle\max_{s' \in S(s)}\lbrace u(s') \rbrace, &s \not\in \mathcal{T} \text{ and our agent is the turn-taker} \\\\\\
\displaystyle\min_{s' \in S(s)}\lbrace u(s') \rbrace, &s \not\in \mathcal{T} \text{ and the adversary is the turn-taker}
\end{cases}\end{aligned}\tag{MM}\label{eq_mm_recurrence}\\]

where the expectations are no longer necessary since $u$ is effectively deterministic. This is called the **min-max** algorithm.

To compute the utilities. the agent must traverse the tree until a state, $s$, is reached whose successors are all leaves, and then compute $\text{Ev}\lbrace u(s) \rbrace$ by working back up the tree.

<img src="https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/minmax_search.gif"/>*Computing utilities via the min-max algorithm on a binary game tree of depth 3.*

### Dealing with Large Game Trees
In many situations, it is computationally infeasible to traverse the entire game tree because it is so large. This is the case with Go. In these situations, one option is to use an iterative approach. To do this, we will need a heuristic function, $h: \mathcal{S} \rightarrow \mathbb{R}$ that can estimate $u$ for any $s \in \mathcal{S}$. In each iteration, $i$, we expand a node in the tree, estimate its utility using the heuristic, and propagate the consequences back up the tree via the min-max algorithm.

<img src="https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/minmax_search_heur.gif"/>*Running the min-max algorithm iteratively on a binary game tree of depth 3. In each iteration, $i$, the agent selects and expands a part of the tree, estimates its utility via $h$, and then propagates the consequences back up the tree. It also keeps track of the best successor found thus far so that if time runs out, it can play the action that yields that successor.*

The assumption here is that the estimate from $h$ gets closer to $u$ as $s$ gets closer to a terminal state. This is why it is still useful to search the tree despite being able to compute $h$ for any $s \in \mathcal{S}$.

Finding a good $h$ is very difficult and even if we could, there is no obvious way to select which part of the tree should be explored further if we have time to run another iteration.

![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/minmax_ee.svg)
*In this case, $s_2$ has a lower estimated utility than $s_1$, but we are more confident in the estimate for $s_1$ since it was based on deeper exploration. If we had enough time to explore the tree further, we could either explore $s_1$ more since it is more likely to be a good state, or we could explore $s_2$ since we haven't explored it as much and thus, could potentially be much better.*

This is called the **exploration versus exploitation dilemma**.

### Solving the Exploration/Exploitation Dilemma
We can resolve the exploration versus exploitation dilemma and avoid needing an explicit heuristic function at the same time using a technique called **Monte-Carlo Tree Search** (MCTS).

We can then estimate the utility of a state, $s$, by repeatedly simulating the game from that state.

Let $N(s,t)$ denote the number of times a state, $s$ has been visited after the $t$th iteration of MCTS, and $U(s,t)$ denote the cumulative utility obtained.

Each iteration has four phases:

1. **Selection**: Starting from $s_0$, choose actions, $a_1, \dots, a_k$, where $a_{i+1} \in \mathcal{A}(s_i), s_i = a_i(s_{i=1})$ and $s_k$ is the first node with unexplored children; the actions should be chosen according to a selection policy chosen balance exploration versus exploitation.

2. **Expansion**: Expand $s_k$ to reveal a child, $s_{k+1}$, and update $N(s,\cdot)$ so that:
\\[\begin{aligned}N(s,t) = \begin{cases} N(s,t-1) + 1, &s = s_0, \dots, s_k, s_{k+1} \\\\\\
N(s,t-1), &\text{otherwise}\end{cases}\end{aligned}\\]
3. **Simulation**: Simulate a game from $s_{k+1}$ to some terminal state by randomly selecting successive actions; let $s_{k+2}, \dots, s_{n}$ denote the resulting states, where $s_n \in \mathcal{T}$.
4. **Back-Propagation**: For $s = s_0, \dots, s_n$, update $U$ so that $U(s,t) + U(s,t-1) + \mu(s_n)$ and estimate $u(s)$ as
\\[\hat{u}(s,t) = \frac{U(s,t)}{N(s,t)}.\\]

Since $\hat{u}(s,t)$ is the mean of $N(s,t)$ independent random variables bounded within $[-1,1]$, we can use Hoeffding's inequality to upper bound the probability that the difference between $\hat{u}(s,t)$ and $\mu(s)$ exceeds some threshold, $\varepsilon$:

\\[\text{Pr}\left\lbrace \lvert \hat{u}(s,t) - u(s) \rvert \geq \varepsilon \right\rbrace \leq 2\exp\left\lbrace -\frac{N(s,t)\varepsilon^2}{2} \right\rbrace.\\]

We see that as $N(s,t) \rightarrow \infty$, then $\text{Pr}\left\lbrace \lvert \hat{u}(s,t) - u(s) \rvert \geq \varepsilon \right\rbrace \rightarrow 0$ for any $\varepsilon > 0$. In other words, for large $N(s,t)$, we can write $\hat{u}(s,t) \approx u(s)$.

To derive the selection policy, we first set the right side of (2) to equal $\delta$ and solve for $\varepsilon$:

\\[\varepsilon = \sqrt{-\frac{2\log{\delta}}{N(s,t)}} := \text{CR}_\{\delta\}\left(\hat{u}(s,t)\right)\\]

which we call the $\delta$ **confidence radius** of $\hat{u}(s,t)$. Intuitively, the probability that $\hat{u}(s,t)$ is more than $\text{CR}_{\delta}\left(\hat{u}(s,t)\right)$ away from $u(s)$ is at most $\delta$

<img src="https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/conf_rad_graph.svg" width="425"/>*The confidence radius for $\hat{\mu}(s_1, N_{s_1})$ and $\hat{\mu}(s_2, N(s_2))$ when $\delta = 0.9$.*

The $\delta$ **upper confidence bound** of $\hat{u}(s,t)$ is

\\[\text{UCB}_\{\delta\}\left(\hat{u}(s,t)\right) = \hat{u}(s,t) + \text{CR}\_{\delta}\left(\hat{u}(s,t)\right).\\]

We want $\delta$ to get smaller as the number of iterations gets larger. If we let $\delta = t^{-c}$ for some $c \geq 1$ and choose actions according to the selection policy:
\\[\hat{a}(s,t) = \text{arg max}_{a \in \mathcal{A}(s)}\text{UCB}\_{t^{-c}}\left(\hat{u}(s,t)\right) = \text{arg max}\_{a \in \mathcal{A}(s)}\left\lbrace\hat{u}(s,t) + \sqrt{\frac{2c\log t}{N(s,t)}}\right\rbrace,\tag{UCT}\\]
then for large $N(s,t)$, it follows that $\hat{a}(s,t) \approx a^\*(s)$ in the sense that $u(\hat{a}(s,t)) \approx u(a^\*(s))$. We could have also defined the selection policy in terms of the $\delta$ **lower confidence bound**, but ineither case, we see that the action identified by the resulting MTCS will have the same expected utility as the one identified by the min-max algorithm.

## Learning Techniques
A completly different approach is to learn $p$ ahead of time from a family of distributions, $p_w$, where $w$ is a set of weights that we can tune. Obviously, we want to choose $w$ so that $p_w$ approximates $p$ as defined in (1).

### via Supervised Learning
Suppose we have a dataset, $\mathcal{D}$, of $N$ games.

The actions taken during the $n$th game were $a\_1^{(n)}, \dots, a\_{T^{(n)}}^{(n)}$, and the resulting state sequence was $s\_1^{(n)}, \dots, s_\{T^{(n)}}^{(n)}$, where $a\_i^{(n)} \in \mathcal{A}\left(s\_{i-1}^{(n)}\right)$, $a\_i^{(n)}\left(s\_{i-1}^{(n)}\right) = s\_i^{(n)}$, and $s\_{T^{(n)}}^{(n)} \in \mathcal{T}$.

We want to choose $w$ to maximize the probability of the games in $\mathcal{D}$ occurring, i.e.,

\\[\text{Pr}\lbrace \mathcal{D} \rbrace = \sum\_{n=1}^{N}\prod\_{t=1}^{T^{(n)}}p\_w\left(a\_t^{(n)} \lvert s\_{t-1}^{(n)}\right).\\]

A necessary condition for the desired $w$ is that the partial derivative of the above expression w.r.t. $w$ is zero, i.e.,
\\[\nabla_w\text{Pr}\lbrace \mathcal{D} \rbrace = 0.\\]

Computing $\nabla_w\text{Pr}\lbrace \mathcal{D} \rbrace$ is very difficult, so we often maximize $\nabla_w\log\left(\text{Pr}\lbrace \mathcal{D} \rbrace\right)$ instead; the resulting $w$ is the same in both cases, but $\nabla_w\log\left(\text{Pr}\lbrace \mathcal{D} \rbrace\right)$ is easier to compute:

\\[\nabla_w\log\left(\text{Pr}\lbrace \mathcal{D} \rbrace\right) = \frac{1}{N}\sum_{n=1}^{N}\sum_{t=1}^{T^{(n)}}\frac{\partial}{\partial w}\log\left(p_w\left(a_t^{(n)} \lvert s_{t-1}^{(n)}\right)\right).\\]

Solving the above for $w$ is still very difficult, but we can approximate it via an iterative approach:

1. choose an arbitrary $w_0$
2. in each iteration, $i$, select a random subset of $\mathcal{D}$ and compute $\nabla_w\log\left(\text{Pr}\lbrace \mathcal{D} \rbrace\right)$ under $p\_{w_\i}$
3. update $w_{i+1} = w_{i} + \alpha\nabla_w\log\left(\text{Pr}\lbrace \mathcal{D} \rbrace\right)$, where $\alpha$ is some scalar

This is called **gradient ascent**; we should update $w$ in the direction of $\nabla_w\log\left(\text{Pr}\lbrace \mathcal{D} \rbrace\right)$ since this is the direction along which $\text{Pr}\lbrace \mathcal{D} \rbrace$ increases the most.

### via Reinforcement Learning
In many cases, we do not actually have a dataset, $\mathcal{D}$. In this case, we can choose $w$ randomly to begin with and estimate the utility of $s_0$ by simulating $N$ games using $p_w$:

\\[\hat{u}\_N(s\_0) = \frac{1}{N}\sum\_{n=1}^{N}\mu\left(s\_{T^{(n)}}\right)\prod\_{t=1}^{T^{(n)}}p\_w\left(a\_t^{(n)} \lvert s\_{t-1}^{(n)}\right).\\]

Due to the law of large numbers, it can be shown that $\lim\_{N \rightarrow \infty}\hat{\mu}\_N(s\_0) = \text{Ev}\lbrace u(s\_0) \rbrace$. Thus, if $N$ is sufficiently large, $\hat{u}\_N(s\_0)$ is a good estimate of $u(s\_0)$, and we can maximize it instead.

A necessary condition for the desired $w$ is that the partial derivative of the above expression w.r.t. $w$ is zero, i.e.,
\\[\nabla_w\text{Ev}\lbrace \hat{u}\_N(s\_0) \rbrace = 0.\\]

Computing $\nabla_w\text{Pv}\lbrace \hat{u}\_N(s\_0) \rbrace$ is very difficult, so we often maximize $\nabla_w\log\left(\text{Ev}\lbrace \hat{u}\_N(s_0) \rbrace\right)$ instead; the resulting $w$ is the same in both cases, but $\nabla_w\log\left(\text{Ev}\lbrace \hat{u}\_N(s_0) \rbrace\right)$ is easier to compute:

\\[\nabla_w\log\left(\text{Ev}\lbrace \hat{u}\_N(s\_0) \rbrace\right) = \frac{1}{N}\sum_{n=1}^{N}\sum_{t=1}^{T^{(n)}}\frac{\partial}{\partial w}\log\left(p_w\left(a_t^{(n)} \lvert s_{t-1}^{(n)}\right)\right).\\]

Solving the above for $w$ is still very difficult, but we can approximate it via an iterative approach:

1. choose an arbitrary $w_0$
2. in each iteration, $i$, simulate $N$ games under $p\_{w\_i}$ and compute $\nabla_w\log\left(\text{Ev}\lbrace \hat{u}\_N(s\_0) \rbrace\right)$.
3. update $w_{i+1} = w_{i} + \alpha\nabla_w\log\left(\text{Ev}\lbrace \hat{u}\_N(s\_0) \rbrace\right)$, where $\alpha$ is some scalar

This is called **gradient ascent**; we should update $w$ in the direction of $\nabla_w\log\left(\text{Ev}\lbrace \hat{u}\_N(s\_0) \rbrace\right)$ since this is the direction along which $\text{Ev}\lbrace \hat{u}\_N(s\_0) \rbrace$ increases the most.

There is a problem with this approach however. If the adversary is the turn-taker at $s$, then $p\_w(\cdot \lvert s)$ approximates the distribution of the adversary's actions.  Obviously our agent will want $p\_w(\cdot \lvert s)$ to maximize $\hat{u}(s_0)$ but the adversary wishes to minimize this quantity. To fix this, we simply need to introduce d
The problem here is that if we simulate both our agent's actions and its adverary's with $p_w$,

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
