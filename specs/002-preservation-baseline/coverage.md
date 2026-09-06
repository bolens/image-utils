# Requirement coverage

| Requirement | Source and acceptance evidence |
| --- | --- |
| FR-001 | `lib/catalog.json`, `scripts/generate.py`, and `scripts/check.py` generated-drift checks. |
| FR-002 | `lib/core.py:execute` and `publish`; `tests/test_common.py` covers failed writers/verifiers, publication races, cleanup, and preserved existing files. |
| FR-003 | `lib/core.py:discover` and `execute`; common filename, exclusion, collision, and mixed-batch tests. |
| FR-004 | `lib/domain.py:staged` and `write`; functional tests cover delegates, animation refusal, exact transform pixels, and PPM/PNG round trips. |
| FR-005 | `lib/core.py:common`, catalog read operations, manifest-response round trips, no-content-read summary tests, and comparison tests. |
| FR-006 | `mcp/server.py`, allowed-root/initialize/request validation tests in `tests/test_common.py`. |
| FR-007 | `lib/core.py:ordered_work` and `execute`; common scheduling tests and mixed valid/corrupt functional batches with one and two workers. |

## Verification receipt

On 2026-09-05, `make check test-all` passed 66 tests with no failures or skips against the inspected base. `make check` also passed after adding this baseline. A separate self-review traced catalog generation, dry-run authority, discovery, staged verification and publication, batch failures, and MCP restrictions through the named source and test assertions. No unresolved requirement gap was found within this baseline. This proves the named fixture contracts, not every possible media file or external parser implementation. Hosted checks and delivery are recorded in the PR.

## Legacy completion receipt, 2026-09-06

[Legacy contracts](legacy-contracts.md) and the [38-tool mapping](legacy-coverage.md)
cover the full catalog plus shared CLI/configuration, publication, MCP, generated
site, Docker and development surfaces. FR-008 is owned by the CLI module alias in
`lib/core.py`; `test_missing_domain_executable_preserves_dependency_status` in
`tests/test_common.py` exercises actual CLI subprocesses with an empty executable
PATH. Both inspection and applied conversion returned 1 before the fix and now
return dependency status 2; dry-run planning succeeds and source/output checks pass.

`make check test-all` passed all 72 tests with zero skips, including installed
conversion delegates, exact transform pixels, PPM/PNG round trip, animation refusal,
publication failures and MCP boundaries. Syntax, ShellCheck, generated drift, local
links and action pins passed. Source comparison confirmed the shared core/MCP
contract equivalence with the archive suite; image behavior was reviewed separately
against `lib/domain.py` and its fixtures. Video Utils has the same import-boundary
pattern and is being corrected in its own change.

Separate self-review checked module identity for both script/import callers,
dependency-versus-delegate failure distinctions, literal filenames, no-clobber
publication, every catalog row, and image fidelity limits. No independent reviewer
was used. No personal media, site generation, live service or version release was
part of the audit. Exact candidate/main CI and GHCR digest verification remain
delivery gates recorded by the PR.
