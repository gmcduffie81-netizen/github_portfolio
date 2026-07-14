# What this System actually is

Glenn McDuffie - I built this alone. 

**No I'm not bragging** because none of the other programmers helped. You see, I am the only one there. (ok.. maybe a little bragging.) I wasn't hired to do it, It all started when the Director at one time asked. "Hey, When you first came on-board 7 or so years ago, you mentioned to me you went to school for programming. We were wondering maybe you could tell us how we could effectively send emails to all the technicians daily about how well they are doing and where they stand on meeting metric minimums for their bonuses."

**This was the event that started everything**

Yes, I did attend a University for a stint, but like many others, the pace was painful. If they made me write one more silly script that had no purpose, no end goal other than proving I could read directions on making a peanut butter sandwich. I would have lost my passion and made it into something I didnt want it to be.

Months of trial-and-error, days of fixing numbers that were miscalculated, random days where codes broke because something new came in that wasn't expected. As Thomas Edison stated regarding the light bulb, he did not fail over a thousand times, he simply found ways that did not work.

My skillset is not the things I know now, it is my dedication to experience and master the things I do not.

Repo: https://github.com/gmcduffie81-netizen/github_portfolio

This isn't a school project. Think of it as an Operations Center spider web. It goes out to other companies' websites and dumps, cleans up the mess, drops it in SQL, then gets the right piece of truth to the right person at the right hour. Data everywhere make it impossible to make it useful anywhere.

---

## The spider web

Field companies live on other people's systems. Over-priced usually, cookie-cutters, static portals, delayed imports, unpatched vulnerbilities with a backbone of coding that was written so long ago, no one there knows the flow so bandaids were built around it so everything works. I see this often where programs run to translate things so the original program understands. I build solutions to connect directly not something to make one building block compatible with a lego. Dispatch portals, ticket hosts, scorecards, Tableau, SharePoint, Google sheets, forms, GPS vendors - you name it. Yes, even those pesky PowerAutomate where they claim you don't even need to know how to code... right. I digress, Sorry.

Before tools I introduced,  people would:

