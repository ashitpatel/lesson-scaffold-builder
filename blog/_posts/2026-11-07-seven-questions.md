---
title: "Seven questions before a single lesson is planned"
description: "Before planning anything, the tool asks about your lesson, your modules and your methods: one sequence or several, broken along which lines, how many weeks, and which approaches to leave out."
layout: post
series: scaffold
date: 2026-11-07 00:01:00 +0000
---

*Part 2 of 6 in a series on [Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder).*

The [last post]({{ site.baseurl }}/from-lesson-to-classroom/) described the Sunday-evening problem: a long lesson in, a runnable sequence out. But a tool that plans lessons without asking anything would just be a faster way to get someone else's plan. So before it plans anything, LSB asks seven questions. Here is what each one asks, and why it matters.

## 1. What is the lesson, and who is it for?

Paste the lesson or upload the file, and give the context a plan needs: the grade band, the lesson length, the language for the cards, and your role. A 45-minute period in a Grade 5 classroom plans differently from a double period in Grade 9, and the cards should say so.

## 2. Is this starting outline right?

The tool shows the lesson's goal and a table of its sections — what each covers, what it asks learners to do — and asks you to confirm. This is the cheapest place to catch a misunderstanding: everything downstream builds on this outline.

## 3. One sequence, or several — and along which lines?

A long lesson can become one scaffold spanning the whole thing, or up to four smaller ones. If several, the tool suggests breakdown lines drawn from the lesson's own sections — by topic, by skill, by week — and asks how many units at most, and how many weeks each may take (2 to 4). Small sequences with clear handoffs are easier to teach, to lose a week from, and to hand to a colleague. But splitting has a cost: every boundary needs a "recall what came before" step, or the thread breaks. So one unbroken sequence is always on the table.

In the same round, the tool asks how to handle region-specific content: strip it to generic labels (the default), keep the lesson's own locale, or strip it and then relocalize to your setting. Relocalizing means naming your target locale, adding notes about it (what to prefer, what to avoid), and reviewing each proposed replacement — approve, skip, or write your own — before it reaches a card.

## 4. Which approaches should it leave out?

Three families of methods are available, each summarized in one line:

- **evidence-based practices**: memory and practice techniques with support from trials and reviews;
- **Connected Learning**: interest-driven themes, peer roles, real-world links;
- **participatory budgeting**: class votes on real resource trade-offs.

You can exclude any of them at the outset. A phonics programme with a fixed method may want no additions at all; a civics unit may want everything. Exclusion is respected everywhere downstream: an excluded method never appears in a card.

## 5. For each unit, what fits?

For every unit, in order, the tool answers "applies" or "doesn't apply" for each surviving family, with a plain reason. A memory technique needs a matching step and all of its non-negotiables, or it stays out — a hollow version is worse than none. A class vote needs a real trade-off the class must decide; it is never put in a decoding drill or the teacher's own admin. "Doesn't apply" is the most common answer, and a good one.

## 6. Does the result pass review?

Now the tool turns strict reviewer. It checks the plan against 21 checks: no child data or scores recorded, no unsupervised trips or hazardous work, no real money through learners' hands, everything offline, no invented tactics or outcome claims, sustained writing and reasoning time kept. Failures get fixed, at most two rounds. If a serious failure won't fix, you get the original outline with the reasons instead of a polished bad plan.

## 7. Here are your cards.

The delivery is an overview card plus one card per unit: who does each step and what they do, what the unit relies on and the fallback if it doesn't hold ("Before you start"), what changed from the lesson and why, and what was set aside. A teacher should be able to run Monday's lesson from the card alone.

## Try it

LSB is free and open source. Try the questions on a real lesson, with no setup: open it in [ChatGPT]({{ site.data.try_links.chatgpt }}), [Claude]({{ site.data.try_links.claude }}) or [Google AI Mode]({{ site.data.try_links.google_ai_mode }}). Each link starts a new chat with the prompt already filled in. The [next post]({{ site.baseurl }}/what-it-takes-out/) covers what comes out of a lesson, and why.

{% include series.html %}
