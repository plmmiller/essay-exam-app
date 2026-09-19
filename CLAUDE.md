
<!-- status-md-discipline -->
## STATUS.md discipline (required)

Maintain `docs/planning/STATUS.md` as the single source of truth for completion state.
It is a burndown, not a plan. Rules:

1. One row per work item (reuse the plan's IDs, e.g. F-01..F-N), each marked:
   ✅ done · 🟡 partial · ⬜ not started · 🚫 blocked.
2. VERIFY, NEVER ASSUME. Before marking ✅ or 🟡, confirm against the actual code
   (read the source/tests/migrations or the PR) and cite evidence — a real path,
   test, or PR. If you can't verify it, it's ⬜. A plan saying "this was sprint 1"
   is NOT evidence it shipped.
3. Update STATUS.md in the SAME change as the work that lands. It must never lag the
   repo. Refresh the header (date + current git SHA) every update.
4. Keep an append-only Changelog (e.g. "F-03 ⬜→✅") and Decisions log.
5. When asked for status, read this file and give a grouped view: counts, current
   focus, what shipped recently, what's next, what's blocked.
6. Planning docs describe intent and sequence; STATUS.md tracks state. Don't merge them.
<!-- /status-md-discipline -->
