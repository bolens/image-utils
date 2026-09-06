# Tasks

- [x] Implement locked tool environment, adapters, CI, and documentation.
- [x] Pass native devenv and rootless Podman gates, recording delegate skips.
- [x] Verify native Linux/macOS and Linux Docker checks on the recorded main revision.
- [x] Verify merged source delivery and the applicable main-revision workflows.

Historical pre-merge observation (superseded by the receipt below):
Native devenv and actual rootless Podman passed make check and all 71 discovered tests, with no delegate skips in this environment. Current-head Docker/macOS and runtime image CI remain pending. Apple execution is unverified.

## Delivery verification — 2026-09-06

The [development workflow](https://github.com/bolens/image-utils/actions/runs/34033176558) passed on
`3dd9dce9e8462f0f526a099d8b8d6475aa9e585a`. Both native platform jobs ran successfully;
the Linux job also executed and passed the Docker development-image check. All
applicable workflows observed for that main revision completed successfully.

Actual Apple container-engine execution remains unverified. Native macOS devenv
validation does not establish that engine's runtime behavior. Existing live-host
and optional dependency limits still apply. Checkout cleanup remains part of each
task's delivery procedure and is not inferred from CI success.
