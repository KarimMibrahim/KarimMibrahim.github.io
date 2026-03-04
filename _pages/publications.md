---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

## Conference & Workshop Papers

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

---

## PhD Thesis

**Personalised Contextual Music Recommendation**
Karim M. Ibrahim — supervised by Dr. Gaël Richard, Dr. Geoffroy Peeters (Télécom Paris) and Dr. Elena Epure (Deezer).
Télécom Paris, Institut Polytechnique de Paris, 2021.

[View on HAL](https://theses.hal.science/tel-03669555)
