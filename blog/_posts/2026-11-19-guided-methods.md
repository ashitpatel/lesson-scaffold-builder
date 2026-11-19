---
title: "Tell it your goals; it proposes the methods"
description: "Teachers shouldn't need to know what NSSA dosage or uptake moves are to get good cards. How LSB interviews you in plain language, explains every option, and shows what will and won't apply before spending anything."
layout: post
series: scaffold
date: 2026-11-19 00:00:00 +0000
---

*Part 9 of 9 in a series on [Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder).*

[Part 4]({{ site.baseurl }}/what-it-adds/) listed twenty-one teaching methods the tool can apply. That post was written for reviewers. This one is for the teacher being asked, at the start of a run, *which of these do you want?* — a question that is unfair as stated, because no teacher should need to know what NSSA dosage or uptake moves are before breakfast. So the tool no longer asks it that way. It asks what you want for your classroom, proposes methods to match, and lets you interrogate every option before anything runs.

## Goals first, methods second

Run with `--ask` and the methodology section opens with one question in plain language: which goals matter — finding where strugglers are stuck, more students talking, lessons tied to real surroundings, more ways in and out, students judging AI tools. Pick any, or nothing. The next question then proposes method families with numbered picks:

```
Based on your goals (Find where strugglers are stuck), suggested: 1, 5 — peer tutoring (extra practice in steady pairs); ROAR screening (browser check per student).
Each applies only above its threshold (checked next). Type suggested numbers, adjust, or blank for none.
```

The proposal is advice, not a decision. Type the numbers, change them, or leave everything blank for the standard pipeline. If your grade band already rules something out, the proposal says so on the spot rather than letting you pick it and fail later.

## Every option explains itself

Type `?N` on any option and it answers four questions: what it is, what it demands, what changes on your cards, and where to read more. For example, `?5`:

```
What: each child completes a short browser reading check; the teacher regroups from it.
Demands: one browser device per student + internet, Primary band. Nothing recorded.
Changes: one screening step, marked with its tech needs.
More: docs/methodologies.md.
```

The "more" pointer lands on the [methodologies guide](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/docs/methodologies.md): triage, thresholds, what changes on your cards, and the inspected primary source behind each method. The evidence guide covers the older practices the same way. Nothing here requires trusting the tool's word.

## The preview before the bill

After five short inventory questions (sessions per week, steady tutor, devices, internet, home access — each explaining what it gates), the run prints a methodology check *before the first model call*, so comparing answers costs nothing:

```
Methodology check (based on your answers):
• Peer tutoring protocol: will be considered for fitting units.
• ROAR screening: not offered — one browser device per student; Primary grade band.
• AI literacy: not offered — High grade band.
Details: docs/methodologies.md.
```

Read a rejection as information, not failure. "Not offered" always names the missing factor, and each factor suggests its own remedy: more sessions, a steady tutor, devices, or — for grade-band mismatches — nothing to do, the method genuinely doesn't fit. You can overrule the proposal and opt into anything; the thresholds still apply, enforced in code, so a weak version can never slip through. (Automated sweeps skip the whole interview and answer from a file.)

One honest limit: this is guided choice, not conversation. The tool cannot discuss trade-offs with you; for that, read the linked guides, which were written to be read. What it can do — propose from goals, explain every option, and show its reasoning before spending your money — is now the default way in.

Corrections and reports are welcome as [issues](https://github.com/ashitpatel/lesson-scaffold-builder/issues). The series starts [here]({{ site.baseurl }}/from-lesson-to-classroom/).

{% include series.html %}
