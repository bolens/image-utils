# Docker

Build from the repository root:

```sh
docker build --pull -t image-utils:local .
docker run --rm image-utils:local --help
make test-docker
```

The image uses digest-pinned Debian 13 and distribution runtime packages.
Package versions resolve at build time. Rebuild with `--pull --no-cache` to pick
up package security updates, and review base digest updates separately.
The published image targets Linux amd64. Other Linux architectures may build
from this Dockerfile, but are not validated by the current CI.

## Published images

Main pushes build, test and publish `ghcr.io/bolens/image-utils:latest` and
`ghcr.io/bolens/image-utils:sha-<full-commit>`. PRs and the weekly scheduled check
build and test only. The publication job tests the exact local image it pushes.
No host tools, release tags or personal access tokens are installed by the image.
Use a registry digest for deployment pinning because tags can move.

```sh
docker pull ghcr.io/bolens/image-utils:latest
```

GHCR package visibility is managed separately from repository visibility. If the
package is private, authenticate with an account that can read it before pulling.
The workflow uses its repository-scoped `GITHUB_TOKEN` with `packages: write`.
See [GitHub's registry guide](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry).

## Files and ownership

The image defaults to UID/GID 10001. On Linux, use your UID/GID so new files belong
to you. Create writable output directories before mounting them. Container paths,
including paths in configuration and manifests, must refer to the mounted paths.
Only bind mounts make media available to the container. No host library is copied
into the image. The build context allows runtime source directories only.

Mount inputs read-only and outputs separately. Writes still require `--apply`.
This example previews the operation:

```sh
mkdir -p input output
docker run --rm --network=none --read-only --tmpfs /tmp \
  --cap-drop=ALL --security-opt=no-new-privileges \
  --user "$(id -u):$(id -g)" \
  --mount "type=bind,src=$PWD/input,dst=/input,readonly" \
  --mount "type=bind,src=$PWD/output,dst=/output" \
  image-utils:local png-to-webp -o /output/picture.webp /input/picture.png
```

Add `--apply` after the tool name to write. Sources remain intact and existing
outputs are refused. Quote filenames containing whitespace or shell characters.

ImageMagick 7 uses the same pinned source revision and build recipe as native CI,
with Debian runtime delegates. The compiler and Git stay in the build stage.
Docker builds default to four compiler jobs; use `--build-arg IM_BUILD_JOBS=N`
to set a different build concurrency. Docker tests require
PNG, JPEG, WebP, TIFF, AVIF, JXL and PPM conversion. The pinned build
uses its upstream security policy. Use `--entrypoint magick IMAGE -list format` to inspect
the installed delegates. See [formats](formats.md).

For the read-only stdio MCP server, use `-i` without `-t`, select
`--entrypoint python3`, and pass `/opt/image-utils/mcp/server.py` after the image
name. Configure its allowed roots as described in [MCP](mcp.md). No port is exposed.

## Runtime state and validation

HOME and XDG directories default under writable `/tmp`, so an arbitrary numeric
UID works with a read-only root filesystem. State and logs disappear with the
container. For persistent state, mount a writable directory and set
`XDG_STATE_HOME` to that path. Mount configuration read-only and set
`XDG_CONFIG_HOME` when needed. Filesystem permissions still apply to all mounts.

`make docker-build` builds only. `make test-docker` also runs real disposable
conversions, source/output comparisons, unusual filenames, ownership checks,
non-root defaults, dry runs and failures with a read-only root and no network.
Host Python 3.11+ is needed for tests. Rootless Podman can run the same checks via
`make test-docker CONTAINER_ENGINE=podman`. Existing native suites remain separate.

To roll back, run the previously verified registry digest. Never overwrite source
media as a recovery step. Publishing containers does not change CLI VERSION or
create a versioned source release.
