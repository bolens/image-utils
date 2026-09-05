#!/usr/bin/env bash
# CI/container dependency build. Installs under the explicit prefix, never system paths.
set -euo pipefail
if [[ $# != 1 || $1 != /* ]]; then
  echo 'usage: build-imagemagick.sh ABSOLUTE_PREFIX' >&2
  exit 2
fi
prefix=$1
revision=fb965f1b54a65ddb633f8c2eac4452c782c66d7f # ImageMagick 7.1.2-31
build_dir=$(mktemp -d "${RUNNER_TEMP:-${TMPDIR:-/tmp}}/image-utils-build.XXXXXX")
trap 'rm -rf -- "$build_dir"' EXIT

git init "$build_dir/source"
git -C "$build_dir/source" remote add origin https://github.com/ImageMagick/ImageMagick.git
git -C "$build_dir/source" fetch --depth=1 origin "$revision"
git -C "$build_dir/source" checkout --detach FETCH_HEAD
cd -- "$build_dir/source"
./configure --prefix="$prefix" --without-perl --disable-docs --disable-openmp --disable-static --without-x
make -j"${IM_BUILD_JOBS:-$(nproc)}"
make install
LD_LIBRARY_PATH="$prefix/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}" "$prefix/bin/magick" -version
