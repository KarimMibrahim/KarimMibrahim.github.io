---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if site.author.googlescholar %}
  You can also find my articles on <u><a href="{{site.author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}

## Conference & Workshop Papers

{% for post in site.publications reversed %}
  {% include archive-single.html %}
{% endfor %}

---

## Theses

**Personalised Contextual Music Recommendation** *(PhD)*
Karim M. Ibrahim — supervised by Dr. Gaël Richard, Dr. Geoffroy Peeters (Télécom Paris) and Dr. Elena Epure (Deezer).
Télécom Paris, Institut Polytechnique de Paris, 2021.
[[View on HAL]](https://theses.hal.science/tel-03633097/)

**Singing Voice Intelligibility** *(M.Sc.)*
Karim M. Ibrahim — Department of Computer Science, National University of Singapore, 2017.
[[View on ScholarBank]](http://scholarbank.nus.edu.sg/handle/10635/148567)

**Primary-Ambient Audio Source Separation and Surround Sound Upmixing** *(M.Sc.)*
Karim M. Ibrahim — Faculty of Information Technology and Computer Science, Nile University, Cairo, 2015.
