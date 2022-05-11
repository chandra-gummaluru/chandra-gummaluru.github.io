---
layout: post
title: "What is Lebesgue Integration?"
author: "Chandra Gummaluru"
---

Suppose we have a function, $f: \mathbb{R} \rightarrow \mathbb{R}$, such as the one shown below, and we wish to find its area under its graph within the interval, $[a,b]$.

The traditional way to do this isto choose $n$ points $x_1, \dots, x_n \in [a,b]$, so that $a = x_1 < x_2 < \dots < x_{n-1} < x_{n} = b$. Then, the sum,
\[\sum_{i}(x_{i+1}-x_i)\inf_{x \in [x_i, x_{i+1}]}f(x)\]
is an under-estimate of the area and
\[\sum_{i}(x_{i+1}-x_i)\sup_{x \in [x_i, x_{i+1}]}f(x)\]
is an over-estimate of it.
