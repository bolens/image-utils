# Formats and limits

The catalog covers JPEG, PNG, WebP, TIFF, BMP, AVIF, HEIC, JXL, GIF, and PPM where installed delegates support them. PNG is the default transform output. JPEG outputs composite transparency over white. JPEG and typical AVIF/WebP encodes are lossy and cannot restore detail. `--quality` defaults to 85 and follows each encoder's meaning.

Conversion verifies full decoding, a single output frame, and unchanged dimensions. Resizing and thumbnails verify the bounding box. This checks structural output integrity, not pixel equivalence or colorimetric fidelity. Profiles follow ImageMagick defaults unless the operation strips them. Metadata stripping and thumbnails remove profiles as well as tags, so review color-sensitive workflows before using those operations.

Multi-frame inputs can be inspected and verified, but transformations reject them rather than silently dropping frames. RAW development, PDF/SVG rendering, animated image optimization, OCR, perceptual duplicate classification, and metadata editing are not implemented. Exact file duplicates use SHA-256. RMSE comparison describes pixel differences and is not a perceptual similarity claim.

Image inputs are copied into temporary files with simple names before ImageMagick parses them. This preserves literal source names containing brackets, globs, newlines, or leading dashes.
