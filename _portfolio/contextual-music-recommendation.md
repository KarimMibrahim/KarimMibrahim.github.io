---
title: "Contextual Music Recommendation"
excerpt: "My PhD project at Télécom Paris and Deezer, studying how listening context — activity, mood, device, time of day — shapes what music people want to hear, and building systems that learn to predict it automatically."
collection: portfolio
date: 2022-01-01
header:
  teaser: teasers/context-teaser.jpg
---

**Duration:** 2018 – 2022  
**Affiliation:** Télécom Paris & Deezer Research, Paris  
**Supervisors:** Dr. Gaël Richard, Dr. Geoffroy Peeters (Télécom Paris), Dr. Elena V. Epure (Deezer)

---

## The Problem

We listen to different music when we are working out than when we are studying. We reach for different tracks when we are with friends than when we are alone. This is intuitive to anyone who uses a music streaming service — yet most recommendation systems still treat music listening as a single, context-free preference.

The goal of this project was to understand how the *listening context* — the combination of a user's activity, mood, social setting, location, and device — shapes what music they want to hear, and to build intelligent systems that can predict this automatically at scale.

<div style="text-align:center">
<figure class="figure w-100">
  <img src="{{ '/images/context/activities.png' | relative_url }}" alt="Frequency of different listening situations" class="figure-img img-fluid mx-auto d-flex" style="max-width:600px">
  <figcaption class="figure-caption text-center">
  Frequency of different listening situations that influence music preference, from Greb et al.
  </figcaption>
</figure>
</div>

## What is Context?

Context in music is multidisciplinary. It draws from **psychology** (how do situations influence listening preference?), **information retrieval** (how do we represent music content in a way that captures its contextual fit?), and **machine learning** (how do we build systems that learn this from data?).

Psychologists have long documented that people use music for specific functions — to manage mood, to energise activity, to signal identity, to accompany social settings. Those functions map to different musical features. A key challenge is mapping the abstract, language-based notion of "context" (e.g. "relaxing at home", "working out") onto the audio signal itself.

<div style="text-align:center">
<figure class="figure w-100">
  <img src="{{ '/images/context/intent.png' | relative_url }}" alt="Listening intent reported by participants" class="figure-img img-fluid mx-auto d-flex" style="max-width:600px">
  <figcaption class="figure-caption text-center">
  Reported listening intents from participants in a study by Schäfer et al. — the variety reflects how context-driven music use really is.
  </figcaption>
</figure>
</div>

## Representing Music for Context

To connect audio content to contextual tags, we need good representations. One classic approach is the valence-arousal scale — a two-dimensional emotional map that places music according to how energetic and how positive it sounds. While useful, it is coarse. More powerful are learned embedding spaces, where music tracks are placed close together if they tend to be listened to in the same contexts.

<div style="text-align:center">
<figure class="figure w-100">
  <img src="{{ '/images/context/valencearousal.png' | relative_url }}" alt="Valence-Arousal space" class="figure-img img-fluid mx-auto d-flex" style="max-width:500px">
  <figcaption class="figure-caption text-center">
  The valence-arousal scale — a simple but widely used way to describe the emotional content of music.
  </figcaption>
</figure>
</div>

<div style="text-align:center">
<figure class="figure w-100">
  <img src="{{ '/images/context/embeds.png' | relative_url }}" alt="Music embedding space" class="figure-img img-fluid mx-auto d-flex" style="max-width:600px">
  <figcaption class="figure-caption text-center">
  A 2-D projection of a music embedding space — tracks with similar contextual associations cluster together.
  </figcaption>
</figure>
</div>

## The Research Arc

The project evolved through four published studies, each building on the last.

**1. Building the dataset and baseline system — ICASSP 2020**  
We first needed data. We assembled a dataset of ~50,000 tracks labelled with 15 contextual tags (e.g. "workout", "sleep", "party") and trained a model to predict these tags from audio alone. This established the first audio-based contextual auto-tagging baseline.

**2. Learning with incomplete labels — ICMR 2020**  
In real-world datasets, not every track is labelled for every context. A track might be labelled "workout" but simply lack a "no sleep" label — it's missing, not absent. We proposed a confidence-based weighted loss function that accounts for this ambiguity during training, improving performance significantly without requiring extra labelling effort.

**3. Should the system know who is listening? — ISMIR 2020**  
Context is not just about the music — it is also about the *listener*. The same track might fit a morning commute for one person but a late-night study session for another. We built a user-aware auto-tagging system that combines audio content with a listener's history to predict contextual tags per user, and proposed a new dataset annotated with per-user contextual labels.

**4. Using device and sensor data as context signals — ISMIR 2022**  
A running user listening on earphones at 7am is a strong signal. We explored whether the *device* a user is listening on (phone, speaker, earphones) and the *time of day* can serve as proxy signals for context, eliminating the need for explicit mood or activity labels entirely. The results showed these passive signals carry surprisingly strong contextual information.

## Publications

- Ibrahim, K. M., Royo-Letelier, J., Epure, E. V., Peeters, G., Richard, G. [Audio-Based Auto-Tagging With Contextual Tags for Music](https://hal.archives-ouvertes.fr/hal-02481374). *ICASSP 2020, Barcelona.*
- Ibrahim, K. M., Epure, E. V., Peeters, G., Richard, G. [Confidence-based Weighted Loss for Multi-label Classification with Missing Labels](https://hal.archives-ouvertes.fr/hal-02547012/). *ICMR 2020, Dublin.*
- Ibrahim, K. M., Epure, E. V., Peeters, G., Richard, G. [Should We Consider the Users in Contextual Music Auto-Tagging Models?](https://hal.telecom-paris.fr/hal-02934433/). *ISMIR 2020, Montreal.*
- Ibrahim, K. M., Epure, E. V., Peeters, G., Richard, G. [Exploiting Device and Audio Data to Tag Music with User-Aware Listening Contexts](https://hal-insu.archives-ouvertes.fr/IDS/hal-03903647v1). *ISMIR 2022, Bengaluru.*
