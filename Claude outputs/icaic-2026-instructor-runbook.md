# ICAIC 2026 — Internal Planning Document

**For coaches and support staff. Not for student circulation.**

| | |
|---|---|
| **Event** | International Collegiate AI Contest (ICAIC) 2026, Singapore, Dec 6–12, 2026 |
| **Host** | NUS School of Computing ([icaic.sg](https://icaic.sg/index.php)) |
| **Our entry** | 1 team leader + 3 undergraduate students, registered and paid |
| **Student-facing page** | `post/icaic-2026.html` on chandra-gummaluru.github.io |
| **Owner / last updated** | `[NAME]` — `[DATE]` |

---

## 1. What we are doing

We are selecting three U of T undergraduates to compete at ICAIC 2026, then training them weekly until departure. Selection runs in four stages: **application → qualifier → interview → selection**. The public page carries what students need; this document carries what we need.

| Stage | What happens | Owner |
|---|---|---|
| Application | Online form, screened for eligibility | `[NAME]` |
| Qualifier | 3-hour in-person Kaggle-style contest on department machines, auto-graded | `[NAME]` |
| Interview | 30 minutes, 2–3 panel members, technical + behavioural, scored against a rubric | `[NAME]` |
| Selection | Qualifier and interview combined; three students plus two alternates | `[NAME]` |
| Training | Weekly sessions from selection to departure, qualifier-style problems | `[NAME]` |

**Hard external deadline:** participant details (names, emails, dietary requirements, t-shirt sizes, phone numbers) are due to ICAIC by **October 31, 2026**. Everything else works backwards from that.

---

## 2. Dates and deadlines

| # | Milestone | Date | Owner |
|---|---|---|---|
| 1 | Roles confirmed, dates locked, website updated with real dates | `[DATE]` | `[NAME]` |
| 2 | Application form live; publicity begins | `[DATE]` | `[NAME]` |
| 3 | Qualifier problem drafted; baseline runs end to end | `[DATE]` | `[NAME]` |
| 4 | Lab booked; machine image and browser allow-list confirmed with IT | `[DATE]` | `[NAME]` |
| 5 | **Applications close** | `[DATE]` | `[NAME]` |
| 6 | Eligibility screened; qualifier invitations sent | `[DATE]` (within 48h of #5) | `[NAME]` |
| 7 | Kaggle competition live; dry run complete | `[DATE]` (≥3 days before #8) | `[NAME]` |
| 8 | **Qualifier** | `[DATE]`, `[TIME]`, `[ROOM]` | `[NAME]` |
| 9 | Private leaderboard final; shortlist agreed; interview invitations sent | `[DATE]` (within 48h of #8) | `[NAME]` |
| 10 | **Interviews** | `[DATES]` | `[NAME]` |
| 11 | Selection meeting; three students + two alternates chosen | `[DATE]` | `[NAME]` |
| 12 | Students notified; written acceptances received | `[DATE]` | `[NAME]` |
| 13 | **Participant details submitted to ICAIC** | **Oct 31, 2026** | `[NAME]` |
| 14 | Weekly training begins | `[DATE]` | `[NAME]` |
| 15 | Passport and visa check complete | `[DATE]` (≥8 weeks before travel) | `[NAME]` |
| 16 | Flights and accommodation booked | `[DATE]` | `[NAME]` |
| 17 | **ICAIC 2026** | **Dec 6–12, 2026** | — |

**Two dates to watch.** The critical path is #5 → #8 → #10 → #12 → #13; a slip anywhere puts October 31 at risk. And the December exam period overlaps the competition week, so check the selected students' exam schedules at stage #11, not later.

**Contingency qualifier date:** `[DATE]` — held in case of a lab, network or platform failure.

---

## 3. What we need to set up

### 3.1 Application form

**Platform:** Microsoft Forms in the U of T tenant, so student identifiers stay inside the university. Responses export to `[SECURE LOCATION]`.

| Field | Type |
|---|---|
| Full name | Text, required |
| U of T email | Text, required |
| Student number | Text, required |
| UTORid | Text, required (used for lab accounts) |
| Program / major | Text, required |
| Year of study | Choice: 1 / 2 / 3 / 4 / 5+ |
| Available to travel to Singapore, Dec 6–12, 2026 | Yes / No |
| Able to commit to weekly training if selected | Yes / No |
| Confirms responsibility for own legal eligibility to travel (passport, visa) | Checkbox, required |
| Accessibility needs for a 3-hour in-person contest | Long text, optional |
| Anything else we should know | Long text, optional |

**Also needed:** the form URL added to the website; a shared mailbox or alias for applicant questions; publicity through `[MAILING LISTS, COURSES, STUDENT GROUPS, POSTERS]`.

**Screening:** current undergraduate, enrolled through December 2026, yes to both availability questions, checkbox confirmed. Everyone eligible is invited to the qualifier; everyone else gets the decline in B.2.

### 3.2 Qualifier

**Platform: Kaggle Community Competition** (free, private/invite-only). It gives us the leaderboard, the public/private split and the scoring without building anything.

Setup:

- [ ] Competition created under `[KAGGLE ACCOUNT]`, visibility private
- [ ] Data uploaded: training set, test features, sample submission, hidden ground truth
- [ ] Metric set to `[METRIC]`; split set to `[30]%` public / `[70]%` private, stratified where the label is imbalanced
- [ ] Submission limit raised to the platform maximum, and the actual number recorded
- [ ] Timer set to open and close with the sitting, plus a `[10]`-minute upload grace period
- [ ] Competition description matches the student page: metric, split, what to submit
- [ ] Student accounts / invite links prepared under **pseudonymous names** (`icaic-2026-###`), mapped to UTORids in a restricted internal sheet so no student identifiers reach Kaggle
- [ ] Channel for code and write-ups decided: `[e.g. private Kaggle notebook shared with the host account]`

Room and machines:

- [ ] `[LAB]` booked for the sitting plus an hour either side; `[N]` seats confirmed against the number of invitees
- [ ] Departmental machines only; `[N]` spares reserved
- [ ] Standard image with Python `[VERSION]` and `[PACKAGES]` as a fallback if Kaggle Notebooks are unavailable
- [ ] Browser allow-list with IT: `kaggle.com`, `www.kaggleusercontent.com`, `[DOCS SITES?]`; everything else blocked, including email, messaging and general-purpose AI assistants
- [ ] USB storage disabled; accounts reset to a clean state
- [ ] Proctors confirmed: one per `[20]` students, minimum two
- [ ] Accommodations arranged for anyone who asked, with extra time run on a staff clock (Kaggle's timer is global)

Problem and grading:

- [ ] Problem written (see Appendix C for the spec template)
- [ ] Dry run at least 3 days out: someone who has not seen the problem completes it on a lab machine and appears on the leaderboard; baseline timing recorded
- [ ] Local fallback grader ready: scores a folder of submissions against the ground truth with the same metric and split, used if Kaggle fails and as an independent check on the final ranking

Two things to settle before invitations go out:

1. **Submissions.** The student page says students can submit as often as they like, but Kaggle caps submissions per day. Either raise the cap beyond anything reachable in three hours, or publish the cap and amend the page.
2. **AI assistants.** Assumed **not permitted** and enforced by the allow-list. This is the first thing students will ask, so it needs to be stated in the invitation and the briefing.

### 3.3 Interviews

- [ ] Panel of 2–3 confirmed, with at least one member in every interview for consistency
- [ ] Format decided: in person or Zoom
- [ ] Slots and booking link for `[DATES]`
- [ ] Rubric (Appendix A) circulated to the panel; each member scores independently before discussion
- [ ] Conflicts of interest declared before scoring

### 3.4 Training

- [ ] Room and weekly slot booked: `[DAY, TIME, ROOM]`
- [ ] Compute for students between sessions: `[DEPARTMENT GPUs / COLAB / KAGGLE / CLOUD CREDITS]`
- [ ] Problem sources lined up (past Kaggle competitions, ICAIC syllabus, problems written by `[NAMES]`)
- [ ] Two full-length simulations scheduled before departure: one 7-hour team, one 5–7 hour individual
- [ ] Alternates invited to all sessions

---

## 4. Selection

Both signals count. Draft weighting: **`[50]%` qualifier** (normalised private-leaderboard rank) and **`[50]%` interview** (weighted rubric total).

- The stated preference for third- and fourth-year students applies only as a tie-break between closely ranked candidates, exactly as the public page describes.
- The panel may adjust for team composition; three people who work well together beat three strong individuals who don't. Any adjustment gets written down with the reasoning.
- Name **three students and two alternates**, in order. Alternates attend training, which is what makes them useful when someone withdraws or a visa is refused.
- Keep a short selection log: shortlist reasons, conflicts declared, weighting used, final decisions, date each student was told.

---

## 5. Open decisions

| # | Decision | Owner | Needed by |
|---|---|---|---|
| 1 | All dates in Section 2 | `[NAME]` | Before the page goes live |
| 2 | Kaggle submission cap vs the website wording | `[NAME]` | Before invitations |
| 3 | AI coding assistants permitted? (default: no) | `[NAME]` | Before invitations |
| 4 | Public pretrained models and weights permitted? | `[NAME]` | Before the problem is final |
| 5 | Qualifier / interview weighting (draft 50/50) | `[NAME]` | Before the selection meeting |
| 6 | Shortlist size for interviews (draft 8–10) | `[NAME]` | Before shortlisting |
| 7 | Compute for students during training | `[NAME]` | Before week 1 |
| 8 | What the department covers for travel, and how it is worded to students | `[NAME]` | Before offers |
| 9 | Lab, machine image and IT contact | `[NAME]` | 2 weeks before the qualifier |
| 10 | Interviews in person or on Zoom | `[NAME]` | Before invitations |

---

## Appendix A — Interview score sheet

**Candidate:** `[NAME]`  **Interviewer:** `[NAME]`  **Date:** `[DATE]`

Score each 1–5 independently, before any discussion. Weights in brackets.

| Dimension | 1 | 3 | 5 | Score |
|---|---|---|---|---|
| Technical depth and ML judgement `[30%]` | Struggles to explain their own approach | Solid grasp of standard methods, sensible validation | Deep; makes principled choices and knows the failure modes | |
| Problem solving under pressure `[20%]` | Froze or thrashed in the qualifier | Steady progress with a reasonable plan | Prioritised well, iterated quickly, knew when to stop tuning | |
| Communication and clarity `[20%]` | Hard to follow; jargon without meaning | Clear; answers the question asked | Explains complex work so a non-specialist follows it | |
| Collaboration and coachability `[20%]` | Dismissive of others; defensive about feedback | Works fine in a team, takes feedback | Actively makes a team better; seeks out and acts on feedback | |
| Commitment and availability `[10%]` | Unclear about the time commitment | Available; understands what is being asked | Fully committed; has thought about how to make it work | |

**Weighted total:** `[ ]`  **Would you want them in the room for seven hours? (yes / no / maybe):** `[ ]`

**Evidence and notes:**

**Conflicts of interest declared:**

### Question bank

*Technical.* Walk us through your qualifier approach: why that model, how you validated, what you would do with another hour. What relevant courses, projects, research or internships have you done? Then one or two fundamentals arising from their answers: overfitting and validation, class imbalance, where a model would fail in deployment. Finally, breadth across the ICAIC syllabus: which of LLMs, vision, RL, data science, multimodal and systems they have actually touched.

*Behavioural.* Tell us about a team project that went badly; what did you do? How do you divide work when everyone wants the interesting part? Describe explaining something technical to someone without your background. Tell us about a time you were wrong and how you found out. What would make this week worthwhile for you?

---

## Appendix B — Email templates

### B.1 Qualifier invitation

> Subject: ICAIC 2026 qualifier — `[DATE]`, `[TIME]`, `[ROOM]`
>
> Hi `[NAME]`,
>
> Thanks for applying to represent U of T at the International Collegiate AI Contest. You are eligible, so the next step is our internal qualifier.
>
> **When:** `[DATE]`, `[START]`–`[END]` (three hours)
> **Where:** `[ROOM]`. Please arrive by `[TIME]` with your TCard.
>
> You will get a machine learning problem with a dataset and a clear evaluation metric, and three hours to build the best model you can. A few things to know:
>
> - You will work on a departmental machine. Bring nothing but yourself and your TCard.
> - Submissions are graded automatically against hidden test data. A live leaderboard shows part of it; final rankings use a separate part you will not see.
> - Submit your code and a short write-up of your approach along with your final submission.
> - Work is individual: no collaboration and no AI assistants. The machines are set up so that only the contest platform is reachable.
>
> Please reply by `[DATE]` to confirm you will be there. If you need an accommodation for the sitting, tell me as soon as possible.
>
> `[SIGNATURE]`

### B.2 Application declined (ineligible)

> Subject: ICAIC 2026 application
>
> Hi `[NAME]`,
>
> Thanks for your interest in the ICAIC 2026 team. Unfortunately we cannot take your application forward, because `[REASON: the contest is open to undergraduates only / it requires enrolment through December 2026 / it requires availability to travel December 6–12]`.
>
> I am sorry for the disappointing answer, and I hope you will keep an eye out for future opportunities like this one.
>
> `[SIGNATURE]`

### B.3 Offer

> Subject: You're on the U of T team for ICAIC 2026
>
> Hi `[NAME]`,
>
> Congratulations. We would like you to be one of the three students representing U of T at ICAIC 2026 in Singapore, December 6–12.
>
> What this involves:
>
> - Competing in both the individual and team events at the contest.
> - Weekly training with the team from `[DATE]` until we leave, roughly `[N]` hours a week including work between sessions.
> - Travel arranged and supported by the department. You are responsible for holding a valid passport and any visa you need; we will help with supporting letters.
>
> Please confirm in writing by `[DATE]` that you accept. I also need `[dietary requirements, t-shirt size, phone number with country code]` for the organisers, and your agreement to us naming you publicly as a team member.
>
> `[SIGNATURE]`

### B.4 Alternate

> Subject: ICAIC 2026 — alternate
>
> Hi `[NAME]`,
>
> Thank you for everything you put into the qualifier and interview. The decisions were close, and I would like you to join the team as `[first/second]` alternate.
>
> In practice: you are invited to all of the weekly training sessions, and if one of the three students cannot travel, you take their place. That does happen, and it usually happens late, so the training matters.
>
> Let me know by `[DATE]` whether you would like to take this up.
>
> `[SIGNATURE]`

### B.5 Not selected

> Subject: ICAIC 2026 — outcome
>
> Hi `[NAME]`,
>
> Thank you for taking part in the qualifier `[and interview]` for ICAIC 2026. We had a strong field for three places, and on this occasion you were not selected.
>
> That is a genuinely difficult result after the work you put in. If it would be useful, I am happy to give you feedback on your qualifier submission `[and interview]` — just reply and we will find a time.
>
> `[SIGNATURE]`

---

## Appendix C — Qualifier problem spec (placeholder)

> Replace with the real problem once written. Keep the structure: the Kaggle description, the student briefing and the fallback grader all draw from it.

**Title:** `[PROBLEM TITLE]`

**One-line description:** `[e.g. predict X from Y, given a tabular dataset of N rows]`

**Task type:** `[binary classification / multi-class / regression / ranking]`

| File | Rows | Columns | Notes |
|---|---|---|---|
| `train.csv` | `[N]` | `[M]` | Labelled |
| `test.csv` | `[N]` | `[M−1]` | Unlabelled; the label is what we score |
| `sample_submission.csv` | `[N]` | 2 | Format example |

**Data provenance and licence:** `[SOURCE, LICENCE]`. Confirm we may redistribute it and that a labelled public copy is not findable online.

**Metric:** `[e.g. macro F1 / RMSE / AUC]`, chosen because `[reason]`.

**Split:** `[30]%` public leaderboard, `[70]%` private, stratified by `[COLUMN]`. Seed recorded in `[LOCATION]`.

**Baseline:** `[e.g. gradient-boosted trees with defaults]`, score `[VALUE]`, runtime `[MINUTES]` on a lab machine. Students should beat this comfortably; if they cannot, the problem is too hard for three hours.

**Target difficulty:** a competent third-year student reaches a reasonable score within `[60]` minutes, with the rest of the time separating the field. Confirm in the dry run.

**Student deliverables:** submission file, code, and a `[3–5]` sentence write-up.

**Integrity notes:** `[pretrained models allowed or not; any findable public version of the dataset; anything else lookupable]`

**Fallback grader:** `[SCRIPT PATH]` reproduces the metric and split from the saved ground truth.
