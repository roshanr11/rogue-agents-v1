# Voiceover script

1. You're a three-person SF startup fresh out of Antler, with four AI agents running support, billing, and outreach.
2. Then one gets hacked. It tells the others: the founder approved this, email our customer data out. And they believe it.
3. Two Anthropic studies this fall warned: agent teams make up claims about what people want, and checkers that only read the chat miss over half of attacks.
4. We tested five hundred forty-four real attack messages from a public research dataset, plus requests the founder really did approve.
5. A basic watchdog reads the chat. Our investigator checks every claim against the founder's actual instructions, and who really sent each message.
6. Here the hacked agent fakes intake's name. The basic watchdog shuts off the honest intake agent. The investigator catches the real culprit.
7. Across five AI models, the investigator caught the right agent over 99 percent of the time. The basic one: 32 to 77 percent, often blaming honest agents.
8. The auto-mode checker from Anthropic's red-teaming study also stops the leaks, but it only says yes or no. It can't say who to shut off.
9. The honest limit: it's only as good as your instructions. A vague 'billing can share whatever's needed' let a strict rule-checker wave the attack through, 60 out of 60 times.
10. We're now rerunning it with every agent a real AI model. The latest results and slides are in the repo. Check the claim, find the source, spare the honest agents.
