---
layout: post
title: "What is Lebesgue Integration?"
author: "Chandra Gummaluru"
---
### The Reimann Integral and its Problems

Suppose we have a function, $f: \mathbb{R} \rightarrow \mathbb{R}$ for which we seek the area under its graph within an interval, $[a,b]$. We will denote this quantity as $\int_{a}^{b}f(x)dx$.



To do this, we pick $n$ points $x_1, \dots, x_n \in [a,b]$, so that $a = x_1 < x_2 < \dots < x_{n-1} < x_{n} = b$. The expression,
\\[
\sum_{i=1}^{n-1}(x_{i+1}-x_i)\inf_{x \in [x_i,x_{i+1}]}f(x)
\\]
is called the lower-sum, and it under-approximates the desired area. Similarly, the expression
\\[
\sum_{i=1}^{n-1}(x_{i+1}-x_i)\sup_{x \in [x_i,x_{i+1}]}f(x)
\\]
is called the upper-sum and it over-estimate the desired area. As $n$​ grows  large, both of these approximations get better. Thus, if we can show that both approximations approach the same value in the limit the area can be defined as follows:
\\[
\int_{a}^{b}f(x)dx := \sum_{i=1}^{n-1}(x_{i+1}-x_i)\inf_{x \in [x_i,x_{i+1}]}f(x) = \sum_{i=1}^{n-1}(x_{i+1}-x_i)\sup_{x \in [x_i,x_{i+1}]}f(x)
\\]
This is called the **Reimann integral**. The problem is that both approximations need not always approach the same value even if the area under seems intuitive. For example, consider a function, $I_{\mathbb{Q}}$, defined so that
\\[
I_{\mathbb{Q}}(x) = \begin{cases}
1, x \in \mathbb{Q} \\\\\\
0, \text{ otherwise}
\end{cases}
\\]
Intuitively, we expect the area to be zero since $\mathbb{Q}$ is countably infinite. Every sub-interval of $[a,b]$, where $a \neq b$ contains at least one irrational number, and so, the lower-sum is indeed always zero. However, since $\mathbb{Q}$ is dense, any sub-interval of $[a,b]$ will contain at least one rational number, and so, the upper-sum is always one. Thus, the Reimann integral does not exist.

### Measuring Sets

Suppose we have a non-empty set $\Omega$. We would like to measure its subset, $\Sigma$, of its subsets. We will refer to such subsets as **measurable** subsets. We expect a few properties to hold:

1. $\Omega$ is measurable, i.e., $\Omega \in \Sigma$ 
2. if $A$ is measurable, then $\Omega \setminus A$ is measurable, i.e., $A \in \Sigma \Rightarrow (\Omega \setminus A) \in \Sigma$
3. if $\lbrace A_i \rbrace$ are measurable, then $\cup_{i}A_i$ is measurable, i.e.
\\[A_1,A_2,\dots \in \Sigma \Rightarrow \bigcup_{i}A_i \in \Sigma\\]
5. if $\lbrace A_i \rbrace$ are measurable, then $\cap_i A_i$ is measurable, i.e.,
\\[A_1,A_2,\dots \in \Sigma \Rightarrow \bigcap_{i}A_i \in \Sigma\\]

Intuitively, these properties mean ensure that combining measurable sets results in a measurable set. If $\Sigma$ satisfies these properties, we call it a **$\sigma$-algebra**. Obviously (1) and (2) imply that $\emptyset \in \Sigma$. It also turns out that (2) and (3) imply (4). Thus, (4) is often not explicitly stated.

The tuple, $(\Omega, \Sigma)$ is called a **measurable space**. We can now define a measure, $\mu: \Omega \rightarrow \mathbb{R}$. Again, we expect a few intuitive properties to hold:

1. the measure of the empty-set is zero, i.e., $\mu(\emptyset) = 0$
2. the measure of the union of *disjoint* sets is the sum of the measures of the individual sets, i.e.,
\\[\mu\left(\bigcup_{i}A_i\right) = \sum_{i}\mu(A_i)\\]
