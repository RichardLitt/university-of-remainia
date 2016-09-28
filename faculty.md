---
layout: page
title: Faculty
header: Our Faculty
group: 
---
{% include JB/setup %}

### Faculty of Arts and Humanities

{% for member in site.faculty %}{% if member.department == "Arts" %}
- [{{member.title}} {{ member.name }}](faculty/{{ member.lastName | downcase }}/){% endif %}{% endfor %}

### Faculty of Social Sciences

{% for member in site.faculty %}{% if member.department == "Social Sciences" %}
- [{{member.title}} {{ member.name }}](faculty/{{ member.lastName | downcase }}/){% endif %}{% endfor %}

### Faculty of Natural Sciences

{% for member in site.faculty %}{% if member.department == "Natural Sciences" %}
- [{{member.title}} {{ member.name }}](faculty/{{ member.lastName | downcase }}/){% endif %}{% endfor %}

### Faculty of Medicine

{% for member in site.faculty %}
  {% if member.department == "Medicine" %}
- [{{member.title}} {{ member.name }}](faculty/{{ member.lastName | downcase }}/){% endif %}
{% endfor %}

### Support Services

* The University Library
* Research Support Office

### Industrial Partners

