---
layout: default
keywords:
comments: false

title: Office Hours
description: Times and locations may occasionally change each week; please check this page often.
buttons: [project_appt_calendly]
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

Please add yourself to your desired queue during regular OH, and wait for your turn. During project OH, please check with the project TA on the location of the meeting.

## Google Calendar
**Office hours (times and locations) will be posted on Ed. Each TA will also have their queuestatus link available (please check Ed). You will likely need to view the calendar with your personal Gmail account (not Stanford) to see the correct settings.**
<div>
<iframe src="https://calendar.google.com/calendar/embed?src=stanfordcs230%40gmail.com&ctz=America%2FLos_Angeles" style="border: 0" width="800" height="600" frameborder="0" scrolling="no"></iframe>
</div>