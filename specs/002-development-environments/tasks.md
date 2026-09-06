# Tasks

- [x] Implement locked tool environment, adapters, CI, and documentation.
- [x] Pass native devenv and rootless Podman gates, recording delegate skips.
- [ ] Verify current-head platform and existing runtime CI.
- [ ] Complete protected merge, post-merge runtime publication verification, and cleanup.

Native devenv and actual rootless Podman passed make check and all 71 discovered tests, with no delegate skips in this environment. Current-head Docker/macOS and runtime image CI remain pending. Apple execution is unverified.
