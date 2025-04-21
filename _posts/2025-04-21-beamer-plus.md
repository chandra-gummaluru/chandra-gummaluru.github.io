---
layout: post
title: "Beamer+: Interactive Presentations"
author: "Chandra Gummaluru"
categories: teaching_projects
---

As someone who teaches and presents technical topics often, I found myself limited by the static nature of traditional Beamer slides. I wanted a more dynamic experience—something that could combine beautifully typeset slides with video playback, drawing, and annotation tools. That’s why I created **Beamer+**.

## What Is Beamer+?

**Beamer+** is a lightweight web-based presentation app built with Python and Flask that enhances your Beamer PDFs by adding:

- 🎥 **Embedded Video Playback**  
- ✏️ **Real-Time Drawing and Highlighting Tools**  
- 🖱️ **Keyboard and Mouse Navigation**  

With Beamer+, you can turn a static PDF into a more engaging and interactive lecture or demo—perfect for classrooms, conferences, or online content creation.

![beamer-plus-ui](https://github.com/user-attachments/assets/8793a043-201f-4b2e-87ef-d673d5ffab3a)

## Why I Built It

As a computer science researcher and educator, I regularly use slides that integrate visual intuition, code snippets, and now more frequently, **demonstrations via video**. I wanted a seamless way to switch between slides and short video clips without disrupting the flow of my presentation. I also wanted to annotate and draw on slides during discussions—all while keeping everything self-contained and customizable.

## How It Works

The app runs locally and loads your Beamer-generated PDFs and video clips from a `static` folder. With a clean UI and keyboard shortcuts (like `P` for pen, `H` for highlight, `E` for eraser), it’s easy to teach and present without ever breaking stride.

## Try It

You can find the open-source project [here](https://github.com/chandra-gummaluru/beamer_plus) To get started, just download the executable, add your slides and videos, and you're ready to present! Got a feature in mind? I’d love to hear it—reach out anytime!
