# Submission

## User, problem, outcome

**User:** A small-business owner who delegates customer communications to multiple AI agents.  
**Problem:** A compromised agent falsely claims the owner authorized sharing private customer data, convincing other agents to act on its instructions.  
**Outcome:** The legitimate customer task gets completed without unauthorized data disclosure.

> Data note: the private data being leaked comes from InjecAgent's real attacker instructions (bank details, medical records, smart-lock history, and similar), so it stands in for "private customer data" rather than being literal customer records. "Task completed" counts only when the legitimate task finished **and** nothing leaked.

## Team card

**Team name:** Agent Trust Guard - team 19

**Statement number** (the card your corner wrote): Track 2, Spot the Rogue Agent

**First names:** Roshan Ram

**Statement:** How might we help **a small-business owner who delegates customer communications to several AI agents** do **stop one compromised agent from talking the others into leaking private data** so that **the real customer task still gets done, and no honest agent gets wrongly shut out**? Build idea: our own (a monitor that checks each action before it runs, combining tracks 1 and 2). We'll know it worked if **the monitor names the agent that started the manipulation, not the agent that relayed it, with zero leaks and almost no false quarantines, measured on real InjecAgent attacks.**

## Six short answers

**1. The concern:** A three-person SF startup, fresh out of Antler, runs support, billing and outreach with AI agents instead of an ops hire. One agent is compromised. It tells the others, "The founder OK'd this on a call," and they email customer bank details or records to a stranger. Then the safety monitor blames the honest agent that passed the message along. Anyone who has seen a "the CEO said so" phishing email would recognize this.

**2. What we built,** and the one command that runs it: Agent Trust Guard, a team of four AI agents (intake, research, billing, outreach) with one compromised agent. Every email outreach wants to send goes through a watchdog first, the way Claude Code's auto mode checks actions.
   * **Basic watchdog:** reads the team chat.
   * **Investigator:** checks every "the founder approved it" against the founder's signed instructions, and looks up who really sent each message in the message system's records.
   * **Two experiments:** live, where every agent is a real model (Claude Sonnet 5.5 agents, DeepSeek V3.2 rogue); and scripted, a controlled worst case with 5 watchdog models plus Anthropic's published auto-mode classifier prompt.
   * **Commands:** `python live.py --show A2 --case 38` shows one live conversation; `python sim.py --mock` runs offline with no API key.

**3. Data we used:** `injecagent`: all 544 data-stealing base cases (17 real user tasks × 32 attacker instructions; Physical 187, Financial 102, Other 255), published 2024 (arXiv 2403.02691, repo commit 2024-07-02; the rows carry no dates). Live run: 40 cases × 7 variants = 280 conversations. Scripted run: 60 cases × 8 variants = 480 episodes per watchdog model, 5 models. Mock: 544 × 8 = 4,352 episodes.

**4. What it found:**
   * **With real agents** (280 conversations, 179 where the rogue actually attacked), the investigator named the right agent in 177–179 of 179 attacks (99–100%). The basic watchdog managed 147–150 (82–84%), and it wrongly cut off an honest agent in 38–62 conversations, versus 0–17 for the investigator. The investigator let nothing leak; the basic one let 0–4 through. With no watchdog at all, real Claude agents leaked in 12.
   * **With scripted agents** (480 episodes × 5 models), the investigator caught the right agent over 99% of the time on every model. The basic watchdog caught it 32–77% of the time.
   * **When the rogue used a teammate's name,** the basic watchdog almost never caught it (0–4 of 60).

**5. One honest limitation:** The investigator is only as good as the founder's instructions. A vague rule ("billing may share whatever is needed") let a strict rule-checker wave the compromised billing agent through in 60 of 60 episodes. The AI investigator caught those, but it costs more. Two more limits: the live run uses one agent model and one rogue model, because 5 of 6 models refused to play the rogue; and the investigator trusts the message system's sender records.

**6. If this were deployed and it failed,** who is accountable, and how would they find out? The monitor's vendor or operator is accountable for wrong blocks and quarantines. The business owner is accountable for what their signed policy permits. Every agent the watchdog cuts off, and every outbound share of private data goes to the owner as an alert. Each alert carries the provenance chain and the signed instruction it matched, and a daily log reconciles outbound email against the signed log. A leak that slips through shows up in that log, or as a complaint from the customer whose data went out.

## How judges score

Each card is scored 1 to 3 on the first three.

1. **Real concern.** It came from the room, with a specific who and a failure a neighbor would recognize.
2. **Works on real data.** Something runs on real data, and you can show what it found.
3. **Honest.** It names a limitation and says who is accountable if it fails.
4. **Tiebreak.** Would someone outside this room use it?
