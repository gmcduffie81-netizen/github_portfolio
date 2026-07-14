# What this system actually is

Glenn McDuffie — I built this alone.

Repo: https://github.com/gmcduffie81-netizen/github_portfolio

This isn't a school project. Think of it as an ops spider web. It goes out to other companies' websites and dumps, cleans up the mess, drops it in SQL, then gets the right piece of truth to the right person at the right hour.

---

## The spider web

Field companies live on other people's systems. Dispatch portals, ticket hosts, scorecards, Tableau, SharePoint, Google sheets, forms, GPS vendors — you name it.

Before tools like this, people would:

1. Log into five sites  
2. Export five spreadsheets  
3. Argue which number was right (the office sheet, the incomplete download, or some mix of both)  
4. Email the whole mess to everyone  

What I put in place instead:

```
  Vendor sites / scorecards / Tableau / SharePoint / Google / forms / GPS
              |
              |  bots log in, download, scrape notes,
              |  hit APIs where the site actually has one
              v
        Scrub, normalize, catch glitches
              |
              |  codes → dictionary, points, dates, offices
              v
           SQL warehouse
              |
    +---------+---------+---------+
    |         |         |         |
 Console   Portal    Email     Night jobs
  admins    techs    queue      reports
```

Console is for power users — heavier work, SQL side is VPN-only in the real world.  
Portal is for the road: simple jobs, tech stuff they need fast.  
Anything that wants to send mail (console, portal, bots) lands in a SQL queue first. A separate email bot checks it, only sends if it passes the rules. If something looks wrong on purpose, the idea is full stop and IT gets notified — not silent garbage flying out the door.

Point of all that: keep key people out of the weeds so they can see the whole board — office, region, company — without retyping someone else's grid into Excel after it's already stale.

---

## End of day notes (it's a relay)

Not one giant email. A handoff.

**1. Pull**  
After the day closes / overnight, the system pulls completed and incomplete work plus notes from the outside dispatch host into SQL.

**2. Office supervisors first**  
Each office gets *their* jobs only. They add real notes — why it didn't finish, parts, weather, customer, whatever actually happened.

**3. Wait a while**  
Give them time to type. No point blasting regionals with empty notes.

**4. Sync again**  
Pull notes back from the host (and lock what we need into SQL) so the supervisor updates are actually in the pack.

**5. Regional managers**  
Same day-prior story, rolled to their offices, with supervisor notes on it. They review and can add regional notes.

**6. Company final later**  
Directors / company list get the company-level view of the day prior — reschedules, incomplete picture, the whole note chain — without someone manually scrubbing it again.

Why bother with stages: close-up first (office), patterns next (region), whole picture last (company). Company execs are the ones who see everything; offices can be straight with their chain without every other office taking shots at them.

Code sketch in the repo: `samples/eod_cascade.py`  
Rough timing: early pull → supervisor mail → pause → note re-pull → RM mail → company final.

---

## R12 / trouble call daily pack

R12 is the 12-day return world. A re-roll hurts. You're paying a tech to fix something the company often doesn't get paid for again, and that tech isn't on a productive job. Double loss. Leadership needs more than a raw dump — what happened, where we messed up, what to watch next time.

What the daily job is doing, in order:

1. Log into the vendor ops site (browser automation)  
2. Pull new reroll / TC creates from overnight (scorecard + search)  
3. Open the related work order detail and notes pages  
4. Drop noise notes (system/ops spam)  
5. Run notes through a local keyword dictionary so codes become plain reasons (e.g. 015Z → signal loss / no protector)  
6. Build one pack with three parts:

**New TCs created yesterday** — trouble calls that showed up the day before  

**TCs scheduled today** — who's on the truck today, which office, which tech  

**Went back yesterday** — return trips done the prior day, with the returning tech's notes on what they actually did to fix it  

That lands as HTML in email to field ops leaders so they can talk to the techs who are going back (and the ones who were there before it turned into more loss).

Code sketch: `samples/r12_pipeline.py` and `samples/data/reason_codes.json`

---

## Why we normalize (glitches)

Vendor sites lie in small annoying ways:

- Point values off a row or a bad formula  
- Dates as Excel serial numbers one place and text somewhere else  
- Same tech spelled three different ways  
- Notes full of codes only people who've been around forever understand  

The pipeline checks and flattens so you're not stuck in "my Tableau says X, your export says Y."

---

## Console + portal UI sample

`samples/console_ui/` is a scrubbed static slice — chips for overview / claims / fleet / R12 / EOD, search, list rows, status pills. Not the real app. No secrets. No live data. Just enough to show it's built for a job, not "hello world."

Open `index.html` in a browser if you want. No install.

---

## Damage claims

I own the process and the tools.

I'm the point of contact with the customer side of it — find the right contractor or get a real field assessment, kill weak claims or accept liability when it's real, and when we can fix it cheaper and correct in-house, I do the repair myself.

Example that's in the sample data story: contractor wanted $1500. I fabbed a bracket, remounted the dish to the eave, reinforced split fascia. About $78.

---

## Training

I'm the only trainer we had on the advanced tracks I ran:

Boost Mobile Tech Expert, SimpliSafe advanced troubleshooting, Flock Safety, maintenance trainer.

---

## What's missing on purpose

No passwords, cookies, or real production hostnames.  
No customer or tech private data.  
No giant teaching comments in the code (I'll walk you through it if we talk).  
No full production tree.

---

## Bottom line

I built a spider web that pulls messy vendor truth into one place and then feeds the right report to the right leader at the right time. Less drowning in tabs. More running the map.

If you want details, email me. I'm easier to understand in a conversation than in a repo full of fake sample files.
