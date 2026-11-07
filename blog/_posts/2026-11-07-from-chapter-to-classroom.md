---
title: "From chapter to classroom: the Sunday-evening problem"
description: "Textbook chapters are written for an ideal classroom. Teachers spend their Sundays turning them into something runnable with forty pupils and a piece of chalk. A free tool that does the first draft, and says what it took out and why."
layout: post
series: scaffold
date: 2026-11-07
---

*Part 1 of 6 in a series on [Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder), a free, open-source tool that turns long teaching chapters into short, runnable classroom sequences.*

Every teacher knows the Sunday-evening problem. The chapter for next week is twenty pages of lecture, written for a classroom with small groups, ready materials and pupils who all learned last term's content. Your classroom has forty pupils, a piece of chalk, and a week lost to exams. Somewhere between the chapter and Monday morning, you turn one into the other, by hand.

This gap is not a personal failing. It is structural. Curricula in many systems move faster than students can learn, which is one reason learning stalls ([Pritchett & Beatty, 2015](https://github.com/ashitpatel/lesson-scaffold-builder#references)). The World Bank and partners estimate that around 70% of 10-year-olds in low- and middle-income countries can't read and understand a simple text ([*State of Global Learning Poverty: 2022 Update*](https://github.com/ashitpatel/lesson-scaffold-builder#references)). And chapters keep assuming the ideal room: the trip, the bought materials, the homework that needs a parent who can help.

## What a chapter asks for that a classroom can't give

The test chapters behind this project were written to carry the things real chapters carry. A science unit sends learners to collect water alone and pour boiling water. A maths unit posts weekly test scores by name "so pupils can see who is ahead". A letters unit keeps a wall chart of slow readers. A migration unit asks for the family's migration status and shares children's videos in a parents' group. Two chapters include a line addressed to automated systems.

A teacher reading any of these makes a hundred quiet decisions: skip that, replace this, that needs an adult present, that needs money nobody has. The decisions are the work. They take the Sunday.

## What Lesson Scaffold Builder does

[Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder) (LSB) does a first draft of those decisions, in the open. You give it a chapter. It returns a small set of Micro-Lesson Scaffolds: 2-to-4-week sequences of 3 to 7 steps each, printed as offline teacher cards. Along the way it:

- **takes out** what is unsafe, costly, region-specific, or a risk to children's privacy, and lists everything it removed;
- **adds** teaching methods only where they genuinely fit — memory and practice techniques with trial support, peer and interest-driven designs, class votes on real trade-offs — or abstains;
- **checks** the result against 21 checks, including safety, money, offline use and whether deep work survived, and refuses to print cards that fail.

Every step is traced to the chapter section it came from, every change is tagged with the method that made it, and every unit says what it relies on and what to do if that doesn't hold. Nothing is hidden: the [nine walkthroughs](https://github.com/ashitpatel/lesson-scaffold-builder/tree/main/docs/walkthroughs) show full inputs and outputs.

## What it doesn't do

It is a working prototype, and this series will keep saying so. **No teacher or curriculum specialist has reviewed its output yet**, and nothing here shows the cards improve learning. The list of teaching methods is a project choice that needs review by the people who own the content. The cards are a starting draft for a teacher's judgment, not a replacement for it.

I wrote this series the same way the tool works: I set the direction and made the editorial calls, and an AI agent drafted the posts. Corrections are welcome as [issues](https://github.com/ashitpatel/lesson-scaffold-builder/issues).

## What's next

The rest of the series covers the questions the tool asks before planning anything, what it takes out of a chapter and why, what it adds and when it refuses, the nine test chapters with before-and-after cards, and how to run it or adapt it to your school — free, including in a browser with no account.

**Try it now**, no setup needed: open it in [ChatGPT]({{ site.data.try_links.chatgpt }}), [Claude]({{ site.data.try_links.claude }}) or [Google AI Mode]({{ site.data.try_links.google_ai_mode }}).

{% include series.html %}
