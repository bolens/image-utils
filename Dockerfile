FROM docker.io/library/debian:trixie-slim@sha256:d7e12182ce18b85b93007c1dedf31f2d29e01ccf3182cc4017c709b6259bc132 AS imagemagick-build
ARG IM_BUILD_JOBS=4
# Reuse the same reviewed ImageMagick source revision and build recipe as native CI.
COPY ci/imagemagick-build-deps.txt /tmp/build-deps.txt
COPY scripts/build-imagemagick.sh /tmp/build-imagemagick.sh
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates git \
    && xargs -r apt-get install -y --no-install-recommends < /tmp/build-deps.txt \
    && /tmp/build-imagemagick.sh /opt/imagemagick \
    && rm -rf /var/lib/apt/lists/*

FROM docker.io/library/debian:trixie-slim@sha256:d7e12182ce18b85b93007c1dedf31f2d29e01ccf3182cc4017c709b6259bc132
LABEL org.opencontainers.image.source="https://github.com/bolens/image-utils"
# Use maintained distribution packages. Refresh the base digest and rebuild for updates.
# hadolint ignore=DL3008
RUN apt-get update \
    && apt-get install -y --no-install-recommends bash python3 libjpeg62-turbo libpng16-16t64 libtiff6 \
        libwebp7 libwebpdemux2 libwebpmux3 libheif1 libjxl0.11 libopenjp2-7 liblcms2-2 \
        libheif-plugin-aomenc libheif-plugin-aomdec libheif-plugin-x265 libheif-plugin-libde265 \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd --gid 10001 utils \
    && useradd --uid 10001 --gid 10001 --no-log-init --create-home utils
COPY --from=imagemagick-build /opt/imagemagick /opt/imagemagick
ENV PATH=/opt/imagemagick/bin:$PATH \
    LD_LIBRARY_PATH=/opt/imagemagick/lib \
    LANG=C.UTF-8 \
    PYTHONDONTWRITEBYTECODE=1 \
    HOME=/tmp \
    XDG_CONFIG_HOME=/tmp/config \
    XDG_CACHE_HOME=/tmp/cache \
    XDG_STATE_HOME=/tmp/state \
    XDG_DATA_HOME=/tmp/data \
    XDG_RUNTIME_DIR=/tmp/runtime
WORKDIR /opt/image-utils
COPY lib/ ./lib/
COPY conversion/ ./conversion/
COPY util/ ./util/
COPY bin/ ./bin/
COPY VERSION LICENSE ./
COPY mcp/*.py ./mcp/
USER 10001:10001
WORKDIR /data
ENTRYPOINT ["/opt/image-utils/bin/image-utils"]
CMD ["--help"]
