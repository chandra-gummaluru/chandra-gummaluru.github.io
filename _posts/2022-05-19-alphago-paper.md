---
layout: post
title: "Understanding AlphaGo"
author: "Chandra Gummaluru"
---

## The Game of Go
Go is a 2-player strategic board game in which the aim is to sorround the most territory. It is played on a grid of $N \times N$ points. Players take turns placing stones, one at a time, on the board:

- the unoccupied points that are orthogonally adjacent to a stone are called its "liberties"

- orthogonally adjacent stones of the same colour are called a "chain"; chains share liberties 

- if a chain encloses a set of points, those points form a "territory"

.
![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/liberties_chains_territories.svg)
*Black has a chain of length 3 with 6 liberties, White has a chain of length 1 with 3 liberties.*

Whenever a player places a stone on the board, any stone without liberties is captured and consequently removed from the board.
![](https://raw.githubusercontent.com/chandra-gummaluru/chandra-gummaluru.github.io/master/media/go/stone_capture.svg)
*White places a stone causing BLack's stones to have no liberties. Thus, black's stones are captured and removed.*

In general, players may place stones anywhere on the board unless, except when doing so would return the board to a previously encountered configuration.
![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/cyclic_stone.svg)
*Black places a stone capturing one of White's pieces. White can no longer play at the highlighted point since this would return the board back to the state before Black played.*

A player need not place a stone during their turn. If both players skip their turn, or neither player can legally place a stone, the game ends. The score for each player is the number of points within their territories plus the number of stones they captured.

## The Goal of AlphaGo
Our goal of AlphaGo was to develop an agent that can decide the best move to play from any board configuration in the sense that its choice maximizes the probability that it will win. Given some initial board configuration, $s_0$, we can represent all potential games as a tree:

![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/go_tree.svg)
*The root of the tree represents the initial board configuration. Each leaf of the tree represents the board configuration after a game has ended. Each path from the root to a leaf represents one possible realization of the game; the leaf is annotated with a utility value of either $1$ or $0$, depending on whether the agent would have won or not if that game was indeed realized.*

In developing our agent, it is fairly common to assume that the adversary will also play the move that will maximize their probability of winning.
