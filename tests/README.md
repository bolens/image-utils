# Tests

`make test` runs shared CLI, publication, filename, configuration, and MCP tests.
`make test-functional` runs real domain operations on generated fixtures.
`make test-all` runs both tiers and repository-validation tests. Tests use disposable fixtures. CLI subprocesses receive isolated HOME, XDG config/state/cache/data/runtime paths, and TMPDIR values. Fixture encoders use the same environment.

Image tests exercise conversion delegates, transforms, metadata, animation refusal, and thumbnail bounds.

Without `magick`, the image functional suite is skipped. Unavailable encode delegates may skip individual tests or format subtests. The unittest report names every skip. CI installs the core dependencies and retains the report as an artifact. Tests require no personal media and perform no network enrichment.

Shared regression tests also cover direct manifest-response round trips, malformed and ambiguous manifests, size-filtered duplicate hashing, and bounded batch submission with stable result ordering.

Summary tests cover extension grouping, zero-byte files, overlapping roots, symlink exclusion, write refusal, MCP access, and operation without reading contents or invoking codecs.

Exclusion tests cover repeated and case-sensitive patterns, relative paths, multiline names, both comparison roots, full manifest filtering, write plans, and folder-packing refusal.

Publication checks cover writer failure, missing output, rejected verification, sync/link failures, existing destinations, and two concurrent publishers. They assert that failed outputs stay unpublished and staging files are removed.

Mixed valid/corrupt batches run with one and two workers. Functional checks verify successful output, source retention, absent failed output, nonzero exit status, and matching success/failure reports. These cases run in the existing `make test` and `make test-functional` tiers, and together in `make test-all`.

Pixel checks use a small asymmetric RGB fixture with explicit expected bytes for flip, flop, clockwise rotation, centered crop, and resize without upscaling. They also check dimensions and unchanged source bytes. This does not certify color profiles or lossy conversion fidelity.

`make test-docker` builds the runtime image and tests disposable bind-mounted
fixtures, non-root ownership, read-only root operation and CLI failure behavior.
It requires Docker and host Python 3.11+. `CONTAINER_ENGINE=podman` uses rootless
Podman locally. Docker CI runs this target on every PR and main push.

The PPM/PNG round-trip test compares exact RGB pixels and checks dry runs,
source retention, collision refusal and corrupt-input non-publication.
