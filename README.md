# ⚠️ This Repository Has Been Archived

**This repository (`arko-sanyal-loci/loci-coordination-bus`) is no longer maintained.**
`coordination_bus/` has been merged into the single canonical engine repo,
per the decision to consolidate into one repo rather than split the engine
across several:

## → [arko-sanyal-loci/LOCI-MEMORY-ENGINE](https://github.com/arko-sanyal-loci/LOCI-MEMORY-ENGINE) (`coordination_bus/`)

### What was ported (unchanged)
- `coordination_bus/bus.py`, `coordination_bus/mcp_server.py` → same paths in the canonical repo
- `tests/test_bus.py`, `tests/test_mcp_server.py` → `tests/coordination_bus/` in the canonical repo
- `docs/SECURE-BUS.md` → `architecture/SECURE-BUS.md` in the canonical repo
- `scripts/run_coordination_mcp.sh` → same path in the canonical repo

170/171 tests pass post-merge (the 1 failure is `fastmcp` not being
installed in the test sandbox, not a code issue).

---
*Consolidated: November 2026 by Arko Sanyal (Billo Tech).*
