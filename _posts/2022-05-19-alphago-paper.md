---
layout: post
title: "Understanding AlphaGo"
author: "Chandra Gummaluru"
---

Go is a 2-player strategic board game played in which the aim is to sorround the most territory. It is played on a grid of $N \times N$ points. Players take turns placing stones on the board. There are two basic rules for how stones may be placed:

1. a stone may only remain on the board if it is vertically/horizontally adjacent to an unoccupied point (called a liberty) or vertically/horizontally adjacent to a stone that is; stones without libterties are removed.
2. during his/her turn, a player can place a stone at any occupied point, except for those that would result in a previous board configuration

![]([https://upload.wikimedia.org/wikipedia/commons/6/6e/Go_capturing.png](https://github.com/chandra-gummaluru/chandra-gummaluru.github.io/raw/master/media/go/gif_stone_capture.gif))
*White plays a stone causing black's stones to have no liberties. Thus, black's stones are removed.*
