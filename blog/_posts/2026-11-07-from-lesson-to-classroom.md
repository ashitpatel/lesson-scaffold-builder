---
title: "From lesson to classroom: the Sunday-evening problem"
description: "Textbook lessons are written for an ideal classroom. Teachers spend their Sundays turning them into something runnable with forty pupils and a piece of chalk. A free tool that does the first draft, and says what it took out and why."
layout: post
series: scaffold
date: 2026-11-07
---

*Part 1 of 8 in a series on [Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder), a free, open-source tool that turns long lessons into short, runnable classroom sequences.*

Every teacher knows the Sunday-evening problem. The lesson for next week is twenty pages of lecture, written for a classroom with small groups, ready materials and pupils who all learned last term's content. Your classroom has forty pupils, a piece of chalk, and a week lost to exams. Somewhere between the lesson and Monday morning, you turn one into the other, by hand.

This gap is not a personal failing. It is structural. Curricula in many systems move faster than students can learn, which is one reason learning stalls ([Pritchett & Beatty, 2015](https://github.com/ashitpatel/lesson-scaffold-builder#references)). The World Bank and partners estimate that around 70% of 10-year-olds in low- and middle-income countries can't read and understand a simple text ([*State of Global Learning Poverty: 2022 Update*](https://github.com/ashitpatel/lesson-scaffold-builder#references)). And lessons keep assuming the ideal room: the trip, the bought materials, the homework that needs a parent who can help.

## What a lesson asks for that a classroom can't give

The test lessons behind this project were written to carry the things real lessons carry. A science unit sends learners to collect water alone and pour boiling water. A maths unit posts weekly test scores by name "so pupils can see who is ahead". A letters unit keeps a wall chart of slow readers. A migration unit asks for the family's migration status and shares children's videos in a parents' group. Two lessons include a line addressed to automated systems.

A teacher reading any of these makes a hundred quiet decisions: skip that, replace this, that needs an adult present, that needs money nobody has. The decisions are the work. They take the Sunday.

## What Lesson Scaffold Builder does

[Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder) (LSB) does a first draft of those decisions, in the open. You give it a lesson. It returns a small set of Micro-Lesson Scaffolds: 2-to-4-week sequences of 3 to 7 steps each, printed as offline teacher cards. Along the way it:

- **takes out** what is unsafe, costly, region-specific, or a risk to children's privacy, and lists everything it removed;
- **asks** how to handle region-specific content: generalize it to generic labels (the default), keep the lesson's own locale, or generalize it and then relocalize to your setting — you name the target locale, add notes about it, and review each proposed replacement before it reaches a card; it can also suggest new locale details to add where the lesson was already generic, and print the final cards in your language;
- **adds** teaching methods only where they genuinely fit — memory and practice techniques with trial support, peer and interest-driven designs, class votes on real trade-offs — or abstains;
- **checks** the result against 21 checks, including safety, money, offline use and whether deep work survived, and refuses to print cards that fail.

Every step is traced to the lesson section it came from, every change is tagged with the method that made it, and every unit says what it relies on and what to do if that doesn't hold. Nothing is hidden: the [thirteen walkthroughs](https://github.com/ashitpatel/lesson-scaffold-builder/tree/main/docs/walkthroughs) show full inputs and outputs.

## What a card looks like

A run prints an overview card (the lesson's goal and the units, with what each builds on) and then one card per unit, each a single page of plain text, black on white. This is part of a unit card from the Peru fractions lesson, shortened:

```
MLS-FRAC-01: What a Fraction Is and Folding Equivalent Fractions
2 weeks. Starts fresh (no earlier unit needed).
Goal: Gives pupils a set of labelled paper strips and the multiplying rule, so
they can represent any fraction and write it in equivalent ways.

WHO                   WHAT TO DO
2. Lead Educator      Give each pupil three strips of reused paper of the same
                      length. Each pupil folds one strip into halves, one into
                      quarters and one into eighths. …
5. Lead Educator      Work four examples on the board … Then every pupil
[changed: EB-04]      writes a fraction equivalent to 3/5 on scrap paper and
                      holds it up at the same time. …

BEFORE YOU START
- Needs: Enough reused paper to give each pupil five strips of the same
  length.
  If not: Cut strips from the backs of old worksheets or newspaper margins, …

CHANGES FROM THE SOURCE
- Evidence-Based, EB-04 Checking for Understanding: after the four worked
  examples, every pupil writes and holds up a fraction equivalent to 3/5 …
```

Every unit card has the same parts: who does each step and what, what the unit relies on and what to do if it isn't there, and every change the tool made. A tag such as `[changed: EB-04]` names the teaching method that changed the step. Each method is itself written as a strict rule, called a method card, which [part 4]({{ site.baseurl }}/what-it-adds/) describes. In this series, *cards* on their own always means the printed teacher cards.

The scaffold's shape — small, time-bound, owned by the teacher — is borrowed from [Shikshagraha's](https://shikshagraha.org/) Micro-Improvement Plan, from the movement now running over a million micro-improvements across India's public schools.

## What it doesn't do

It is a working prototype, and this series will keep saying so. **No teacher or curriculum specialist has reviewed its output yet**, and nothing here shows the cards improve learning. The list of teaching methods is a project choice that needs review by the people who own the content. The cards are a starting draft for a teacher's judgment, not a replacement for it. How to find out whether they help, step by step, is set out in an [evaluation protocol](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/docs/evaluation-protocol.md).

I wrote this series the same way the tool works: I set the direction and made the editorial calls, and an AI agent drafted the posts. Corrections are welcome as [issues](https://github.com/ashitpatel/lesson-scaffold-builder/issues).

## What's next

The rest of the series covers the questions the tool asks before planning anything, what it takes out of a lesson and why, what it adds and when it refuses, the thirteen test lessons with before-and-after cards, how to run it or adapt it to your school — free, including in a browser with no account — how to revise cards after they print, and how anyone would find out whether they help.

**Try it now**, no setup needed: open it in [ChatGPT]({{ site.data.try_links.chatgpt }}), [Claude]({{ site.data.try_links.claude }}) or [Google AI Mode]({{ site.data.try_links.google_ai_mode }}).

{% include series.html %}
