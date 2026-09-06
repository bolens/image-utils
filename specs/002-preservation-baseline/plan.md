# Plan: Image preservation and local library tools

The [specification](spec.md) preserves existing behavior. Use the project guide
and constitution for implementation constraints. Keep upstream-managed templates,
helpers, and integration manifests unchanged.

## Source ownership

- `lib/core.py`
- `lib/domain.py`
- `lib/catalog.json`
- `mcp/server.py`
- `scripts/generate.py`
- `tests/test_common.py`
- `tests/test_functional.py`
- `docs/formats.md`

## Constitution check

Preserve explicit local write authority, source retention, no-clobber publication, Python 3.11 compatibility, and the catalog/shared-engine boundary. The original retrofit changed documentation only. The legacy completion pass also repairs dependency-status propagation without adding a codec, protocol, write mode, or live service.

## Validation

```sh
make check test-all
```

Run checks in an isolated checkout. Commands are instructions, not evidence of
a pass. Record results in `coverage.md`, keep incomplete work in `tasks.md`, and
follow `RELEASING.md` for reviewed delivery. No live operation is required solely
to create this retrospective baseline.

## Legacy completion audit, 2026-09-06

Map all 38 catalog commands and supporting public/development surfaces. Reuse the
verified shared-core contracts where source comparison establishes identical
behavior, and define image-specific conversion, transforms, inspection, delegate
and fidelity boundaries from the domain implementation and native fixtures.
Repair FR-008 by sharing the CLI module identity with domain imports; test real
CLI subprocesses with no executable PATH, proving dependency status, successful
planning, retained source and absent failed output. Check Video Utils for the
same import-boundary defect and keep each repository's fix separately reviewable.
