# Legacy implementation coverage

Audit at `ccd8366`, 2026-09-06. All 38 catalog entries are mapped below.
[Legacy contracts](legacy-contracts.md) supplies acceptance rules; generated
[CLI references](../../docs/cli.md) retain exact options. LC-001–004 apply to every
CLI command, LC-008 to domain image operations, and LC-013 to the restricted MCP
subset. Test links name acceptance owners, not a claim that every delegate or
color profile was exercised.

| Tool | Contract | Implementation | Acceptance fixtures |
| --- | --- | --- | --- |
| `library-inventory` | LC-009 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `library-summary` | LC-009 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `library-dupes` | LC-010 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `hash-manifest` | LC-011 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `hash-verify` | LC-011 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `tree-diff` | LC-012 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `path-audit` | LC-012 | [lib/core.py](../../lib/core.py) | [tests/test_common.py](../../tests/test_common.py) |
| `jpg-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `png-to-jpg` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `webp-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `png-to-webp` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `tiff-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `png-to-tiff` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `bmp-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `png-to-avif` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `avif-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `heic-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `jxl-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `png-to-jxl` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `gif-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `png-to-ppm` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `ppm-to-png` | LC-005 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-resize` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-thumbnail` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-auto-orient` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-strip` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-grayscale` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-rotate` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-flip` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-flop` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-crop` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-flatten` | LC-006 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-metadata` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-verify` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-orientation` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-colors` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-compare` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |
| `image-alpha-audit` | LC-007 | [lib/domain.py](../../lib/domain.py) | [tests/test_functional.py](../../tests/test_functional.py) |

## Supporting surfaces

| Contract | Source owner | Acceptance owner and limits |
| --- | --- | --- |
| LC-001–004 / FR-008 | [Dispatcher](../../bin/image-utils), [core](../../lib/core.py), [catalog](../../lib/catalog.json), generated wrappers/Makefiles | [Common tests](../../tests/test_common.py), including missing domain executable, configuration, discovery, exclusions, publication races, reports and bounded workers; [checkout tests](../../tests/test_checkout_portability.py) cover renamed/Unicode roots. |
| LC-005–008 | [Domain engine](../../lib/domain.py) | [Functional tests](../../tests/test_functional.py): all conversion directions, exact asymmetric transform pixels, PPM round trip, bounds, multi-frame refusal, corrupted/mixed batches and retained sources. Delegate skips remain explicit. |
| LC-013 | [MCP server](../../mcp/server.py) | MCP fixtures in [common tests](../../tests/test_common.py): read-only catalog selection, root boundaries, protocol and input validation. Image comparison stays excluded because it takes another path-bearing argument. |
| LC-014 | [Generator](../../scripts/generate.py), [checker](../../scripts/check.py), [Make rules](../../lib/tool.mk), [site](../../site/), [architecture data](../../docs/diagrams/architecture.json) | `make check` validates generated drift, syntax, local links, wrapper lint and pinned actions; [repository tests](../../tests/test_repository_checks.py) exercise the checker. [Browser evidence](../../docs/evidence/README.md) remains separate from runtime tests. |
| Existing Docker/development specs | [Dockerfile](../../Dockerfile), [Docker tests](../../scripts/test-docker.py), [development launcher](../../scripts/development-container.py), locked devenv files | [Docker specification](../002-docker-runtime/spec.md), [development specification](../002-development-environments/spec.md), [launcher tests](../../tests/test_development_container.py). Isolated containers do not validate a personal library. |
| Delivery/governance | [Workflows](../../.github/workflows/), [hooks](../../.githooks/), [playbook](../../RELEASING.md), [Spec Kit](../../.specify/) | Native/hosted gates, protected squash merge, main CI, Pages and published GHCR digest checks. Integration installation alone is not capability completion. |

New commands and changed behavior must update their contract and acceptance owner.
Execution results and unavailable environments belong in [coverage](coverage.md)
and the delivery PR.
