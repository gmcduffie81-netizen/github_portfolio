# What this system actually is

**Glenn McDuffie** — sole builder  
Private portfolio: github.com/gmcduffie81-netizen/github_portfolio

This is not a homework app. It is an **ops spider web**: go out to other companies’ websites and data dumps, clean the mess, land it in SQL, then push the right slice of truth to the right person at the right hour.

---

## The spider web (plain English)

Field companies live on **other people’s systems** — dispatch portals, ticket hosts, scorecards, Tableau workbooks, SharePoint lists, Google sheets, form tools, GPS vendors.

Humans used to:

1. Log into five sites  
2. Export five spreadsheets  
3. Argue whose numbers were right  
4. Email everyone everything  

**What I built instead:**

```
  Vendor web UIs / scorecards / Tableau / SharePoint / Google / forms / GPS
              |  (bots log in, download, scrape notes)
              v
        Scrub + normalize + glitch checks
              |  (codes → dictionary, points, dates, offices)
              v
           SQL warehouse
              |
    +---------+---------+---------+
    |         |         |         |
 Console   Portal    Email     Night jobs
  bosses    techs    queue      reports
```

**Point of the whole thing:** stop key people from living in the weeds so they can see the **whole board** — offices, regions, company — without retyping someone else’s portal into Excel at 10pm.

---

## End-of-day / notes pipeline (timed cascade)

This is a **relay**, not one blast email.

| Stage | When (concept) | Who gets it | What happens |
|-------|----------------|-------------|--------------|
| **1. Pull** | After day close / overnight | System | Pulls completed / incomplete work + notes from the external dispatch host into SQL |
| **2. Office supervisors** | First wave | Each office FOS / supervisor | Report of **their office only**. They open jobs, add **real notes** (why incomplete, customer, parts, weather) |
| **3. Wait window** | Hours | — | Time for supervisors to type. No point emailing the RM empty notes. |
| **4. Re-sync** | After the window | System | Scrapes notes again from the host (or DB) so supervisor updates are in the pack |
| **5. Regional managers** | Second wave | RM per region | Same day-prior story, **rolled to their offices**, with supervisor notes attached. They review, add regional notes if needed. |
| **6. Company final** | Later | Directors / company list | **Company-level** pack for the day prior — reschedules / incomplete picture, full cascade of notes, ready for leadership without another manual scrub |

**Why it works:** the right person gets the right zoom level. Office first (close-up). Region next (pattern). Company last (whole picture).

Code shape: `samples/eod_cascade.py`  
Schedule idea: early pull → supervisor mail → pause → note re-pull → RM mail → company final.

---

## R12 / trouble-call daily report

R12 is the **12-day return** world — repeat truck rolls hurt the score. Leadership needs more than a raw export.

### What the job does every day

1. **Logs into the vendor operations site** (browser automation)  
2. Pulls **new reroll / TC creates overnight** (scorecard + search pages)  
3. For each related job, **opens work-order detail + notes pages**  
4. **Filters noise** (system/ops note spam)  
5. Hits a **local keyword dictionary** — short codes in the note become human reasons (`015Z` → “Signal loss – no protector”, etc.)  
6. Builds a daily pack with three brains:

| Section | Meaning |
|---------|---------|
| **New TCs created yesterday** | Fresh trouble calls born on the prior day |
| **TCs scheduled today** | Who is on the truck today, which office, which tech assigned |
| **Went back yesterday** | Return trips completed prior day — **returning tech’s repair notes** so QA knows what actually got fixed |

Then lands CSV/HTML where people already look (internal web host / share) and logs success/fail.

Code shape: `samples/r12_pipeline.py` + `samples/data/reason_codes.json`

---

## Glitch hunting (why normalize)

Vendor sites lie in small ways:

- Point values off by a row or formula  
- Dates as Excel serials vs text  
- Same tech spelled three ways  
- Notes full of codes only veterans know  

The pipeline **checks and flattens** so reports agree. That is how you get out of “my Tableau says X, your export says Y.”

---

## Ops Console + Field Portal (UI you can click in the repo)

`samples/console_ui/` is a **scrubbed, static slice** of the road console look-and-feel:

- Chip navigation (Overview, Claims, Fleet, Techs…)  
- Search + filters  
- Claim / ticket list rows  
- Status pills  

Not the production app. No secrets. No live data. Enough to see it is a **real product UI**, not a print(“hello”).

---

## Damage claims (human + system)

I own the **process** and the **tools**:

- Customer-facing point of contact  
- Right contractor or field assessment  
- Dismiss weak claims or accept liability cleanly  
- **On-site repair** when it is cheaper and correct  

Example in sample data: contractor **$1,500** → in-house **$78** (custom bracket, eave remount, fascia reinforce).

---

## Training (only trainer)

Boost Mobile Tech Expert · SimpliSafe advanced · Flock Safety · Maintenance trainer  

---

## What is intentionally missing from this repo

- Passwords, cookies, real hostnames of production systems  
- Customer / tech PII  
- Teaching comments in code (you get the walkthrough from me)  
- Full production tree  

---

## One line

I built a spider web that pulls messy vendor truth into one place, then feeds the right report to the right leader at the right time — so people stop drowning in tabs and start running the map.
