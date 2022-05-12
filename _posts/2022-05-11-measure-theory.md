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
1, x \in \mathbb{Q}\\\\0, \text{ otherwise}
\end{cases}
\\]
Intuitively, we expect the area to be zero since $\mathbb{Q}$ is countably infinite. Every sub-interval of $[a,b]$, where $a \neq b$ contains at least one irrational number, and so, the lower-sum is indeed always zero. However, since $\mathbb{Q}$ is dense, any sub-interval of $[a,b]$ will contain at least one rational number, and so, the upper-sum is always one. Thus, the Reimann integral does not exist.

### Generalizing Integration

Our goal is to generalize the notion of an integral for a function, $f: \Omega \rightarrow \mathbb{R}$,  over some set $R \subseteq \Omega$. If $f$ is bounded, we can pick $n$ points in its range so that $y_1 < \dots < y_n$ and then define the lower-sum as
\\[
\sum_{i=1}^{n-1}f(y_i)\mu(f^{-1}([y_i,y_{i+1}]))
\\]
and the upper-sum as
\\[
\sum_{i=2}^{n}f(y_i)\mu(f^{-1}([y_{i-1},y_{i}]))
\\]
where $f^{-1}([a,b])$ denotes the inverse image of $[a,b]$ under $f$, and $\mu: \Omega \rightarrow \mathbb{R}$ is suppose to measure the size of subsets of $\Omega$.

### Measuring Sets
We need to understand the properties of $\mu$.  Firstly, we note that $\mu$ need not measure *all* subsets of $\Omega$ - it may only need to measure a subset $\Sigma$, of $\Omega$'s subsets. We will refer to such subsets as $\mu$-**measurable** subsets. We expect a few properties to hold:

1. $\Omega$ is measurable, i.e., $\Omega \in \Sigma$ 
2. the complement of a measurable set w.r.t. $\Omega$ is measurable,i.e., $A \in \Sigma \Rightarrow (\Omega \setminus A) \in \Sigma$
3. the union of measurable sets is measurable, i.e.,
\\[A_i \in \Sigma, i \in \mathbb{N} \Rightarrow \bigcup_{i=1}^{\infty}A_i \in \Sigma\\]
5. the intersection of a measurable set is measurable, i.e.,
\\[A_i\in \Sigma, i \in \mathbb{N} \Rightarrow \bigcap_{i=1}^{\infty}A_i \in \Sigma\\]

Intuitively, these properties mean ensure that combining measurable sets results in a measurable set. If $\Sigma$ satisfies these properties, we call it a **$\sigma$-algebra**. Obviously (1) and (2) imply that $\emptyset \in \Sigma$. It also turns out that (2) and (3) imply (4). Thus, (4) is often not explicitly stated.

There are many $\sigma$-algebras for any $\Omega$, and thus, many measure spaces. The largest one is $(\Omega, \mathcal{P}(\Omega))$, where $\mathcal{P}(\Omega)$ denotes the power-set of $\Omega$. Of course, we are often interested in the smallest one. It can be shown that the smallest $\sigma$-algebra of $\Omega$ that contains $M \subseteq \Omega$ is given by
\\[\sigma(\Omega, M) = \bigcap_{\substack{\Sigma \in \sigma(\Omega)\\\\M \subseteq \Sigma}}\Sigma,\\]
where $\sigma(\Omega)$ is the set of all $\sigma$-algebras of $\Omega$.

We can now define a measure, $\mu: \Omega \rightarrow \mathbb{R}$. Again, we expect a few intuitive properties to hold:

1. the measure of the empty-set is zero, i.e., $\mu(\emptyset) = 0$
2. the measure of the union of *disjoint* sets is the sum of the measures of the individual sets, i.e.,
\\[\mu\left(\bigcup_{i}A_i\right) = \sum_{i}\mu(A_i), A_i \in \Sigma, i \in \mathbb{N}, A_i \cap A_j = \emptyset\\]

In general, a mapping $f: \Omega \rightarrow \Omega'$ is measurable w.r.t. $\Sigma$ and $\Sigma'$ iff
\\[
f^{-1}(S) = \lbrace s \in \Omega \text{ s.t. } f(s) \in S \rbrace \in \Sigma, \forall S \in \Sigma'
\\]
We write $f: (\Omega, \Sigma) \rightarrow (\Omega', \Sigma')$ to denote that $f$ is measurable w.r.t. $\Sigma$ and $\Sigma'$.
### Lebesgue Integration

Let $\Omega$ be a non-empty set and $\Sigma$ be a $\sigma$-algebra on $\Omega$> If $f: (\Omega, \Sigma) \rightarrow (\mathbb{R}, \mathcal{B}(\mathbb{R}))$ is bounded, and $R \in \Sigma$ , then the lower and upper sums defined by (3) and (4) are not only well defined, but also converge to the same value in the limit as $n \rightarrow \infty$. Thus, we define the integral as:
\\[\int_{R}f(\omega)d\mu(\omega) := \lim_{n\rightarrow\infty}\sum_{i=1}^{n-1}f(y_i)\mu(f^{-1}([y_i,y_{i+1}])) = \lim_{n\rightarrow\infty}\sum_{i=2}^{n}f(y_i)\mu(f^{-1}([y_{i-1},y_{i}]))\\]
