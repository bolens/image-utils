# Tool catalog

36 commands. Generated from `lib/catalog.json`.

| Command | Category | Mode | Purpose |
|---|---|---|---|
| [`library-inventory`](../util/library/library-inventory/) | library | read | List file sizes and relative paths. |
| [`library-dupes`](../util/library/library-dupes/) | library | read | Find exact SHA-256 duplicates without deleting files. |
| [`hash-manifest`](../util/library/hash-manifest/) | library | read | Print a JSON SHA-256 manifest for the input tree. |
| [`hash-verify`](../util/library/hash-verify/) | library | read | Verify file presence and hashes against a JSON manifest. |
| [`tree-diff`](../util/library/tree-diff/) | library | read | Compare file hashes and presence against another tree. |
| [`path-audit`](../util/library/path-audit/) | library | read | Report filename portability issues. |
| [`jpg-to-png`](../conversion/jpg-to-png/) | conversion | write | Convert single-frame JPG to PNG. |
| [`png-to-jpg`](../conversion/png-to-jpg/) | conversion | write | Convert single-frame PNG to JPG. |
| [`webp-to-png`](../conversion/webp-to-png/) | conversion | write | Convert single-frame WEBP to PNG. |
| [`png-to-webp`](../conversion/png-to-webp/) | conversion | write | Convert single-frame PNG to WEBP. |
| [`tiff-to-png`](../conversion/tiff-to-png/) | conversion | write | Convert single-frame TIFF to PNG. |
| [`png-to-tiff`](../conversion/png-to-tiff/) | conversion | write | Convert single-frame PNG to TIFF. |
| [`bmp-to-png`](../conversion/bmp-to-png/) | conversion | write | Convert single-frame BMP to PNG. |
| [`png-to-avif`](../conversion/png-to-avif/) | conversion | write | Convert single-frame PNG to AVIF. |
| [`avif-to-png`](../conversion/avif-to-png/) | conversion | write | Convert single-frame AVIF to PNG. |
| [`heic-to-png`](../conversion/heic-to-png/) | conversion | write | Convert single-frame HEIC to PNG. |
| [`jxl-to-png`](../conversion/jxl-to-png/) | conversion | write | Convert single-frame JXL to PNG. |
| [`png-to-jxl`](../conversion/png-to-jxl/) | conversion | write | Convert single-frame PNG to JXL. |
| [`gif-to-png`](../conversion/gif-to-png/) | conversion | write | Convert single-frame GIF to PNG. |
| [`png-to-ppm`](../conversion/png-to-ppm/) | conversion | write | Convert single-frame PNG to PPM. |
| [`image-resize`](../util/transform/image-resize/) | transform | write | Fit inside a bounding box without upscaling. |
| [`image-thumbnail`](../util/transform/image-thumbnail/) | transform | write | Create a compact, oriented preview with metadata removed. |
| [`image-auto-orient`](../util/transform/image-auto-orient/) | transform | write | Apply stored orientation to pixels. |
| [`image-strip`](../util/transform/image-strip/) | transform | write | Remove embedded metadata from a new PNG copy. |
| [`image-grayscale`](../util/transform/image-grayscale/) | transform | write | Create a grayscale PNG copy. |
| [`image-rotate`](../util/transform/image-rotate/) | transform | write | Rotate pixels 90 degrees clockwise. |
| [`image-flip`](../util/transform/image-flip/) | transform | write | Flip pixels vertically. |
| [`image-flop`](../util/transform/image-flop/) | transform | write | Mirror pixels horizontally. |
| [`image-crop`](../util/transform/image-crop/) | transform | write | Crop a centered rectangle. |
| [`image-flatten`](../util/transform/image-flatten/) | transform | write | Composite transparency over white. |
| [`image-metadata`](../util/audit/image-metadata/) | audit | read | Report dimensions, channels, bit depth, and frames. |
| [`image-verify`](../util/audit/image-verify/) | audit | read | Decode all image frames to check integrity. |
| [`image-orientation`](../util/audit/image-orientation/) | audit | read | Report stored image orientation. |
| [`image-colors`](../util/audit/image-colors/) | audit | read | Count unique colors. |
| [`image-compare`](../util/audit/image-compare/) | audit | read | Compare an image to a reference using RMSE. |
| [`image-alpha-audit`](../util/audit/image-alpha-audit/) | audit | read | Report transparency and channel information. |
