# ICAIC 2026 Application Form: Microsoft Forms build sheet

Build this at forms.office.com while signed in with your university account. Each section below is a
**section** in Forms (Add new > Section). Question types are in brackets. `*` = required.

---

## Settings (… menu > Settings)

- **Who can fill out this form:** Only people in my organization
- **Record name:** On (gives you each student's verified name and university email automatically)
- **One response per person:** On
- **Start date:** Monday, September 28, 2026
- **End date:** Friday, October 9, 2026, 11:59 PM
- **Customize thank you message:** On (text in the last section below)
- **Allow receipt of responses after submission:** On

**Form title:** Department of Computer Science ICAIC 2026 Application Form

**Form description:**
> The Department of Computer Science is selecting three undergraduate students to compete at the
> International Collegiate AI Contest at the National University of Singapore (NUS), December 6–12,
> 2026. Travel is covered by the Department of Computer Science and accommodation is provided by NUS.
>
> Applications close Friday, October 9 at 11:59 PM. Full details:
> https://chandra-gummaluru.github.io/post/icaic-2026.html
>
> Questions? Email chandra@cs.toronto.edu

---

## Section 1 – About you

1. **Full name** * [Text]
2. **Student number** * [Text, Restrictions > Number]
   Subtitle: *Your 9- or 10-digit student number.*
3. **UTORid** * [Text]

(Your university email is recorded automatically by the "Record name" setting.)

---

## Section 2 – Eligibility

4. **Are you a registered undergraduate student in the Faculty of Arts & Science (St. George campus)?** * [Choice]
   - Yes → *Go to next section*
   - No → *Go to section "Not eligible"*

5. **Which program(s) are you enrolled in?** * [Choice, Multiple answers on]
   - Computer Science Specialist
   - Computer Science Major
   - Computer Science Minor
   - Data Science Specialist
   - First-Year Computer Science admission category (CMP1)
   - None of the above

   Subtitle: *Select all that apply (for example, the Data Science Specialist together with another program).*

   Note: Forms can't branch on multi-select questions, so "None of the above" can't route to
   "Not eligible" automatically. Filter these out in the Excel results instead.

6. **Year of study** * [Choice]
   Subtitle: *As defined by the Faculty of Arts & Science, based on credits earned. See "Year of study" at the bottom of https://artsci.calendar.utoronto.ca/glossary-terms*
   - Year 1
   - Year 2
   - Year 3
   - Year 4

7. **Will you remain enrolled through December 2026?** * [Choice]
   - Yes
   - No → *Go to section "Not eligible"*

---

## Section 3 – Availability

8. **Are you available to travel to Singapore for the full competition week, December 6–12, 2026?** * [Choice]
   - Yes
   - No → *Go to section "Not eligible"*

9. **Which qualifier day(s) can you attend?** * [Choice, Multiple answers on]
   Subtitle: *The qualifier is a three-hour, in-person contest. You will only attend one day. Select every day that works and we will confirm yours by Sunday, October 11.*
   - Friday, October 16
   - Saturday, October 17

10. **If shortlisted, which interview day(s) work for you?** * [Choice, Multiple answers on]
    Subtitle: *Interviews are the week after the qualifier. Select every day that works.*
    - Tuesday, October 20
    - Thursday, October 22

11. **If selected, can you commit a few hours each week to team training from late October until the competition?** * [Choice]
    - Yes
    - No

---

## Section 4 – Confirmations

12. **Please confirm each of the following:** * [Choice, Multiple answers on]
    Subtitle: *All three must be checked to submit a complete application.*
    - I understand that I am responsible for making sure I can legally take part and travel, including holding a valid passport and any visa I may need for Singapore.
    - If selected, I will complete the University's Safety Abroad requirements before departure (https://learningabroad.utoronto.ca/safety-abroad/students/).
    - I will compete in both the individual and team events if selected.

→ End of form (Submit)

---

## Section "Not eligible"

Put this section **last** and set its "after section" to *Submit form*.

Title: **You may not be eligible**
Description:
> Based on your answers, you do not meet the eligibility requirements for this year's team. ICAIC
> 2026 is open to registered undergraduates in the Faculty of Arts & Science (St. George) enrolled
> in a Computer Science Specialist, Major, or Minor, the Data Science Specialist, or CMP1, who can
> travel for December 6–12, 2026.
>
> If you think this is a mistake, email chandra@cs.toronto.edu before submitting.

13. **Anything you would like us to know?** [Text, Long answer, optional]

---

## Thank-you message

> Thanks for applying! We will email eligible applicants by Sunday, October 11 to confirm your
> qualifier day, time, and location.

---

## After the form is live

- Click **Collect responses** > **Copy link**, then send it over so I can drop it into the two
  Apply buttons on the website.
- To share results with Brandon: **Responses** > **Open results in Excel**, or add him as a
  co-owner via **… > Collaborate or Duplicate**.
- Tip: in the Excel sheet, filter Q12 for rows missing one of the three confirmations before
  sending qualifier invites.
