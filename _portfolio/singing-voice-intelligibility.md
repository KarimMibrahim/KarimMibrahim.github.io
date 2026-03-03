---
title: "Singing Voice Intelligibility"
excerpt: "For my M.Sc. at NUS, I studied what makes song lyrics easy or hard to understand, and built systems to measure it automatically — motivated by a real application: recommending music for language learning."
collection: portfolio
date: 2018-01-01
---

**Duration:** 2017 – 2018  
**Affiliation:** National University of Singapore (NUS)  
**Supervisor:** Dr. Ye Wang

---

## The Problem

When you listen to a song in a language you are learning, how much of it can you actually understand? This is not just about vocabulary — it is about how clearly the singer enunciates, how fast the lyrics move, whether the melody obscures the consonants, and how the production treats the vocal track.

Intelligibility in speech is a well-studied field. In singing, it is much less explored, despite being directly relevant to applications like language-learning music recommendation. If you are trying to learn English through music, being recommended a song with mumbled, heavily processed vocals is not going to help you.

This project asked two related questions: what acoustic properties of a song predict how intelligible its lyrics are to a listener? And can we build a system to estimate this automatically?

## Measuring Intelligibility

The first challenge was measurement. There is no off-the-shelf intelligibility score for songs. We designed a listening study where participants transcribed lyrics from a diverse set of songs, and used transcription accuracy as a proxy for intelligibility. This produced a ground-truth dataset linking songs to human-perceived intelligibility scores.

## Acoustic Features

With labels in hand, we extracted a range of acoustic features from the vocal track — things like the clarity of consonant onset, the ratio of voiced to unvoiced segments, pitch stability, tempo, and spectral balance between the voice and accompaniment. We then trained regression models to predict intelligibility from these features, and analysed which factors mattered most.

This second study (ISMIR 2018) took a broader lens, asking not just "how intelligible is this?" but "what makes a song more or less singable in the first place?" — which fed back into the recommendation use case.

---

*A figure from the ISMIR 2017 or ISMIR 2018 paper will be added here. You can drop an image into `images/` and reference it as `{{ '/images/your-figure.png' | relative_url }}`.*

---

## Publications

- Ibrahim, K. M., Grunberg, D., Agres, K., Gupta, C., Wang, Y. [Intelligibility of Sung Lyrics: A Pilot Study](https://karimmibrahim.github.io/files/2017-10-01-IoSL.pdf). *ISMIR 2017, Suzhou.*
- Mustaine, M., Ibrahim, K. M., Gupta, C., Wang, Y. [Empirically Weighing the Importance of Decision Factors When Selecting Music to Sing](http://karimmibrahim.github.io/files/2018-10-01-singability.pdf). *ISMIR 2018, Paris.*
