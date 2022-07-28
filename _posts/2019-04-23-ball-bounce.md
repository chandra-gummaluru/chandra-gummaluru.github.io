---
layout: post
title: "Tutorial: Simulating a Ball Bounce in Python"
author: "Chandra Gummaluru"
---

In this tutorial, we will aim to simulate a ball bouncing off a curved surface in Python as shown below: 

![enter image description here](https://raw.githubusercontent.com/chandra-gummaluru/chandra-gummaluru.github.io/master/media/ball_bounce/bb_bounce.gif)

**Objective:** To show how basic linear algebra and calculus is used in developing games.

**Audience:** Anyone who has some familiarity with calculus, linear algebra, and Python programming, but aren't sure how to put all the pieces together.

*Note that the code we write in this tutorial is neither efficient nor robust. It is only meant to serve as a learning example.*

## Defining the Surface

For simplicity, we shall define the surface using a polynomial function, i.e., a function of the form
\\[ f(x) = a_0x^n + a_1x^{n-1}\dots + a_{n-1}x + a_n \\]
The polynomial is defined entirely in terms of the coefficients, $a_0, \dots, a_n$. Thus, we can represent it in Python using a list:

    a =[a0, a1, a2, a3,...,an]

We can also write code to evaluate $y=f(x)$ for any input, $x$:

    def evaluate_polynomial(a, x):
	    n = len(a) - 1
	    y = 0
	    
	    for i in range(0, n+1):
		    y += a(i)*x ** (n-i)
	    return y

Instead, we want a piecewise linear approximation of $f$. To achieve this, we will split the domain of $f$ into $k + 1$ segments, say $(-\inf, x_1], [x_1, x_2], \dots, [x_{k-1}, x_k], [x_k, \infty)$. For each segment, $(x_i ,x_{i+1})$, we evaluate $f$ at its limit points, i.e., $f(x_1)$ and $f(x_2)$. We then define the line segment,
\\[l_i(x) = \frac{f(x_{i+1}) - f(x_i)}{x_{i+1}-x_i}x\\]


To determine which way the ball bounces when it hits the ground, we need to find the tangent line to the surface at the point of contact.

First, we will need to compute the derivative of a polynomial. Analytically, we know that
\\[ f'(x) = na_0x^{n-1} + (n-1)a_1x^{n-2} + \dots  2a_{n-2}x + a_{n-1}\\]
We see that the $i$th coefficient of $f'$ is given by $(n-i)a_i$.

We use this fact to define a Python function, `differentiate` that computes the derivative of a polynomial:

    def differentiate(a):	
	    n = len(a) - 1
	    a_ = a[0:n]
	    for i in range(0, len(a_)):
		    a_[i] = (n-i)*a[i]
	    return a_	    

\\[  \begin{tikzpicture}[auto,vertex/.style={draw,circle}]
    \node[vertex] (a) {A};
    \node[vertex,right=1cm of a] (b) {B};
    \node[vertex,below right=1cm and 0.5cm of a] (c) {C};
    
    \path[-{Stealth[]}]
      (a) edge node {1} (b) 
      (a) edge (c)
      (c) edge (b);
  \end{tikzpicture}\\]
## Basic Linear Algebra Functions

We will define points in the space using two-dimensional vectors.

A vector, $\vec{v} = \begin{bmatrix} v_x, v_y \end{bmatrix}$ is an arrow drawn from $(0,0)$ to $(v_x,v_y)$, and represents the point $(v_x,v_y)$.

In Python, we will define vectors using lists.

    v = [vx, vy]
    
Given a vector, $\vec{v}$, we can compute its magnitude as
\\[|\vec{v}| = \sqrt{v_x^2+v_y^2}\\]

InPython, we define a function, `mag`, to do just this:

    def mag(v):
	    return (v[0] ** 2 + v[1] ** 2) ** 0.5
Note that `vx = v[0]` and `vy = v[1]`.

If $\|\vec{v}\| = 1$, we say that $\vec{v}$ is a unit vector. We can see that
\\[ \hat{v} = \frac{\vec{v}}{\|\vec{v}\|}\\]
is a unit-vector in the direction of $\vec{v}$.
In Python, we define a function, `unit`, to compute unit vectors:

    def unit(v):
	    return v / mag(v)
Given two vectors, $v$ and $u$, we define the dot-product of the vectors to be
\\[ v \cdot u = v_xu_x + v_yu_y\\]
In Python, we define a function, `dot` to compute the dot-product of two vectors:

    def dot(u,v):
	    return u[0]*v[0] + u[1]*v[1]
It can be shown that $v \cdot u  = \|v\|\|u\|\cos{\theta}$, where $\theta$ is the angle between the vectors.

We can now project $\vec{u}$ onto $\vec{v}$, as follows:
\\[\text{proj}_{\vec{v}}(\vec{u}) = \frac{\vec{v} \cdot \vec{u}}{\|\vec{u}\|^2}\vec{u}\\]
In Python, we define a function, `proj` to compute the projection of a vector onto another:

    def proj(u,v):
	    return u * dot(u,v) / (mag(u) ** 2)
    
    

If $m$ is the slope of the line, the unit vector parallel to the line is
\\[ \hat{u} = \frac{\vec{u}}{\|\vec{u}\|}\\] where $\vec{u} = \begin{bmatrix} 1 & m \end{bmatrix}$.

    def slope_to_vec(m):
        uvec = np.array([1.0, m])
        uhat = uvec / mag(uvec)
        return uhat

