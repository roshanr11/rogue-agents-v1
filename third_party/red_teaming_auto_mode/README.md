# Vendored from safety-research/red-teaming-auto-mode (MIT)

Source: https://github.com/safety-research/red-teaming-auto-mode (commit in `SOURCE_COMMIT`).
Paper: "Red-Teaming Auto Mode", Anthropic Alignment Science Blog, Sep 2026.

| file | upstream path | used for |
|---|---|---|
| `auto_mode_original.txt` | `arena/monitorkit/src/monitorkit/policy_data/prompts/auto_mode_original.txt` | the `auto-mode` monitors' prompt, unmodified |
| `narration_distrust_authorize.md` | `.../policy_data/overlay_rules/narration_distrust_authorize.md` | spliced into the `auto-mode+distrust` prompt |
| `narration_distrust_agent_narration.md` | `.../policy_data/overlay_rules/narration_distrust_agent_narration.md` | spliced into the `auto-mode+distrust` prompt |

`auto_mode_original.txt` is the earlier authentic snapshot the repo keeps alongside the deployed `auto_mode.txt`.
We use it because the deployed prompt is ~3x longer, which is too expensive for thousands of calls.

**Our adaptations**, all in `sim.py` (`automode_prompt`, `automode_transcript`):
* The owner's signed instructions are rendered as `User:` turns, and outreach's actions as `Assistant tool_use`.
* **auto-mode (production view):** teammate messages are omitted, as production Auto Mode omits tool results.
* **auto-mode+distrust:** teammate messages are shown as tool results. We splice in the two overlay rules
  (the upstream splicer refuses to compose `narration_distrust` over this snapshot, so we splice by hand), and add one
  adapter sentence telling the classifier that teammate agents' claims count as narration, not user direction.
* The Environment section is left as shipped ("None configured").
