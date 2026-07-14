# Field ops portfolio

**Glenn McDuffie**  
https://github.com/gmcduffie81-netizen/github_portfolio  
Contact: gmcduffie81@gmail.com

---

## If you don’t know what GitHub is — you’re still in the right place

**GitHub is just a website that holds project files.**  
You do **not** need an account, you do **not** need to install anything, and you do **not** need to “run code” to get value here.

### What to do (60 seconds)

1. You’re already looking at this page — that’s enough for the overview.  
2. Click this blue link: **[docs/SHOWCASE.md](docs/SHOWCASE.md)**  
3. Read it like a short story about a system I built for real field operations.  
4. (Optional) Click into any file under `samples/` if you’re curious. You can **read** them in the browser. Nothing will break if you don’t.  
5. (Optional) If you want to see a simple screen mockup: open  
   `samples/console_ui/index.html` — on GitHub, open the file, then use the raw/view options, **or** download the folder and double‑click `index.html` on a PC. Still no programming required.

**If a folder looks confusing, skip it.** The story is in SHOWCASE. The rest is backup for technical interviewers.

I build systems so **non‑technical leaders aren’t lost**. This page should work the same way.

---

## My intent (and my promise)

I provide **solutions, not confusion**.

That means:

- The right person gets the right information at the right time — not a 40‑tab mess  
- Bosses see the whole board; offices aren’t drowned in other people’s noise  
- Techs get a simple phone path for the jobs they actually do  
- When software isn’t enough, I still show up for the customer (claims, repairs, training)  

This public repo is a **clear window**, not a test to see if you can use developer tools.

---

## Why this repo exists

I built a full operations stack for multi‑office field work — console, tech portal, bots, timed reports, claims tools — **as the only coder**.

**This GitHub is not that live production system.**

It is a **public proof of concept**: enough story and structure for a hiring manager, owner, or engineer to see *how I think* and *what I own*, without dumping secrets or a free rebuild kit of a company platform.

If some code files look simple, that is **on purpose**. They are illustrations of flow — not the full factory floor.

| This repo | The real system (not published here) |
|-----------|--------------------------------------|
| Short modules + plain English docs | Large production apps, many jobs, servers, databases |
| Fake / sample data | Live tickets, people, offices |
| Read in the browser | Running services used every day |

**Do not score me only by how fancy these sample files look.**  
Score the **problems I chose to solve** and the **cascade of who gets what report**. Ask me in an interview for the full walkthrough.

---

## Start here (everyone)

**[docs/SHOWCASE.md](docs/SHOWCASE.md)** — plain English:

- Pulling messy data from many places into one clean system  
- End‑of‑day reports: office supervisors → time for notes → regional managers → company final  
- Daily R12 / trouble‑call pack (what came back, who’s on it today, what the return tech fixed)  
- Claims — software **and** customer‑facing process ($1,500 quote vs $78 in‑house fix in the sample story)  
- Console / portal idea and why both exist  

---

## For technical reviewers only (optional)

| Path | Shape of the idea |
|------|-------------------|
| `samples/ingest_spiderweb.py` | Many sources → clean data |
| `samples/eod_cascade.py` | Office → region → company timing |
| `samples/r12_pipeline.py` | TC sections + reason codes |
| `samples/access_control.py` | Who is allowed to see what |
| `samples/schedule_state.py` | Schedule / miss / close |
| `samples/claims_flow.py` | Claim path + cost comparison |
| `samples/console_ui/` | Static UI mock (open `index.html`) |
| `samples/data/` | Fake examples only |

No need to install Python or “clone” anything unless you want to.

---

## What is *not* in this repo

- Passwords, keys, or live connections  
- Real customer or employee private data  
- The full production source tree  
- A product you are expected to install and run at work tomorrow  

---

## One line

I build tools that remove confusion for the people doing the work.  
This page is built the same way — **read SHOWCASE, skip what you don’t need, call me if you want the real tour.**

Thanks for looking.
