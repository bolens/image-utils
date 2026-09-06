# Legacy capability contracts

Retrospective audit at `ccd8366`, 2026-09-06. This extends [spec.md](spec.md)
with concrete behavior for all 38 existing image/library commands and their
supporting entry points. [Legacy coverage](legacy-coverage.md) maps source and
native acceptance owners.

## Contract authority

The [CLI reference](../../docs/cli.md), [catalog](../../docs/catalog.md),
[format limits](../../docs/formats.md), [requirements](../../docs/requirements.md),
and [MCP guide](../../docs/mcp.md) are normative parts of this specification.
Catalog-generated help remains single-sourced. Existing
[Docker](../002-docker-runtime/spec.md) and
[development](../002-development-environments/spec.md) contracts remain authoritative.
This is retrospective documentation, not a claim that these specs preceded code.

## Shared execution

- **LC-001, CLI/configuration:** Dispatcher help/list, version, generated command
  wrappers and Make aliases MUST retain the same catalog identities. JSON config
  accepts only `roots` and `jobs`; explicit paths/jobs take precedence. Config and
  path components must not be symlinks. Jobs are integers from 1 to 32, default 1.
  Unknown options/tools and invalid configuration return 2. No input matches
  return failure, including an empty tree. Image size requires WIDTHxHEIGHT with dimensions 1–99999; quality is 1–100,
  default 85. Inherited time and archive-limit flags retain parser validation
  but do not transform image contents.
- **LC-002, discovery/exclusions:** Regular-file discovery MUST recurse without
  following symlinks, deduplicate overlapping absolute paths, preserve filename
  bytes through argument arrays, and return stable bytewise path order. Extension
  matching is case-insensitive. Repeated exclusions match case-sensitive relative
  path globs, including newline names; empty patterns are invalid. Exclusions
  filter both tree-comparison sides and full expected/actual manifest sets.

- **LC-003, write planning/publication:** Every writer MUST require an explicit
  output or output directory. Explicit output requires exactly one source;
  output-directory mode appends the catalog suffix to the relative source name.
  Reject duplicate target mappings, existing destinations, source replacements,
  and targets replacing source inputs. Default execution plans writes;
  `--dry-run` overrides `--apply` and suppresses success/failure report writes.
  Applied writes verify private staging before no-clobber publication, retain
  sources, and remove failed staging. Concurrent publishers must have at most
  one winner.
- **LC-004, batches/results:** Bounded worker submission MUST retain at most
  twice the worker count outstanding jobs, preserve result order, and retain
  successful outputs when another source fails. JSON stdout separates results
  and failures; progress belongs on stderr unless quiet. Dependency failures
  return 2, other operation failures 1, successful execution 0. Requested JSON
  reports cannot overwrite existing paths and publication failure must fail the
  run. FR-008 preserves missing-executable status across domain imports.
  Read-only commands reject apply/output options but may write explicitly
  requested reports. Discovery/result memory still grows with input count.

## Image operation contracts

- **LC-005, conversion:** The 15 catalog conversion commands MUST select their
  explicit output coder independently of destination filename. The supported
  directions cover JPEG, PNG, WebP, TIFF, BMP, AVIF, HEIC, JXL, GIF and PPM as
  listed in the coverage table, subject to installed delegates. Every applied
  conversion must fully decode the result, require one output frame and preserve
  dimensions. JPEG composites transparency over white. Encoder quality retains
  its own meaning; lossy encodes do not promise pixel identity or restored detail.
  PPM/PNG interchange has an exact 8-bit RGB round-trip fixture, without promising
  preservation of comments, metadata, or container bytes.
- **LC-006, transforms:** All ten transforms produce PNG. `image-resize` fits
  the requested box without upscaling; `image-thumbnail` additionally auto-orients
  and strips profiles/tags. `image-auto-orient` follows orientation metadata;
  `image-strip` strips profiles as well as tags. Grayscale uses ImageMagick Gray
  colorspace; rotation is 90 degrees clockwise; flip is vertical and flop
  horizontal. Crop is centered with the requested dimensions and resets the page
  offset. Flatten removes alpha against white. Verification checks successful full
  decode and one frame; dimension-preserving operations check unchanged width/
  height, and resize/thumbnail check bounds. Existing asymmetric-pixel fixtures
  define flip/flop/rotate/crop/resize acceptance; they do not certify arbitrary
  color-profile fidelity.
