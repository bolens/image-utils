"""Raster operations. Stage literal names before invoking ImageMagick's filename parser."""

from contextlib import contextmanager
from pathlib import Path
import shutil
import tempfile
from core import publish, run


@contextmanager
def staged(source):
    with tempfile.TemporaryDirectory(prefix="image-input-") as folder:
        path = Path(folder) / ("input" + source.suffix.lower())
        shutil.copyfile(source, path)
        yield path


def metadata(path):
    raw = run(
        ["magick", "identify", "-format", "%w\t%h\t%m\t%[channels]\t%z\n", str(path)]
    )
    rows = []
    for line in raw.decode().splitlines():
        w, h, fmt, channels, depth = line.split("\t")
        rows.append(
            {
                "width": int(w),
                "height": int(h),
                "format": fmt,
                "channels": channels,
                "depth": int(depth),
            }
        )
    if not rows:
        raise ValueError("image has no frames")
    return rows


def inspect(tool, source, args):
    op = tool["operation"]
    with staged(source) as path:
        rows = metadata(path)
        if op == "verify":
            run(["magick", str(path), "null:"])
            return {"verified": True, "frames": len(rows)}
        if op == "metadata":
            return {"frames": rows}
        if op == "orientation":
            return {
                "orientation": run(
                    ["magick", "identify", "-format", "%[orientation]", str(path)]
                ).decode()
            }
        if op == "colors":
            return {
                "colors": run(["magick", str(path), "-format", "%k", "info:"]).decode()
            }
        if op == "compare":
            from core import regular

            with staged(regular(args.against)) as other:
                import subprocess

                result = subprocess.run(
                    [
                        "magick",
                        "compare",
                        "-metric",
                        "RMSE",
                        str(path),
                        str(other),
                        "null:",
                    ],
                    capture_output=True,
                    timeout=3600,
                    check=False,
                )
                if result.returncode not in (0, 1):
                    raise RuntimeError(result.stderr.decode("utf-8", "replace"))
                return {
                    "equal": result.returncode == 0,
                    "rmse": result.stderr.decode().strip(),
                }
        if op == "alpha-audit":
            return {
                "frames": rows,
                "opaque": run(
                    ["magick", str(path), "-format", "%[opaque]", "info:"]
                ).decode(),
            }
        raise ValueError("unsupported operation: " + op)


def write(tool, source, target, args):
    op = tool["operation"]
    with staged(source) as path:
        before = metadata(path)
        # No silent flattening or dropping frames in a still-image utility.
        if len(before) != 1:
            raise ValueError(
                "multi-frame input requires an animation-specific workflow"
            )
        options = []
        if op == "resize":
            options = ["-resize", args.size + ">"]
        elif op == "thumbnail":
            options = ["-auto-orient", "-thumbnail", args.size + ">", "-strip"]
        elif op == "auto-orient":
            options = ["-auto-orient"]
        elif op == "strip":
            options = ["-strip"]
        elif op == "grayscale":
            options = ["-colorspace", "Gray"]
        elif op == "rotate":
            options = ["-rotate", "90"]
        elif op == "flip":
            options = ["-flip"]
        elif op == "flop":
            options = ["-flop"]
        elif op == "crop":
            options = ["-gravity", "center", "-crop", args.size + "+0+0", "+repage"]
        elif op == "flatten":
            options = ["-background", "white", "-alpha", "remove", "-alpha", "off"]
        elif op == "convert":
            pass
        else:
            raise ValueError("unsupported operation: " + op)
        suffix = tool["suffix"]
        if suffix in ("jpg", "jpeg"):
            options += ["-background", "white", "-alpha", "remove", "-alpha", "off"]

        def writer(temp):
            # Explicit coder makes --output naming independent of encoding choice.
            run(
                [
                    "magick",
                    str(path),
                    *options,
                    "-quality",
                    str(args.quality),
                    suffix + ":" + str(temp),
                ]
            )

        def verify(temp):
            after = metadata(temp)
            run(["magick", str(temp), "null:"])
            if len(after) != 1:
                raise ValueError("unexpected output frame count")
            if op in ("convert", "strip", "grayscale", "flip", "flop", "flatten") and (
                before[0]["width"],
                before[0]["height"],
            ) != (after[0]["width"], after[0]["height"]):
                raise ValueError("unexpected output dimensions")
            if op in ("resize", "thumbnail"):
                w, h = map(int, args.size.split("x"))
                if after[0]["width"] > w or after[0]["height"] > h:
                    raise ValueError("output exceeds requested dimensions")

        publish(target, writer, verify)