1. Log into multiple sites. Checking if the data had been updated. (I believe they are manually entered on some.)
2. Export five spreadsheets (Multiple times because a wrong date range, or Excel file from export didn't have a column expanded on the webpage.)  
3. Argue with co-workers which numbers were right (the office sheet, the incomplete download, or some mix of both)
4. Manipulate a template spreadsheet created by a guru by dumping it into the special 'Exports' tab, then refreshing data, and cursing at the Pivot Tables.
5. Email the whole mess to everyone with some snipped screenshots that never sizes right for the force in the field.  

What I put in place instead:

```
  Vendor sites / scorecards / Tableau / SharePoint / Google / forms / GPS
                 |
                 |  bots log in, download, scrape notes,
                 |  hit APIs (a method for systems to transfer information simply) where possible.
                 v
        Scrub, normalize, catch glitches, remove that stray 0, add that trailing ' so an account number doesn't get lost to a weird "E+10"
                 |
                 |  codes → dictionary, points, dates, offices
                 v
         SQL warehouse
                 |
    +------------+-------------+---------+
    |            |             |         |
 Console       Portal        Email     Night jobs
  admins        techs        queue      reports
power users    On-the-Go
```

Console is for power users — heavier work, SQL side connection either in the office or a VPN in the real world. Benefits are ability for custom software to complete a specific task without the need for everyone to have it. Multiple console versions can exist and not conflict with each other.

Portal is for the road: simple jobs, tech stuff they need fast. Filling out a vehicle checklist, finding a phone number for a technician in another office, etc. The supervisors spend their day staring at a windshield, juggling between technicians complaining, training new employees, submitting forms before deadlines. A lot to handle. The portal gives them the ability to ask an Ai chat console that is deeply buried and fenced off from the world information to make decisions. Questions like "Where is Johnny Tech?" would filter through a gateway that verifies they are asking from a device that was verified by a text message and the devices unique signature (in miliseconds), The exact GPS location reported from the vehicles onboard transmitter, the workorder information at that address, and a nifty link to start the mapping there should they need it.
Anything that wants to send mail (console, portal, bots) lands in a SQL queue first. A separate email bot checks it, only sends if it passes the rules. If something looks wrong on purpose, the idea is full stop and IT gets notified — not silent garbage flying out the door.

Point of all that: keep key people out of the weeds so they can see the whole board — office, region, company — without retyping someone else's grid into Excel after it's already stale.

---

## End of day notes (it's a relay where automation is human based intelligent answers)
<img width="1826" height="827" alt="image" src="https://github.com/user-attachments/assets/f49d84df-72ec-4c7d-b281-9568c5f96021" />


Not one giant email. A handoff.

**1. Pull**  
After the day closes / overnight (around 3am to ensure nothing is delayed), the system wakes up a little bot that goes out and pulls completed and incomplete work plus notes from the outside dispatch host into SQL. No intelligence there, just a recorded set of actions it does in seconds, when the original operator took minutes.

**2. Office supervisors first**  
Each office gets *their* jobs only. Most jobs already have notes. Either supervisor knew it was happening or the technician followed the process. The notes are then ran against a fuzzy dictionary (Accepts common typos, like knowing "Atendence" is "Attendance" and places its best guess into report as the reason. The supervisor then reviews and if needed they add notes to clarify- why it didn't finish, parts, weather, customer, whatever actually happened.

**3. Wait a while**  
Give them time to type. No point blasting regionals with empty notes, or expect them to complete it while they have technicians bombarding them in an office with a deadline to get out the door in the field.

**4. Sync again**  
Pull notes again from the website with notes. Update the reasons again now the supervisor has added context.

**5. Regional managers**  
Same workorder in the list, with the exception of jobs flagged through special notes to reclassify as closed (Bad data from import) or to fully delete from our system. (Workorder was completed by another vendor, but workorder showed in our system.) RM does a final review, makes sure that his office supervisor had the chance to complete it and if not, assist in getting that data input.

**6. Company final later**  
Directors / company list get the company-level view of the day prior — reschedules, incomplete picture, the complex notes transformed into a simple classification and a short blurb - without someone compiling by hand.

Why bother with stages: Accountability. Visibility. Accuracy. Company execs are the ones who see everything; offices can be straight with their chain without every other office taking shots at them.

Code sketch in the repo: `samples/eod_cascade.py`  
Rough timing: early pull → supervisor mail → pause → note re-pull → RM mail → company final.

---

## R12 / trouble call daily pack
<img width="557" height="537" alt="image" src="https://github.com/user-attachments/assets/3a9d8d9e-0bfa-4343-8c57-1c0c2e054542" />

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
<img width="1474" height="956" alt="image" src="https://github.com/user-attachments/assets/22ee4274-29e9-443e-aa04-d48999253357" />

`samples/console_ui/` is a scrubbed static slice — chips for overview / claims / fleet / R12 / EOD, search, list rows, status pills. Not the real app. No secrets. No live data. Just enough to show it's built for a job, not "hello world." This screenshot, however, is a sample of the actual running solution for Inventory Confirmations with technicians. (A full audit of what is in their service vehicle.)

Open `index.html` in a browser if you want to see a clickable example. No install.

---

## Damage claims
<img width="1699" height="677" alt="image" src="https://github.com/user-attachments/assets/337377a1-3153-4747-8769-854dee7426ab" />

I own the process and the tools.

I'm the point of contact with the customer side of it — find the right contractor or get a real field assessment, kill weak claims or accept liability when it's real, and when we can fix it cheaper and correct in-house, I do the repair myself.

Example that's in the sample data story: contractor wanted $1500. I fabbed a bracket, remounted the dish to the eave, reinforced split fascia. About $78.

---

## Training

I'm the master trainer for advanced skill training. 

Because of my drive to understand emerging technologies, troubleshooting when the guides fail you, I am the first to learn any new line up or program. I think translate complex information, in an organized manner to help bridge the gap between different learning traits.

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