- **LC-007, inspection:** `image-metadata` MUST return per-frame width, height,
  format, channels and bit depth. `image-verify` fully decodes and reports frame
  count; metadata identification alone is not that full verification.
  `image-orientation`, `image-colors`, and `image-alpha-audit` retain ImageMagick's
  orientation, unique-color-count and opacity text, with alpha audit also returning
  frame metadata. `image-compare` stages both selected images and reports equality
  and RMSE; ImageMagick comparison statuses 0/1 are valid results, other statuses
  are failures. A difference is a successful report, not a perceptual verdict.
- **LC-008, input and fidelity limits:** Raster input filenames MUST be copied
  to simple literal temporary paths before ImageMagick parses them, including
  bracket/glob/newline/leading-dash source names. Applied writes reject multi-frame
  input instead of dropping frames; inspection/verification can retain multiple
  frames. Missing executables return dependency failure under FR-008; missing
  delegates or malformed data are operation failures. No automatic installation
  or network access is part of a command. Image parser resource/security policy
  remains external; filename staging does not sandbox hostile payloads. RAW, PDF/
  SVG rendering, OCR, animated optimization, perceptual duplicate classification,
  and arbitrary metadata editing are outside the existing feature scope.

## Local library operations

- **LC-009, inventory and summary:** `library-inventory` MUST report absolute
  and relative paths and file sizes. `library-summary` reports count, total bytes,
  zero-byte count, min/max sizes and lowercase final-extension groups, treating
  trailing-dot names as extensionless consistently across supported Python
  versions. Summary must not read file contents, hash, or invoke codecs. Empty
  discovery is a failure, rather than a fabricated successful zero-file report.
- **LC-010, duplicates:** `library-dupes` MUST report exact SHA-256 groups with
  at least two files, hashing only files whose sizes have another candidate.
  It neither deletes nor hardlinks files; reported duplicates are data, so their
  presence does not itself change a successful exit status to failure.
- **LC-011, manifests:** `hash-manifest` MUST emit relative names, byte sizes,
  and SHA-256 without ambiguous duplicate relative paths. `hash-verify` accepts
  the documented direct manifest and command-response forms, validates schemas
  and checksums, and compares the complete expected/actual key union. Missing,
  changed, and extra files all fail. Uppercase checksum hex normalizes; malformed,
  unsafe, ambiguous or symlink manifest paths fail. A manifest is only as trusted
  as its independently supplied source.
- **LC-012, tree/path findings:** `tree-diff` MUST compare SHA-256 and presence
  across the full union, reporting left-only/right-only/changed relative names.
  Equal files are omitted and ambiguous left-side relative names fail.
  `path-audit` reports control characters, Windows-reserved punctuation,
  components over 240 filename bytes, and trailing dot/space. It does not rename
  or claim exhaustive cross-platform filename validation. Findings from either
  command are successful structured reports, not operational errors.

## MCP and support surfaces

- **LC-013, MCP:** Local newline-delimited JSON-RPC MUST require existing allowed
  roots at startup, initialize before listing/calling tools, and expose only read
  catalog operations without additional path-bearing arguments. Hash verification
  and tree comparison stay excluded. Calls accept only 1–100 string paths,
  reject symlink components and outside-root paths, ignore user config, and run
  one worker with no report paths. Notifications receive no response. Preserve
  the documented protocol negotiation, 1 MiB input and 4 MiB serialized-result
  limits, JSON-only stdout, tool `isError` and JSON-RPC error distinctions.
  Result limits apply after execution. No HTTP, authentication, cancellation,
  arbitrary argument forwarding, write mode, or background tasks are implied.
- **LC-014, maintenance/site:** Catalog generation MUST keep wrappers, tool
  Makefiles, command references and the static site synchronized. Browser search
  combines case-insensitive text with exact category selection and updates the
  count/empty state. Theme toggling retains a stored valid light/dark preference
  or the default light theme, tolerating storage denial. Copying the preview
  command reports clipboard failure and offers manual selection. These controls
  and diagrams do not gain access to media. Existing site/link/accessibility/responsive checks and Pages
  deployment gates remain part of delivery. Architecture diagram sources and
  their evidence are maintained separately from generated catalog output.
  Test fixtures, native codec notices, repository checks, hooks and Spec Kit
  updater templates are supporting contracts, not untracked runtime features.

Changes to existing behavior must update these contracts and the relevant native
fixtures together. New features require their own prospective specification.
