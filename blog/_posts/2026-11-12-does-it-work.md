---
title: "Does it work? How we'd find out"
description: "Every post in this series says no teacher has reviewed the cards and nothing shows they improve learning. What it would take to change that sentence: three steps, from a curriculum review to a classroom trial, and who does this kind of work."
layout: post
series: scaffold
date: 2026-11-12 00:00:00 +0000
---

*Part 8 of 8 in a series on [Lesson Scaffold Builder](https://github.com/ashitpatel/lesson-scaffold-builder).*

Every post in this series ends up saying the same thing: **no teacher or curriculum specialist has reviewed the tool's output, and nothing shows the cards improve learning.** That sentence is true, and it will stay true until someone tests the tool. This post sets out what a test would look like and who does this kind of work. The full plan is in the repository's [evaluation protocol](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/docs/evaluation-protocol.md).

## Two questions, not one

"Does it work?" hides two questions.

**Do the teaching methods work?** Mostly answered elsewhere. The nine evidence-based practices in [part 4]({{ site.baseurl }}/what-it-adds/) were chosen because reviews and trials support them. That evidence comes mainly from high-income classrooms; Teaching at the Right Level, tested in Indian schools, is the exception.

**Do the cards work?** Nobody knows. A practice can work in a study and still fail on a card, if teachers skip the step, run a hollow version of it, or never get the cards at all. This is the question a test has to answer.

There is a trap between the two. Reviews of what works for learning in low- and middle-income countries rate *structured pedagogy* among the best buys. It sounds like a description of this tool, but in those reviews it means a package: lesson plans, learning materials, and ongoing support for teachers, such as coaching. The cards are only the lesson plans. That evidence can't be borrowed for them.

## Three steps, in order

Each step has to pass before the next one starts. A trial of cards that teachers don't use measures nothing.

**1. Review on real lessons.** So far the tool has been run only on [test lessons](https://github.com/ashitpatel/lesson-scaffold-builder/tree/main/docs/walkthroughs) written for this project. The first step is a partner's own textbook units, reviewed by its curriculum specialists and experienced teachers. They check whether the goal of each unit survived, whether anything was removed that shouldn't have been, and whether anything unsafe slipped through. A missed safety problem is a bug to fix before going further, however good the rest looks.

**2. A short classroom pilot.** A few dozen classrooms run the cards for one unit cycle, about a month. There's no comparison group yet: the question is whether teachers use the cards as designed. Did they run the steps? Was the quiz really left unmarked? Did every student answer the understanding check, or only the quick ones? How long did preparation take, compared with usual? A practice that is delivered hollow isn't being tested at all.

**3. A trial.** Only then is it worth comparing schools that get the cards with schools that don't, over at least a term, with one main outcome chosen in advance. The schools are chosen at random, by school rather than by teacher, because teachers in the same school share cards. The trial is designed and run by researchers, not by this project.

## What would be tested

The raw output of a pipeline isn't something to test. What would be tested is the thing that would actually reach a classroom: cards made from a partner's own curriculum, **checked by a person at the partner before printing**, and then frozen. The cards are generated once, and the version and model are recorded. Nobody re-runs or tweaks them partway through, because a test of something that keeps changing tests nothing.

Cost counts too. A small gain that costs little can be worth more than a large gain that costs a lot. The cost of each unit includes the model run, the reviewer's time, printing and teachers' preparation, and it is recorded from the pilot on.

## Who does this kind of work

None of these organisations has reviewed or endorsed this tool. They are where this kind of evidence comes from:

- **[J-PAL](https://www.povertyactionlab.org/)** is a network of university researchers who run randomised evaluations. The Teaching at the Right Level trials behind the level-groups card are their work, with the Indian NGO Pratham.
- **[IPA](https://poverty-action.org/)** runs field trials through its country offices, and helps implementers set up monitoring before anyone pays for a trial. That is the stage of steps 1 and 2.
- **[CEGA](https://cega.berkeley.edu/)** at UC Berkeley works on how studies are done: writing the analysis plan before seeing the data, and counting costs properly.
- **The [Global Education Evidence Advisory Panel](https://www.worldbank.org/en/topic/teachingandlearning/publication/cost-effective-approaches-to-improve-global-learning)** compares approaches to learning by cost-effectiveness. It's the source of the "best buys" above.
- **The [What Works Hub for Global Education](https://www.bsg.ox.ac.uk/research/what-works-hub-global-education)** studies why approaches that work in trials often stop working when governments scale them up.

## If your organisation adapts lessons

Researchers rarely test a tool on its own. They work with an organisation that delivers it: an NGO programme, a district team or a ministry. If that's you, they will look for three things:
- schools you can reach;
- a willingness to bring them in in a random order;
- outcome data you already collect, such as term assessments.

Run step 1 on your own units first. With your specialists' findings in hand, you can show researchers what you found instead of just promising results. The protocol includes an [email template](https://github.com/ashitpatel/lesson-scaffold-builder/blob/main/docs/evaluation-protocol.md#approaching-a-research-team) for the first contact. It keeps the tool's claims to what has actually been shown, and it contains no student data.

## What even a good trial won't say

A trial would give one result, for one system, one version and one setting. It wouldn't show which card did the work, because a whole set of cards is tested together. It wouldn't settle whether the cards work anywhere else. That is still more than anyone knows today. It would also show whether reviewed, automated adaptation of a school system's own curriculum is a sensible way to get good practices into classrooms.

Corrections and reports are welcome as [issues](https://github.com/ashitpatel/lesson-scaffold-builder/issues). The series starts [here]({{ site.baseurl }}/from-lesson-to-classroom/).

{% include series.html %}
