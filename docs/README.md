# Lesson Scaffold Builder — Docs

*Turning lessons into teachable classroom plans.*

Plain-language documentation of what the Lesson Scaffold Builder (LSB) is for, how people would use it, and what it actually does to real-looking teaching material from six countries.

> **Read this first.** Every walkthrough below is **live output**: the pipeline was run on an original test lesson set in that country, and the walkthrough reports what came out, including what went wrong. Nothing is a hand-written "ideal answer". The lessons were written for this project to contain the kinds of problems real material has, and **no teacher or curriculum specialist has reviewed the output yet.** The locale handling in each walkthrough (generalized, kept, or relocalized terms) may be incorrect or incomplete: review it with the rest of the output to make sure the material is culturally and educationally appropriate and complete. There's no graphical interface; the pipeline runs from the command line.

## User experience
1. [Who uses it](ux/01-who-uses-it.md): curriculum adapters, teachers, school leaders, volunteers; who it's not for
2. [The end-to-end journey](ux/02-journey.md): from a lesson to printed teacher cards, and what happens at each stage
3. [Decision points and edge cases](ux/03-decision-points.md): what the pipeline does with unsafe activities, child data, money, regional names, pure lecture, deep work, and problems found late; the principles and open questions

## Walkthroughs: one per lesson

| # | Walkthrough | Subject | What the stages applied | What was removed or ruled out |
|---|---|---|---|---|
| 1 | [Kenya: clean water and health](walkthroughs/01-kenya-clean-water/) | Grade 6 science | Whole-class checks, recall from memory; rotating roles; a guide shown to younger pupils | Learners cutting bottles with a razor, pouring boiling water and climbing on the roof; a register of which families treat their water; an unsupervised lake trip; testing kits to buy |
| 2 | [Peru: fractions in the market and the garden](walkthroughs/02-peru-fractions/) | Grade 5 mathematics | Whole-class checks, recall; a showcase for a younger class; **a class vote on the garden bed with the rule announced first** | Pupils spending money at a market; family harvest income; scores posted by name |
| 3 | [Vietnam: folk tales and retelling](walkthroughs/03-vietnam-folk-tales/) | Grade 6 literature | Checks, recall, spaced review; an unranked class book | Children's videos sent to parents; winners named on the loudspeaker; visits to unknown neighbours; pupils selling a book. **Participatory budgeting: ruled out everywhere** |
| 4 | [Ghana: local government and community development](walkthroughs/04-ghana-local-government/) | JHS 2 social studies | A chalkboard diagram, a worked budget example, checks, recall; letters read to another class; **a mock vote counted two ways, with a report-back** | An unsupervised household survey with names and phone numbers; a real prefect election; pupils at a town hall alone; a cash fund with a pupil treasurer |
| 5 | [Bangladesh: letters, sounds and first words](walkthroughs/05-bangladesh-letters-and-sounds/) | Class 1 reading | Thumbs and finger checks, letters from memory, spaced review. **Connected Learning and participatory budgeting: ruled out everywhere** | Back benches and colouring sheets for children who can't yet read; a "slow readers" chart; a workbook to buy; nightly phone videos |
| 6 | [Mexico: migration stories, past and present](walkthroughs/06-mexico-migration/) | Grade 8 history | Finger and scrap-paper checks, recall; an unranked class book | Questions about families' legal documents; family photos with names; an unsupervised bus-terminal trip; paying for printing |
| 7 | [Hydrology: tracking rainfall](walkthroughs/07-hydrology/) | Middle science | A reading check, a worked example. **Connected Learning and participatory budgeting: ruled out everywhere** | Backyard recording at home; cloud lectures; multi-season tracking |
| 8 | [Ecosystems: energy flow and food webs](walkthroughs/08-ecosystems/) | Middle science | Checks, a worked example, a linked drawing; rotating pairs. **Participatory budgeting: ruled out everywhere** | Tablets; weekly photos for grading; insects in jars; field guides to buy; a planted instruction ignored |
| 9 | [Civics: making decisions together](walkthroughs/09-civics/) | Upper-secondary civics | Checks, recall, a worked example; a pooled chart, a reading; **a class ballot with the rule stated first** | Named votes; neighbourhood interviews; real-money fundraising; social-media photos; a planted instruction ignored |
| 10 | [Tanzania: multiplication and division practice](walkthroughs/10-tanzania-multiplication-division/) | Grade 4 mathematics | Checks, **level groups (new)**, a worked example, recall; theme choice, a class set; **a mock ledger vote** | Ranked scoreboard; workbook purchase; family earnings homework; fixed pairs; timed race; named scores sent out |
| 11 | [Philippines: how plants grow](walkthroughs/11-philippines-how-plants-grow/) | Grade 5 science | Checks, **asking-then-telling on why/how (new)**; rotating pairs, shared charts | Night observation; ranked growers chart; unsupervised riverbank trip with photos; rulers to buy; a planted instruction ignored |
| 12 | [ATREE S.N.A.I.L.: water source mapping](walkthroughs/12-snail-water-source-mapping/) | Grade 6 environmental studies | Slate checks, week-2 recall, a worked percent; observer/recorder pairs | Unsupervised source visits; home addresses in reports; touching water and waste |
| 13 | [ATREE S.N.A.I.L.: pond management](walkthroughs/13-snail-pond-management/) | Grade 9 environmental studies | Slate checks, week-2 recall; rotating Reader/Writer/Checker roles | Solo pond surveys; contact with waste and water; a town track set aside; pujas, place names, the network generalized |

Every walkthrough follows the same shape: **at a glance → the starting point → what the pipeline kept → what was removed and why → the units → what each stage did → what the reviewers caught → before/after → the teacher card → what to watch for**. Each lives in its own folder with the source lesson (`source.md`), the engine's decision trace (`decisions.md`: frameworks found relevant, what was asked and answered, and every changed step's before → after), the complete final cards (`final.md`), and three relocalized variants (`localizations.md`, with one `final-<locale>.md` per locale).

## Going deeper
- What the five evidence-based practices are, when they fit, and what supports them: [evidence-guide.md](evidence-guide.md)
- How to run, check and extend it: [technical.md](technical.md)
- Rebuild the whole project with an AI coding agent: [regeneration-prompts.md](regeneration-prompts.md)
- Exploratory design note on exporting runs to ShikshaLokam ELEVATE (nothing built): [integrations/elevate.md](integrations/elevate.md)
- The methods, as the pipeline reads them: [evidence-based practices](../frameworks/evidence-based-practices.md), [Connected Learning](../frameworks/connected-learning.md), [participatory budgeting](../frameworks/participatory-budgeting.md)
- The model prompts and how they're orchestrated: [prompts/README.md](../prompts/README.md)
- The test lessons and what each run must show: [tests/fixtures/README.md](../tests/fixtures/README.md), [tests/regression/cases.json](../tests/regression/cases.json)
