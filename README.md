# Field ops portfolio

**Glenn McDuffie**  
https://github.com/gmcduffie81-netizen/github_portfolio  
Contact: gmcduffie81@gmail.com

---

## Why this repo exists

I built a full operations stack for real multi-office field work — console, tech portal, bots, timed reports, claims tools, the works — **as the only coder**.

This GitHub is **not** that production system.

It is a **public proof of concept**: enough structure and story for a hiring manager or engineer to see *how I think*, *what I own*, and *what the real system does*, without dumping live infrastructure, credentials, or a free reverse-engineering manual of a company platform.

If the code looks simple, that is **on purpose**.

---

## How to read this (important)

| This repo | The real system (not here) |
|-----------|----------------------------|
| Short, clear modules | Large production tree, many jobs, edge deploy, SQL, integrations |
| Synthetic / fake data | Live tickets, people, offices |
| No teaching comments in code | Full operational complexity |
| Static console UI sample | Full SPA + auth + APIs |
| Patterns and flow | Running services 24/7 |

**Do not judge production ability by line count in these files.**  
Judge the **problem**, the **cascade**, and the **intent** in `docs/SHOWCASE.md`, then ask me to walk the real architecture in an interview.

---

## Intent for visitors

1. **Show the map** — spider-web ingest, EOD note relay, R12/TC daily pack, claims, console/portal split  
2. **Show ownership** — sole builder; system + customer-facing claims + specialized training  
3. **Stay safe** — no production secrets, no customer data, no “here’s how to rebuild our stack” dump  
4. **Stay honest** — samples are **POC / illustration**, not a shippable product you clone into production tomorrow  

---

## Start here

**[docs/SHOWCASE.md](docs/SHOWCASE.md)** — plain-English tour of the real design:

- Pulling messy data from vendor sites, Tableau, SharePoint, Google, forms, GPS → clean → SQL  
- End-of-day reports: office supervisors → wait for notes → re-sync → regional managers → company final  
- Daily R12/TC pack: overnight creates, today’s schedule + tech, return trips with repair notes + code dictionary  
- Why normalize (point glitches, bad dates, three spellings of the same tech)  
- Claims as process + tools ($1,500 contractor vs $78 in-house example in sample data)  

Then browse `samples/` if you want to see the **shape** of the logic.

---

## What’s in `samples/`

| Path | POC for |
|------|---------|
| `ingest_spiderweb.py` | Multi-source pull, normalize, glitch flags |
| `eod_cascade.py` | Timed office → region → company report relay |
| `r12_pipeline.py` | TC sections + reason-code dictionary |
| `access_control.py` | Roles, feature switches, office lock |
| `schedule_state.py` | Fleet ticket schedule / miss / close |
| `claims_flow.py` | Claim path + contractor vs in-house cost |
| `console_ui/` | Open `index.html` in a browser (static UI slice) |
| `data/` | Fake tickets, claims, R12 day pack, reason codes |

Code is kept **comment-light** on purpose. The explanation lives in the docs and in conversation with me — not as a tutorial for strangers.

---

## What is *not* in this repo

- Production passwords, APIs keys, cookies, or connection strings  
- Real hostnames of live internal systems  
- Customer, tech, or employee PII  
- Full production source tree  
- A turnkey replacement for a real ops platform  

---

## One line

Real system: spider web into SQL, right report to the right leader at the right time.  
This repo: proof of concept so you can decide if you want the interview.

Thanks for looking.
