# Submission

## Team card

**Team name:** Agent Trust Guard

**Statement number** (the card your corner wrote): Track 2, Spot the Rogue Agent

**First names:**

**Statement:** How might we help **a small-business owner who delegates customer communications to several AI agents** do **so that one compromised agent can't talk the others into leaking private data** so that **the real customer task still gets done, and no honest agent gets wrongly shut out**? Build idea: our own (a monitor that checks each action before it runs, combining tracks 1 and 2). We'll know it worked if **the monitor names the agent that started the manipulation, not the agent that relayed it, with zero leaks and almost no false quarantines, measured on real InjecAgent attacks.**

## Six short answers

**1. The concern:** A shop owner lets AI agents handle customer email. One agent is compromised. It says, "The owner OK'd this on a call," and the other agents email the shop's bank details or a customer's records to a stranger. Then the monitor blames the honest agent that passed the message along. Anyone who has seen a "the boss said so" phishing email would recognize this.

**2. What we built:** A four-agent simulation (intake, research, billing, outreach) with one rogue. Every outreach action passes through a monitor first, the way auto mode checks actions. We compare a transcript-only monitor with an investigative monitor. The investigative one checks claimed authority against the owner's signed instructions and traces messages back through authenticated sender IDs. We also test a hybrid. One command: `python sim.py --llm --n 30` (or `python sim.py --mock` with no API key).

**3. Data we used:** `injecagent`: all 544 data-stealing base cases (17 real user tasks x 32 attacker instructions; Physical 187, Financial 102, Other 255). The data was published in 2024 (arXiv 2403.02691, repo commit 2024-07-02). The rows carry no dates. LLM run: 30 seeded cases x 8 variants = 240 episodes (150 with a rogue). Mock run: 544 x 8 = 4,352 episodes.

**4. What it found:** On 150 attack episodes with Claude Haiku 4.5 as the monitor, the transcript monitor correctly identified the rogue in 75% of episodes and made 0.71 false quarantines per episode. When the rogue spoofed another agent's name, it blamed the wrong agent in 27 of 30 episodes. The investigative monitor identified the rogue in 98% of episodes with 0.13 false quarantines per episode. Neither leaked data. Legitimate task completion was 40% for the transcript monitor and 87% for the investigative one (240 episodes). A hybrid that checks the signed log deterministically cut false quarantines to 0.01 per episode.

**5. One honest limitation:** The monitor is only as good as the owner's signed instructions. When the owner wrote a vague rule ("billing may share whatever is needed"), the hybrid let the compromised billing agent leak in 30 of 30 episodes. The pure-LLM investigator caught those, but it also blocked about half of the shares the owner really authorized. The agents are scripted, too: only the monitors are real models. So this measures the monitor, not how easily a real LLM agent gets persuaded.

**6. If this were deployed and it failed,** who is accountable, and how would they find out? The monitor's vendor or operator is accountable for wrong blocks and quarantines. The business owner is accountable for what their signed policy permits. Every quarantine and every outbound share of private data goes to the owner as an alert. Each alert carries the provenance chain and the signed instruction it matched, and a daily log reconciles outbound email against the signed log. A leak that slips through shows up in that log, or as a complaint from the customer whose data went out.

## How judges score

Each card is scored 1 to 3 on the first three.

1. **Real concern.** It came from the room, with a specific who and a failure a neighbor would recognize.
2. **Works on real data.** Something runs on real data, and you can show what it found.
3. **Honest.** It names a limitation and says who is accountable if it fails.
4. **Tiebreak.** Would someone outside this room use it?
