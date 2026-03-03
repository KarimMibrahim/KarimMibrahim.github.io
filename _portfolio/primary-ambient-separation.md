---
title: "Primary-Ambient Source Separation"
excerpt: "My first research project, spanning my M.Sc. at Nile University and an internship at Sony Stuttgart. The goal: automatically separate the direct sound from the diffuse ambience in a stereo recording, to enable surround sound upmixing."
collection: portfolio
date: 2016-01-01
---

**Duration:** 2015 – 2018  
**Affiliation:** Nile University, Cairo & Sony Stuttgart Technology Center  
**Supervisors:** Dr. Mahmoud Allam (Nile University), Dr. Stefan Uhlich (Sony)  
**Award:** Best Thesis Award — Nile University

---

## The Problem

When you record a concert or a live performance, what you capture is a mixture of two fundamentally different types of sound. The *primary* component is the direct sound — the instrument in front of you, the singer's voice travelling straight to the microphone. The *ambient* component is the diffuse sound — the reverb bouncing off the walls, the crowd noise, the acoustic space of the room.

A standard stereo recording blends these two components together. But if you want to play that recording back through a surround sound system — five speakers, or seven — you need to separate them. The direct sound should come from the front speakers. The ambience should wrap around the listener from the sides and rear. Without separating them first, you cannot do this convincingly.

Primary-ambient extraction (PAE) is the signal processing problem of doing this separation automatically, from the stereo mix alone, without access to the original recording stems.

## The Classical Approach — SMC 2016

The traditional approach to PAE relies on the observation that primary and ambient sounds have different spatial properties. Direct sounds tend to be correlated between the left and right channels (they come from a specific direction), while ambient sounds are less correlated (they come from all directions).

In our first paper, we used **Principal Component Analysis (PCA)** to exploit this correlation structure. By decomposing the stereo signal into its principal components and applying adaptive frequency-dependent weighting, we could estimate the primary and ambient signals more accurately than previous fixed-weight approaches. The key contribution was the adaptive weighting scheme, which let the system adjust to the signal at different frequencies independently.

## A Neural Network Approach — ICASSP 2018

The classical method works well under ideal conditions, but real recordings are messy. The assumptions about correlation break down when multiple instruments overlap, or when the recording is heavily processed.

The second study replaced the classical signal processing pipeline with a **neural network**. Given pairs of mixed stereo signals and their known primary/ambient components (generated synthetically), the network learned to perform the separation end-to-end. This was one of the first neural network approaches to primary-ambient extraction, and it outperformed the PCA baseline on more realistic, complex material.

This work was done during my thesis internship at Sony's Stuttgart Technology Center, where the application to real product development was direct.

---

*A figure from the SMC 2016 or ICASSP 2018 paper will be added here. You can drop an image into `images/` and reference it as `{{ '/images/your-figure.png' | relative_url }}`.*

---

## Publications

- Ibrahim, K. M., Allam, M. [Primary-Ambient Extraction in Audio Signals Using Adaptive Weighting and Principal Component Analysis](http://karimmibrahim.github.io/files/2016-09-01-PAE_PCA.pdf). *SMC 2016.*
- Ibrahim, K. M., Allam, M. [Primary-Ambient Source Separation for Upmixing to Surround Sound Systems](https://ieeexplore.ieee.org/abstract/document/8461459). *ICASSP 2018, Calgary.*
