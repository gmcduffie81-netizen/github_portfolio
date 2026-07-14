# Field OPS Portfolio

Glenn McDuffie  
https://github.com/gmcduffie81-netizen/github_portfolio  
gmcduffie81@gmail.com

---

## Never used GitHub? It's ok, I promise you're fine.

It's basically a website that stores files for a project. You don't need an account. You don't need to install Python or "clone" anything.

Here's all I need you to do:

1. Read this page (You're already here, Thank you! I am truly humbled and honored you gave me a moment).
2. Click **[docs/SHOWCASE.md](docs/SHOWCASE.md)** and read that next. That's the real story.
3. If you're not a coder, stop there. Seriously. That's enough.
4. If you want a rough screen mock, open `samples/console_ui/index.html` somehow on a computer and double-click it. Optional.

If a folder name looks weird, ignore it. I didn't put this up to trip people who don't live in code all day.

I spend a lot of time building tools so regular leaders aren't lost in tech. Figured this page ought to work the same way.

---

## What I Care about

I try to hand people solutions, not more confusion.

In practice that looks like: the right person gets the right info without drowning in everybody else's noise. Techs get something simple on a phone. Supervisors aren't retyping five websites into Excel at 10pm. And when the software isn't enough, I still get involved with customers, claims, training, or a repair on site.

This repo is just a window into that. It's not a test to see if you know Git.

---

## What this IS and what it ISN'T

I built a full ops setup for multi-office field work covering four states by myself - console, portal, bots, web scrappers, reports, claims tools, etc.

**None of that live production system is sitting here.** On purpose. 

What's here is smaller on purpose too. Fake data. Short code files that show the *shape* of a flow, not the whole factory. If it looks basic compared to a commercial product, good - I wasn't trying to open-source the real stack or give away things that lived in my brain, haunted me with bugs, and became a solution that some would re-package, slap a barcode on and sell as their own. This solution is Middleware and end solution wrapped together in a pretty package.

The long version of the design is in SHOWCASE. If you want the full tour of what actually runs day to day, that's a conversation. Happy to do that live.

---

## Where to Click

**Everyone:** [docs/SHOWCASE.md](docs/SHOWCASE.md)

Covers the spider-web data pulls, the end-of-day note relay (office -> region -> company), the daily trouble-call / R12 style pack, claims (including a $1500 vs $78 repair story), and why console and portal are different.

**Coders only if you want:** poke around under `samples/`. Read in the browser. No install required.

Rough map of samples:

- `ingest_spiderweb.py` — many sources, clean-up, bad number checks  
- `eod_cascade.py` — timed mail waves  
- `r12_pipeline.py` — TC sections + code dictionary  
- `access_control.py` — who can see what  
- `schedule_state.py` — schedule / miss / close  
- `claims_flow.py` — claim path + costs  
- `console_ui/` — static mock screens  
- `data/` — fake examples  

---

## Stuff I deliberately left out

Passwords, live connections, real customer/employee data, production hosts, the full source tree. Also not a product you're supposed to install at work next week.

## Comments in code. PEP Standards not in here. Fellow coders, I promise it's not because I was lazy.

It wasn't because I forgot them, either. Its because these code examples are to show the bolts I made to build something that had no blueprint. If you are a fellow coder and some of my code is what you need for your project, reach out to me, I'll gladly give you more insight and applying it to use.
---

Thanks for taking a look. If something's unclear, email me — I'll explain it straight.
