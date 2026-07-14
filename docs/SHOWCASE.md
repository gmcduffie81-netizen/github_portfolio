# What this system actually is

**Glenn McDuffie** — Sole Builder  
Private portfolio: github.com/gmcduffie81-netizen/github_portfolio

This is not a homework app. It is an **Operations Team spider web**: go out to other companies’ websites, grabs data from all the messy places it lives and data dumps, clean up the mess, land it in SQL, then push the right slice of truth to the right person at the right hour.

---

## The spider web

Field companies live on **other people’s systems** — dispatch portals, ticket hosts, scorecards, Tableau workbooks, SharePoint lists, Google sheets, form tools, GPS vendors.

Humans used to:

1. Log into five sites  
2. Export five spreadsheets  
3. Argue whose numbers were right. The in-house spreadsheet, the dataset downloaded missing key items, or a combination of both. 
4. Email everyone everything  

**What I built instead:**

```
  Vendor web UIs / scorecards / Tableau / SharePoint / Google / forms / GPS
              |  (bots log in, download, scrape notes, APIs request new information from sites with capabilities)
              v
        Scrub + normalize + glitch checks
              |  (codes → dictionary, points, dates, offices)
              v
           SQL warehouse
              |
    +---------+---------+---------+
    |         |         |         |
 Console   Portal    Email     Night jobs
  Admins    Techs    queue      reports
```
Console is for power computing - Direct Access to SQL through VPN only.
Portal is for on the road, simple tasks, and technician portal with all their information quick to access.
Email sent out by any piece (Console, Portal, Bots) all are submitted to a SQL db. A bot who's only job is email, reviews the data, verifies it is valid, and sends out if email passes all rules. Should a rogue submission bee found, it immediately shuts down all access to systems and communicates directly to IT by text message of the All systems full stop.

**Point of the whole thing:** stop key people from living in the weeds so they can see the **whole board** — offices, regions, company — without retyping someone else’s grids of data that will be obsolete by the type it is sent into Excel at 10pm.

---

## End-of-day / notes pipeline (timed cascade)

This is a **relay**, not one blast email.

| Stage | When (concept) | Who gets it | What happens |
|-------|----------------|-------------|--------------|
| **1. Pull** | After day close / overnight | System | Pulls completed / incomplete work + notes from the external dispatch host into SQL |
| **2. Office supervisors** | First wave | Each office FOS / supervisor | Report of **their office only**. They open jobs, add **real notes** (why incomplete, customer, parts, weather) |
| **3. Wait window** | Hours | — | Time for supervisors to type. No point emailing the RM empty notes. |
| **4. Re-sync** | After the window | System | Scrapes notes again from the host so supervisor updates are in the pack, secures the data into SQL|
| **5. Regional managers** | Second wave | RM per region | Same day-prior story, **rolled to their offices**, with supervisor notes attached. They review, add regional notes if needed. |
| **6. Company final** | Later | Directors / company list | **Company-level** pack for the day prior — reschedules / incomplete picture, full cascade of notes, ready for leadership without another manual scrub |

**Why it works:** the right person gets the right zoom level. Office first (close-up). Region next (pattern). Company last (whole picture). The Compant level Executive are the only ones to receive every detail, so each office share with their chain of command without fear of the other offices criticizing their results.

Code shape: `samples/eod_cascade.py`  
Schedule idea: early pull → supervisor mail → pause → note re-pull → RM mail → company final.

---

## R12 / trouble-call daily report

R12 is the **12-day return** world — repeat truck rolls hurt the company. A re-roll means we are paying an employee to fix something for pay, while the company doesn't get paid for it. A double loss - Technician routed to a loss when he could have been working for productivity. Leadership needs more than a raw export, we need to know what happened, what we did wrong, and what we can do in the future.

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

Then lands HTML into an email to all field operations leaders where people look at the data and communicate it to those returning technicians and those that we there to stop it from being more loss.

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

Not the production app. No secrets. No live data. Enough to see it has true purpose, not a print(“Hello World”).

---

## Damage claims (human + system)

I own the **process** and the **tools**:

- Customer-facing point of contact  
- Right contractor or field assessment  
- Dismiss weak claims or accept liability cleanly  
- **On-site repair** when it is cheaper and correct  

Example in sample data: contractor **$1,500** → in-house **$78** (custom bracket, eave remount, fascia reinforce).

---

## Training (Only Trainer for Advanced Tiers)

Boost Mobile Tech Expert · SimpliSafe Advanced Troubleshooting· Flock Safety · Maintenance trainer  

---

## What is intentionally missing from this repo

- Passwords, cookies, real hostnames of production systems  
- Customer / tech PII  
- Teaching comments in code (you get the walkthrough from me)  
- Full production tree  

---

## One line

I built a spider web that pulls messy vendor truth into one place, then feeds the right report to the right leader at the right time — so people stop drowning in tabs and start running the map.
