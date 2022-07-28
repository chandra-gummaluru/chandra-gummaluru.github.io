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
The final step is to actually simulate the physics within the `update_canvas` function. In the real-world, the motion of objects is continuous. However, we will need to discretize it. Thus, we define $\Delta t$ to represent the actual elapsed time between discrete time-steps.

    dt = 1
    dt2 = dt ** 2
    
The physics involved depends on whether the ball is currently above the surface or whether it has collided with it. The height of the surface directly above the ball's current position is given by

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

It is convenient to define some constants representing the standard basis:

    ex = np.array([1.0, 0.0])
    ey = np.array([0.0, 1.0])

We are interested in the _tangential/normal basis_, which represents a vector using directions that are tangent to and normal to a surface at some point along the surface. We need a way switch between the standard basis and the tangential/normal basis, i.e., a change-of-basis transformation.

To do this, we will need to introduce a few additional concepts. Given two vectors, $\vec{v}$ and $\vec{u}$, we define the dot-product of the vectors to be
\\[ \vec{v} \cdot \vec{u} = v_xu_x + v_yu_y\\]

In Python, we define a function, `dot` to compute the dot-product of two vectors:
	
	def dot(u,v):
	    return u[0]*v[0] + u[1]*v[1]


It can be shown that $\vec{v} \cdot \vec{u}  = \|\vec{v}\|\|\vec{u}\|\cos{\theta}$, where $\theta$ is the angle between the vectors (see [the proof here](https://tutorial.math.lamar.edu/classes/calcii/dotproduct.aspx)). Thus, the _projection_ of $\vec{v}$ onto $\vec{u}$ is given by
\\[\text{proj}_{\vec{u}}(\vec{v}) = \frac{\vec{v} \cdot \vec{u}}{\|\vec{u}\|^2}\vec{u}\\]

In Python, we define a function, `project` to compute the projection of a vector onto another:

	def project(u,v):
	    return u * dot(v,u) / (mag(u) ** 2)

Thus, if we are given basis vectors, $\hat{e}^{(1)}$, and $\hat{e}^{(2)}$, and a vector $\begin{bmatrix} v_x & v_y \end{bmatrix}$ represented using the standard basis, the equivalent vector in the new basis is
\\[\text{proj}_{\hat{e}^{(1)}}(\vec{v}) + \text{proj}_{\hat{e}^{(2)}}(\vec{v}).\\]

Now, we need to figure out what the tangential and normal directions are. If $m$ is the slope of tangent line to the surface at some point, then the unit vector parallel to the line is
\\[ \hat{u} = \frac{\vec{u}}{\|\vec{u}\|}\\] where $\vec{u} = \begin{bmatrix} 1 & m \end{bmatrix}$.

In Python, we can use the following to get a unit vector for a given slope, $m$.

	def slope_to_vec(m):
	    uvec = np.array([1.0, m])
	    uhat = uvec / mag(uvec)
	    return uhat
	    
We now need to determine the slope of the tangent/normal lines to the surface. The latter is the negative reciprocal of the former, which itself is given by the derivative of $f$. In this case,

\\[ f'(x) = nc_0x^{n-1} + (n-1)c_1x^{n-2} + \dots  2c_{n-2}x + c_{n-1}\\]

We see that the $i$th coefficient of $f'$ is given by $(n-i)c_i$.

We use this fact to define a Python function, `differentiate` that computes the derivative of a polynomial:

	def differentiate(c):
	    dc = []

	    for i in range(0, len(c) - 1):
		dc.append((len(c) - 1 - i) * c[i])

	    return np.array(dc)

We can now resolve the collision as follows.

1. Let $(x^\*, f(x^\*))$ denote the point of collision.

2. Use `differentiate` and `evaluate_function` to compute $t = f'(x^\*)$, which represents the slope of the line tangent to $f$ at $x^\*$. The slope of the line normal to $f$ at $x^\*$ is then $n = -1/t$.
   
3. Convert $t$ and $n$ into vectors, $\vec{t}$ and $\vec{n}$, representing the tangential and normal directions using `slope_to_vec`.
    
4. Project $\vec{v}$ onto $\vec{t}$ and $\vec{n}$ using `project`; denote the resulting vectors as $\vec{v}^{(t)}$ and $\vec{v}^{(n)}$.

5. Set $v \leftarrow \vec{v}^{(t)} - k_r\vec{v}^{(n)}$, where $k_r$ is the coefficient of restitution.

6. Project $\vec{v}$ back onto the $x$ and $y$ axes using `project`; denote the resulting vectors as $\vec{v}^{(x)}$ and $\vec{v}^{(y)}$.

7. Set $v \leftarrow \vec{v}^{(x)} + \vec{v}^{(y)}$.
    
8. move the ball to the surface, i.e., shift it down by `ysurf - p[1]` and set its vertical position to be `p[1] = ysurf`.

Putting it all together, the `update_canvas` function becomes:

    def update_canvas(dt, p, v, a, surface):
        # determine the height of the surface directly above the ball.
        ysurf = eval(surface, p[0])

        # if the ball is below the surface
        if p[1] > ysurf:
        
            #compute the slope of the tangent and normal lines.
            tangent = eval(differentiate(surface), p[0])
            normal = -1.0 / tangent

            # compute the tangent and normal vectors.
            tangent = slope_to_vec(tangent)
            normal = slope_to_vec(normal)

            #get the tangential and normal components of the velocity vector.
            vtan = project(v, tangent)
            vnorm = project(v, normal)

            #negate the normal component.
            vnorm = - 0.6 * vnorm
            vtan = 0.99 * vtan

            #back project the new velocity onto the x and y axes.
            v = project(vtan, xaxis) + project(vnorm, xaxis) + project(vtan, yaxis) + project(vnorm, yaxis)

            canvas.move(ball, 0, ysurf - p[1])
            p[1] = ysurf
        else:
            #update ball position and velocity using the kinematic equations.
            p += v * dt + 0.5 * a * dt2
            v += 0.5 * a * dt2

            canvas.move(ball, v[0], v[1])

        #wait, and repeat
        canvas.after(frame_rate, update_canvas, dt, p, v, a, surface) 
