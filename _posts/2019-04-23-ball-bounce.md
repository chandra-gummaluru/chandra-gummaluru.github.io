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
	cw = 800
	ch = 600

	#create the canvas
	root = Tk()
	canvas = Canvas(root, width = cw, height = ch)
	canvas.pack()

The canvas uses a coordinate system whose origin $(0,0)$ is at its the top-left, and the bottom-right is $(c_w,c_h)$.

Once we have the canvas, we can draw the background.

	#draw a rectangle from the point (0,0) to (canv_width, canv_height)
	back = canvas.create_rectangle(0, 0, canv_width, canv_height, fill = "#95e2e2")

## Defining the Surface
The surface can be described using any mathematical curve, but for simplicity, we shall define it using a polynomial function on $[a,b]$, i.e., a function of the form
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
	    
We can then draw line segments from $(x_i, f(x_i))$ to $(x_{i+1}, f(x_{i+1})$ for $i = 1, \dots, k-1$. The larger we make $k$, the better the approximation becomes. We will choose $x_1 = 0$ and $x_k = cw$ so that we draw the surface along the entire width of the canvas. Of course, when we actually draw the surface, we want to draw a closed curve. Thus, we will introduce additional line segments between $(cw, f(cw))$, $(cw, ch)$, $(0,ch)$ and $(0,f(0))$. 
	
	# generate the surface using k = 1000.
	surface = get_pts(np.array([-3.75E-9, 8.26E-6, -6.1E-3, 1.44, 4E2])
	surface.append([cw, ch, 0, ch])
	surface = canvas.create_polygon(surface, 1000, 0, canv_width), fill = "#6bd687")
	    
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

## Simulating the Physics
The final step is to actually simulate the physics within the `update_canvas` function. There are two cases we must consider, namely, whether the ball is above or below the surface.

The height of the surface directly above the ball's current position is given by

    ysurf = evaluate_polynomial(c, p[0])

The height of the ball itself is given by

    p[1]
    
Thus, the cases are `p[1] < ysurf` or `p[1] > ysurf`:

1. If `p[1] < ysurf`, i.e., the ball is above the surface, simulate free-fall due to gravity.

2. If the ball is on or below the surface, simulate and resolve the collision.

Simulating free-fall due to gravity is quite trivial. Indeed, we can simply use the kinematic equations:

\\[\Delta p = v\Delta t + \frac{1}{2}a\Delta t^2\\]
and
\\[ \Delta v = \frac{1}{2}a\Delta t^2.\\]

Resolving the collision is quite involved, but is based on the idea that when an object collides with a flat surface, its velocity in the direction tangent to the surface remains unchanged, but its velocity normal to the surface is negated.

To represent this idea mathematically, it will be helpful to introduce some concepts from linear algebra.

We will define points in the space using two-dimensional vectors.

A vector, $\vec{v} = \begin{bmatrix} v_x, v_y \end{bmatrix}$ is an arrow drawn from $(0,0)$ to $(v_x,v_y)$, and represents the point $(v_x,v_y)$.

In Python, we will define vectors using lists.

    v = [vx, vy]

Given a vector, $\vec{v}$, we can compute its magnitude as
\\[|\vec{v}| = \sqrt{v_x^2+v_y^2}\\]

In Python, we define a function, `mag`, to do just this:

	def mag(v):
	    return (v[0] ** 2 + v[1] ** 2) ** 0.5
	    
If $|\vec{v}| = 1$, we say that $\vec{v}$ is a unit vector. We can see that
\\[ \hat{v} = \frac{\vec{v}}{\|\vec{v}\|}\\]
is a unit-vector in the direction of $\vec{v}$.

In Python, we define a function, `unit`, to compute unit vectors:

	def unit(v):
	    return v / mag(v) 

The numbers $v_1$ and $v_y$ respectively represent _how much_ we move in the $x$ and $y$ directions. Thus, we could write $\vec{v} = v_x\hat{e}^{(x)} + v_y \hat{e}^{(y)}$, where unit vectors
\\[\hat{e}^{(x)} := \begin{bmatrix} 1 & 0 \end{bmatrix} \text{ and } \hat{e}^{(y)} := \begin{bmatrix} 0 & 1 \end{bmatrix}\\]
are called the _standard basis vectors_ and represent the $x$ and $y$ directions respectively.

The $x$ and $y$ directions are not special. Indeed, we could have chosen any two (perpendicular) directions. In general, these directions can also be represented with unit vectors, $\hat{e}^{(1)}$ and $\hat{e}^{(2)}$. If $v_1\vec{e}^{(1)} + v_2\hat{e}^{(2)} = v_x\vec{e}^{(x)} + v_y\vec{e}^{(y)}$, then the vector $\begin{bmatrix} v_1 & v_2 \end{bmatrix}$ under the basis $\lbrace \hat{e}^{(1)}, \hat{e}^{(2)} \rbrace$ is equivalent to the vector $\begin{bmatrix} v_x & v_y \end{bmatrix}$ under the standard basis.

We are interested in the _tangential/normal basis_, which represents a vector using directions that are tangent to and normal to a surface at some point along the surface. We need a way switch between the standard basis and the tangential/normal basis, i.e., a change-of-basis transformation.

To do this, we will need to introduce a few additional concepts. Given two vectors, $v$ and $u$, we define the dot-product of the vectors to be
\\[ v \cdot u = v_xu_x + v_yu_y\\]

In Python, we define a function, `dot` to compute the dot-product of two vectors:
	
	def dot(u,v):
	    return u[0]*v[0] + u[1]*v[1]
	    
It turns out that $\vec{v} \dot \vec{u} / \|\vec{u}\|$ gives the magnitude of the component of $\vec{v}$ in the direction given by $\vec{u}$ (see [the proof here](https://tutorial.math.lamar.edu/classes/calcii/dotproduct.aspx)).

Thus, if we are given basis vectors, $\vec{e}^{(1)}$, and $\vec{e}^{(2)}$, and a vector $\begin{bmatrix} v_x & v_y \end{bmatrix}$ represented using the standard basis, the equivalent vector in the new basis is
\\[\begin{bmatrix}\begin{bmatrix} v_x & v_y \end{bmatrix} \cdot e^{(1)} & \begin{bmatrix} v_x & v_y \end{bmatrix} \cdot e^{(2)}.\\]
