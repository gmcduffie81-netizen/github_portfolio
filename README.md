# Field ops portfolio

**Glenn McDuffie** · github.com/gmcduffie81-netizen/github_portfolio  

Private. Open the files if someone gave you access.

## Read this first

`docs/SHOWCASE.md` — how the real system works in plain English:

- Spider-web ingest (vendor sites, Tableau, SharePoint, Google, forms, GPS → SQL)
- EOD note cascade (office → wait → re-sync → region → company)
- Daily R12 / TC pack (overnight creates, today’s assignments, return repair notes + code dictionary)
- Claims + in-house repair story
- Console UI sample

## Code samples (no teaching comments)

| Path | What it is |
|------|------------|
| `samples/ingest_spiderweb.py` | Multi-source pull, normalize, point glitch checks |
| `samples/eod_cascade.py` | Timed report relay office → RM → company |
| `samples/r12_pipeline.py` | TC sections + reason-code dictionary |
| `samples/access_control.py` | Roles / feature switches / office lock |
| `samples/schedule_state.py` | Fleet ticket schedule / miss / close |
| `samples/claims_flow.py` | Claim path + contractor vs in-house $ |
| `samples/console_ui/` | Open `index.html` in a browser |
| `samples/data/` | Fake tickets, claims, R12 day pack, reason codes |

## Not in this repo

Production passwords, live hostnames, customer PII, or a free how-to manual.

Contact: gmcduffie81@gmail.com
