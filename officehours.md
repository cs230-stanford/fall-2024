---
layout: default
keywords:
comments: false

title: Office Hours
description: Times and locations may occasionally change each week; please check this page often.
buttons: [project_appt_calendly, zoom]
micro_nav: false
---

## Office Hours Table <a name="table"></a>

| TA | Specialization | Project Office Hour Signup |
|----|----------------|:--------------------------:|
{% assign people = site.course.ta | concat: site.course.staff -%}
{% for ta in people -%}
{% unless ta.type != "TA" and ta.type != "Head TA" -%}
| {{ ta.name }} | {{ta.area}} | [Click to book]({{ ta.calendly }})
{% endunless -%}
{% endfor %}

Please add yourself to your desired queue during regular OH, and wait for your turn. During project OH, go to your project TA's room on Zoom.

## Google Calendar

**All Office Hours are held remotely over Zoom**

<div>
<iframe src="https://calendar.google.com/calendar/embed?src=3j15449s7pcjs6tta065qm1p1k%40group.calendar.google.com&ctz=America%2FLos_Angeles" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>
</div>
