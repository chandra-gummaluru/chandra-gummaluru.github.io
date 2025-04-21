---
layout: category
title: "teaching"
permalink: '/teaching'
---

<br>
<div style="font-size:3em;">Teaching</div>
This page contains a selection of courses I’ve taught, along with related materials, projects, and other teaching contributions. Each entry includes links to resources, descriptions, and context where available.
<br>
<div style="font-size:1.8em;">Portfolio</div>
<hr>
<div class="catalogue">
  {% assign category = "teaching_portfolio" %}
  {% for post in site.categories[category] %}
    {% include catalogue_item.html post=post %}
  {% endfor %}
</div>
<div style="font-size:1.8em;">Projects</div>
<hr>
<div style="font-size:1.8em;">Course Material</div>
<hr>
