# Requirements

GNU/Linux, Bash 4.3+, Python 3.11+, and GNU Make for development shortcuts. No third-party Python packages are used. Python 3.11 and 3.14 run in CI. ShellCheck is required for `make check`.

Image operations require ImageMagick **7** (`magick`). Library hashing and inventory need only Python. Codec availability depends on your ImageMagick build: AVIF/HEIC use libheif delegates, JXL uses libjxl, and WebP uses libwebp. `magick -list format` shows local support. Missing delegates are reported as operation failures. Tests mark unavailable optional encode delegates as skips.

Ubuntu 24.04 ships ImageMagick 6, so image CI builds the pinned ImageMagick 7 release shown in its workflow. The CI build is a disposable runner operation, not a user-machine installer. One preparation job builds it for both Python test jobs. The compiled installation is cached by pinned source/build recipe, dependency lists, architecture, and hosted-runner image version. Cache hits skip compilation. Cache misses use all runner cores. Runtime packages are installed separately in each test job, and a missing shared cache fails explicitly.

ImageMagick processes local raster files. Keep ImageMagick, its delegates, and its security policy maintained. Inputs use the listed raster extensions and are staged under literal filenames before invoking ImageMagick. These restrictions do not sandbox the image parser.

No automatic downloads, network enrichment, telemetry, package installation, or source deletion happens when running commands.

## Development checkouts

The checkout folder may be renamed or contain spaces and Unicode. CLI identity
and the default configuration directory remain `image-utils`. Git is required
for the disposable-checkout regression tests; normal media commands do not
require Git. Tests copy only tracked source and isolate HOME/XDG/TMPDIR state.
