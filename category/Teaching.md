---
layout: category
title: "teaching"
permalink: '/teaching'
---

<br>
<div style="font-size:3em;">Teaching</div>

<div style="font-size:1.5em;">Portfolio</div>
<div class="catalogue">
  {% assign category = "teaching_portfolio" %}
  {% for post in site.categories[category] %}
    {% include catalogue_item.html post=post %}
  {% endfor %}
</div>

<br>
<div style="font-size:1.5em;">Resources</div>
You can find teaching resources for various subjects below.
