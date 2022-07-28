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

## Defining the Canvas
To begin, we want to define a canvas onto which we can draw. In `Python`, we can use the `Tkinter` library for this purpose.

	from tkinter import *
	
	#define the canvas width and height.
	canv_width = 800
	canv_height = 600

	#create the canvas
	root = Tk()
	canvas = Canvas(root, width = canv_width, height = canv_height)
	canvas.pack()

The canvas uses a coordinate system whose origin $(0,0)$ is at its the bottom-left. The $x$ coordinate increases rightward, and the $y$ coordinate increases upwards.

Once we have the canvas, we can draw the background.

	#draw a rectangle from the point (0,0) to (canv_width, canv_height)
	back = canvas.create_rectangle(0, 0, canv_width, canv_height, fill = "#95e2e2")

## Defining the Surface

For simplicity, we shall define the surface using a polynomial function on $[a,b]$, i.e., a function of the form
\\[ f(x) = c_0x^n + c_1x^{n-1}\dots + c_{n-1}x + c_n,\\]
where $x \in [a,b]$.

The polynomial is defined entirely in terms of the coefficients, $c_0, \dots, c_n$. Thus, we can represent it in Python using a list:

    c =[c0, c1, c2, c3,...,cn]

We can also write code to evaluate $y=f(x)$ for any input, $x$:

    def evaluate_polynomial(c, x):
	    n = len(a) - 1
	    y = 0
	    
	    for i in range(0, n+1):
		    y += c[i]*x ** (n-i)
	    return y
	    	    
Actually drawing $f$ is quite tedious since we have to go through each $x \in [a,b]$, compute $f(x)$ and then plot the point $(x,f(x))$. However, it can be made easier if we approximate $f$ using a set of line segments.

We split the domain $[x_1, x_2]$ into $k$ segments of equal length. For each segment, $[x_i, x_{i+1}]$, we evaluate $f$ at its end-points.

	# linearize the polynomial defined by coeffs into k segments.
	# pts = [x1, f(x1), x2, f(x2),...]
	def linearize(coeffs, k, x1, x2):
	    pts = []

	    for i in range(0, k + 1):
		x = x1 + (i * (x2 - x1) / n_segs)
		pts.append(x)
		pts.append(eval(coeffs, x))
	    return pts

We can now draw line segments from $(x_i, f(x_i))$ to $(x_{i+1}, f(x_{i+1})$, approximating $f$.
	
	# generate the surface 
	surface = canvas.create_polygon(get_pts(np.array([-3.75E-9, 8.26E-6, -6.1E-3, 1.44, 4E2]), 1000, 0, canv_width), fill = "#6bd687")

To determine which way the ball bounces when it hits the ground, we need to find the tangent line to the surface at the point of contact.

First, we will need to compute the derivative of a polynomial. Analytically, we know that
\\[ f'(x) = na_0x^{n-1} + (n-1)a_1x^{n-2} + \dots  2a_{n-2}x + a_{n-1}\\]
We see that the $i$th coefficient of $f'$ is given by $(n-i)a_i$.

We use this fact to define a Python function, `differentiate` that computes the derivative of a polynomial:

    def differentiate(c):	
	    n = len(c) - 1
	    c_ = c[0:n]
	    for i in range(0, len(c_)):
		    c_[i] = (n-i)*c[i]
	    return c_	    
	    
## Defining the Ball
Like the surface, the ball can also be defined mathematically; in this case, as a circle of radius, $r$. However, unlike the surface, the ball has properties that change over time. These include:

- its position, i.e., where it is in space
- its velocity, i.e., how fast is it moving (and in what direction)
- its acceleration, i.e., how fast is its velocity changing (and in what direction)

We can thus define the ball accordingly:

	# generate the ball.
	radius = 10
	p = np.array([120.0, 0.0])
	v = np.array([4.0, 0.0])
	a = np.array([0.0, 0.22])
	ball = canvas.create_oval([p[0] - radius, p[1] - radius, p[0] + radius, p[1] + radius], fill = "white")

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

