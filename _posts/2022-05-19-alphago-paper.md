---
layout: post
title: "Understanding AlphaGo"
author: "Chandra Gummaluru"
---

## The Game of Go
Go is a 2-player strategic board game in which the aim is to sorround the most territory. It is played on a grid of $N \times N$ points. Players take turns placing stones, one at a time, on the board:

- the unoccupied points that are vertically/horizontally adjacent to a stone are called its "liberties"

- vertically/horizontally adjacent stones of the same colour are called a "chain"; chains share liberties 

- if a chain encloses a set of points, those points form a "territory"

Whenever a player places a stone on the board, any stone without liberties is captured and consequently removed from the board.
![](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/gif_stone_capture.gif)
*White plays a stone causing black's stones to have no liberties. Thus, black's stones are removed.*

In general, players may place stones anywhere on the board unless, exceptwhen doing so would return the board to a previously encountered configuration.

A player need not place a stone during their turn. If both players skip their turn, or neither player can legally place a stone, the game ends. The score for each player is the number of points within their territories plus the number of stones they captured.

## The Goal of AlphaGo
Our goal of AlphaGo was to develop an algorithm that can decide the best move to play from any board configuration. 
