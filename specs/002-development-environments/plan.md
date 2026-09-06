# Implementation plan

Own devenv configuration and lock, container helper/tests, CI, ignores, and developer documentation. Reuse native checks and functional tests rather than substituting an unrelated smoke command. Preserve engine, catalog, generated site, and VERSION.

Run native devenv and actual Podman, then current-head Linux Docker/macOS CI. Review archive/image privacy and existing Docker runtime delivery. No source release version change is required. Apple runtime execution needs a suitable Mac and remains separately unverified.
