---
layout: archive
title: "CV"
permalink: /cv/
author_profile: true
redirect_from:
  - /resume
---

{% include base_path %}

## Education

<div class="cv-timeline">

  <div class="cv-entry">
    <div class="cv-entry__date">2018 – 2022</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">Ph.D. in Computer Science</div>
      <div class="cv-entry__org">Télécom Paris · Polytechnic Institute of Paris, France</div>
      <ul>
        <li>Thesis: <em>Personalized Audio Auto-Tagging as Proxy for Contextual Music Recommendation</em></li>
        <li>Supervisors: Dr. Gaël Richard, Dr. Geoffroy Peeters, Dr. Elena V. Epure</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">2016 – 2018</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">M.Sc. in Computer Science</div>
      <div class="cv-entry__org">National University of Singapore, Singapore</div>
      <ul>
        <li>Thesis: <em>Recommending Music for Language Learning: The Problem of Singing Voice Intelligibility</em></li>
        <li>Supervisor: Dr. Ye Wang</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">2014 – 2016</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">M.Sc. in Software Engineering</div>
      <div class="cv-entry__org">Nile University, Cairo, Egypt</div>
      <ul>
        <li>Thesis: <em>Primary-Ambient Separation of Audio Signals</em></li>
        <li>🏆 Best Thesis Award</li>
        <li>Supervisors: Dr. Mahmoud Allam, Dr. Stefan Uhlich</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">2010 – 2014</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">B.Sc. in Electronics Engineering</div>
      <div class="cv-entry__org">Fayoum University, Egypt</div>
    </div>
  </div>

</div>

---

## Work Experience

<div class="cv-timeline">

  <div class="cv-entry">
    <div class="cv-entry__date">May 2025 – Present</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">Senior Audio Research Scientist</div>
      <div class="cv-entry__org">Serato · Auckland, New Zealand</div>
      <ul>
        <li>Develop next-gen beat detection and low-latency stem separation powering Serato creator products (Serato DJ Pro, Serato Studio).</li>
        <li>Designed tempo-tracking pipeline robust to genre shifts, swing, and drift.</li>
        <li>Provide technical leadership across research and product; mentor junior scientists and engineers.</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">Jun 2023 – Oct 2024</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">Research Scientist</div>
      <div class="cv-entry__org">Emobot · Paris, France</div>
      <ul>
        <li>Led research on speech emotion recognition, increasing accuracy to 96%, impacting healthcare applications with real-time responsiveness.</li>
        <li>Supervised research interns and junior researchers, leading projects from inception to prototype development.</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">Jun 2022 – Jun 2023</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">R&D Project Manager</div>
      <div class="cv-entry__org">Arkamys · Paris, France</div>
      <ul>
        <li>Led research project on road noise cancellation for vehicles.</li>
        <li>Managed end-to-end audio/ML project lifecycles from planning and resourcing to delivery and production.</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">Oct 2018 – Jan 2022</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">Research Scientist</div>
      <div class="cv-entry__org">Deezer Research · Paris, France</div>
      <ul>
        <li>Developed and implemented contextual music recommendation models, improving recommendations used by 10 million users.</li>
        <li>Conducted large-scale data collection and analysis to create music auto-tagging models for varying listening moods.</li>
        <li>Supervisor: Dr. Elena V. Epure</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">Mar – Aug 2018</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">Research Intern</div>
      <div class="cv-entry__org">IBM · Singapore</div>
      <ul>
        <li>Designed and trained NLP-based question answering systems using Markov Logic Networks.</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">Dec 2016 – Sep 2018</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">Research Assistant</div>
      <div class="cv-entry__org">National University of Singapore · Singapore</div>
      <ul>
        <li>Built evaluation system for singing-voice intelligibility to support language-learning music recommendation research.</li>
      </ul>
    </div>
  </div>

  <div class="cv-entry">
    <div class="cv-entry__date">Aug 2015 – Feb 2016</div>
    <div class="cv-entry__body">
      <div class="cv-entry__role">Research Intern</div>
      <div class="cv-entry__org">Sony Stuttgart Technology Center · Stuttgart, Germany</div>
      <ul>
        <li>Developed algorithms for primary-ambient source separation for audio up-mixing.</li>
        <li>Developed the first neural network based solution for primary-ambient source separation.</li>
        <li>Supervisor: Dr. Stefan Uhlich</li>
      </ul>
    </div>
  </div>

</div>

---

## Publications

<ul>{% for post in site.publications %}
  {% include archive-single-cv.html %}
{% endfor %}</ul>
