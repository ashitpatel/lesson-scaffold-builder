---
title: "Tweak it next week: revising cards after they print"
description: "Cards assume things your classroom doesn't have. lsb-refine revises a finished run's wording turn by turn — one instruction at a time, each turn checked and re-reviewed, revisions accumulating over days."
layout: post
series: scaffold
date: 2026-11-09 00:06:00 +0000
---

*Part 7 of 8 in a series on [Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder).*

The cards assume chart paper you don't have, 45-minute periods you don't get, and volunteers who never show up. And needs don't all surface on Sunday: on Monday you learn the chart paper is gone, on Wednesday that periods are 30 minutes, next term that a new class needs simpler wording. A plan you can't revise is a plan you'll abandon — so the tool treats printed cards as a living draft, not a finished product.

## One instruction per turn

Point `lsb-refine` at a finished run folder and the source lesson, and say the change in your own words:

```bash
lsb-refine my-lesson.md runs/my-run-1 --instruction "Use pencils instead of chalk wherever chalk is named."
```

Each instruction becomes one numbered revision — `rev1`, `rev2`, and so on — saved beside the original, which is never overwritten. Turns accumulate over sessions and days: come back next week with the next constraint. `--ask` converses instead of taking flags, `--unit` confines edits to one scaffold, and `--base` replays from any earlier revision when a tweak goes wrong.

## What each turn guarantees

A tweak that quietly breaks the cards is worse than no tweak. So every turn runs the same discipline as the pipeline, scoped to the edit:

- **Only touched steps change.** Units, steps, titles, dependencies, weeks, and roles are fixed; the reply must keep the same shape with nothing emptied, or it is refused and the run stays untouched.
- **The edit is re-reviewed.** The critic checks the changed steps fully — and safety, privacy, and money issues anywhere, since a rewording can always hide one — while pre-existing wording elsewhere is set aside as notes instead of blocking the tweak.
- **Cards are re-printed and recorded.** The revision folder holds the new cards plus a record of what changed and why, in the run's own language, with locale terms you approved earlier left alone.

A real turn from testing: asked for pencils instead of chalk on a French reading lesson, the tool changed one tracing step (*"l'écrivent cinq fois au crayon sur du papier"*), re-printed the cards, and wrote down what it did — in French, like the cards.

## What it won't do

Step wording only. It can't add a unit, move weeks, or restructure the plan: anything that changes the shape needs a fresh run, not a tweak. It needs the run folder and a model backend, and every turn is still reviewed — even a small tweak can be refused, and that refusal is the feature working, not failing. As with everything the tool makes, read the revised cards before they reach a classroom: no teacher has reviewed this output yet.

Small plans, revised often, beat big plans revised never. That was the idea behind borrowing the scaffold's shape from [Shikshagraha's](https://shikshagraha.org/) Micro-Improvement Plan in [part 1]({{ site.baseurl }}/from-lesson-to-classroom/) — and it applies to the cards themselves.

The [next post]({{ site.baseurl }}/does-it-work/) asks how anyone would find out whether the cards help.

Corrections and reports are welcome as [issues](https://github.com/ashitpatel/lesson-scaffold-builder/issues).

{% include series.html %}
