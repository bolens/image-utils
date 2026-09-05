from pathlib import Path
import json
import shutil
import subprocess
import unittest
from test_common import Fixture, core


@unittest.skipUnless(shutil.which("magick"), "missing dependency: ImageMagick 7")
class Image(Fixture):
    def test_ppm_png_roundtrip_preserves_pixels(self):
        pixels = bytes((255, 0, 0, 0, 255, 0, 0, 0, 255, 255, 255, 255))
        source = self.file("-雪 [*]\n.ppm", b"P6\n2 2\n255\n" + pixels)
        original = source.read_bytes()
        png, restored = self.work / "output.png", self.work / "restored.ppm"
        self.cli("ppm-to-png", "-o", png, source)
        self.assertFalse(png.exists())
        self.cli("ppm-to-png", "--apply", "-o", png, source)
        png_bytes = png.read_bytes()
        self.cli("png-to-ppm", "--apply", "-o", restored, png)
        for path in (png, restored):
            actual = subprocess.run(
                ["magick", str(path), "-depth", "8", "rgb:-"],
                check=True, capture_output=True, env=self.env, timeout=30,
            ).stdout
            self.assertEqual(actual, pixels)
        self.cli("ppm-to-png", "--apply", "-o", png, source, code=1)
        self.assertEqual(png.read_bytes(), png_bytes)
        self.assertEqual(source.read_bytes(), original)
        corrupt = self.file("corrupt.ppm", b"P6\n2 2\n255\n")
        failed = self.work / "failed.png"
        self.cli("ppm-to-png", "--apply", "-o", failed, corrupt, code=1)
        self.assertFalse(failed.exists())

    def test_transform_pixels_and_source_retention(self):
        # Every pixel differs, so swapped axes, rotation direction, and no-ops fail.
        pixels = [bytes(color) for color in (
            (255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0),
            (0, 255, 255), (255, 0, 255), (0, 0, 0), (255, 255, 255),
        )]
        source = self.file("literal [1]\n.ppm", b"P6\n4 2\n255\n" + b"".join(pixels))
        original = source.read_bytes()
        cases = (
            ("image-flip", "4x2", (4, 2), [4, 5, 6, 7, 0, 1, 2, 3]),
            ("image-flop", "4x2", (4, 2), [3, 2, 1, 0, 7, 6, 5, 4]),
            ("image-rotate", "4x2", (2, 4), [4, 0, 5, 1, 6, 2, 7, 3]),
            ("image-crop", "2x2", (2, 2), [1, 2, 5, 6]),
            ("image-resize", "8x8", (4, 2), list(range(8))),
        )
        for tool, size, dimensions, order in cases:
            with self.subTest(tool=tool):
                target = self.work / (tool + ".png")
                self.cli(tool, "--apply", "--size", size, "-o", target, source)
                actual = subprocess.run(
                    ["magick", str(target), "-depth", "8", "rgb:-"],
                    check=True, capture_output=True, env=self.env, timeout=30,
                ).stdout
                self.assertEqual(actual, b"".join(pixels[i] for i in order))
                frame = json.loads(self.cli("image-metadata", target).stdout)[
                    "results"][0]["result"]["frames"][0]
                self.assertEqual((frame["width"], frame["height"]), dimensions)
                self.assertEqual(source.read_bytes(), original)

    def test_mixed_batch_preserves_success_and_reports_failure(self):
        source = self.seed().rename(self.inputs / "zz-good.png")
        corrupt = self.file("00-corrupt.png", b"invalid input")
        before = {path: path.read_bytes() for path in (source, corrupt)}
        for jobs in (1, 2):
            with self.subTest(jobs=jobs):
                output = self.work / ("batch-" + str(jobs))
                success_log = self.work / ("success-" + str(jobs) + ".json")
                failure_log = self.work / ("failure-" + str(jobs) + ".json")
                response = json.loads(self.cli(
                    "image-resize", "--apply", "-j", jobs, "--output-dir", output,
                    "-S", success_log, "-L", failure_log, self.inputs, code=1,
                ).stdout)
                self.assertEqual([r["path"] for r in response["results"]], [str(source)])
                self.assertEqual([r["path"] for r in response["failures"]], [str(corrupt)])
                self.assertEqual(response["results"][0]["status"], "written")
                self.assertEqual(response["failures"][0]["status"], "failed")
                self.assertEqual(json.loads(success_log.read_text()), response["results"])
                self.assertEqual(json.loads(failure_log.read_text()), response["failures"])
                published = Path(response["results"][0]["output"])
                self.cli("image-verify", published)
                self.assertFalse(Path(response["failures"][0]["output"]).exists())
                self.assertEqual(list(output.iterdir()), [published])
                for path, original in before.items():
                    self.assertEqual(path.read_bytes(), original)

    def seed(self, suffix="png"):
        path = self.inputs / ("space [1]\n." + suffix)
        result = subprocess.run(
            [
                "magick",
                "-size",
                "80x60",
                "gradient:#347756-#eeee99",
                suffix + ":" + str(self.work / ("fixture." + suffix)),
            ],
            env=self.env,
            capture_output=True,
        )
        if result.returncode:
            self.skipTest("ImageMagick lacks " + suffix + " encoding")
        shutil.copyfile(self.work / ("fixture." + suffix), path)
        return path

    def test_exclude_corrupt_input_from_applied_batch(self):
        source = self.seed()
        before = core.digest(source)
        ignored = self.file("skip-corrupt.png", b"not valid media")
        output = self.work / "selected-output"
        result = json.loads(
            self.cli(
                "png-to-webp",
                "--exclude",
                "skip*",
                "--apply",
                "--output-dir",
                output,
                self.inputs,
            ).stdout
        )
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["status"], "written")
        self.assertEqual(result["failures"], [])
        self.assertEqual(core.digest(source), before)
        self.assertEqual(ignored.read_bytes(), b"not valid media")

    def test_every_converter(self):
        for tool in core.catalog():
            if tool["operation"] != "convert":
                continue
            with self.subTest(tool=tool["name"]):
                source = self.seed(tool["extensions"][0][1:])
                target = self.work / (tool["name"] + "." + tool["suffix"])
                # Detect optional output delegates using an independent fixture encode.
                probe = subprocess.run(
                    [
                        "magick",
                        "-size",
                        "2x2",
                        "xc:red",
                        tool["suffix"]
                        + ":"
                        + str(self.work / ("probe." + tool["suffix"])),
                    ],
                    env=self.env,
                    capture_output=True,
                )
                if probe.returncode:
                    self.skipTest("ImageMagick lacks " + tool["suffix"] + " encoding")
                self.cli(tool["name"], "--apply", "-o", target, source)
                self.assertTrue(source.exists())
                self.assertTrue(target.is_file())

    def test_transforms_and_inspection(self):
        source = self.seed()
        for tool in core.catalog():
            if tool["category"] == "transform":
                with self.subTest(tool=tool["name"]):
                    target = self.work / (tool["name"] + ".png")
                    self.cli(
                        tool["name"], "--apply", "--size", "30x20", "-o", target, source
                    )
                    self.cli("image-verify", target)
                    if tool["operation"] == "rotate":
                        result = json.loads(self.cli("image-metadata", target).stdout)[
                            "results"
                        ][0]["result"]["frames"][0]
                        self.assertEqual((result["width"], result["height"]), (60, 80))
            elif tool["category"] == "audit":
                extra = ["--against", source] if tool["operation"] == "compare" else []
                self.cli(tool["name"], *extra, source)

    def test_dry_run_collision_and_corruption(self):
        source = self.seed()
        target = self.work / "out.png"
        self.cli("image-resize", "-o", target, source)
        self.assertFalse(target.exists())
        self.cli("image-resize", "--apply", "--dry-run", "-o", target, source)
        self.assertFalse(target.exists())
        self.cli("image-resize", "--apply", "-o", target, source)
        self.cli("image-resize", "--apply", "-o", target, source, code=1)
        broken = self.file("broken.png", b"invalid")
        self.cli("image-verify", broken, code=1)
        failed = self.work / "failed.png"
        self.cli("image-resize", "--apply", "-o", failed, broken, code=1)
        self.assertFalse(failed.exists())

    def test_animation_refused(self):
        path = self.inputs / "animated.gif"
        subprocess.run(
            ["magick", "-size", "8x8", "xc:red", "xc:blue", str(path)],
            check=True,
            env=self.env,
            capture_output=True,
        )
        target = self.work / "flattened.png"
        self.cli("gif-to-png", "--apply", "-o", target, path, code=1)
        self.assertFalse(target.exists())

    def test_parallel_and_size(self):
        self.seed()
        self.seed("jpg")
        out = self.work / "thumbs"
        self.cli(
            "image-thumbnail",
            "--apply",
            "--size",
            "32x24",
            "-j",
            "2",
            "--output-dir",
            out,
            self.inputs,
        )
        self.assertEqual(len(list(out.iterdir())), 2)
        result = json.loads(self.cli("image-metadata", out).stdout)
        for row in result["results"]:
            frame = row["result"]["frames"][0]
            self.assertLessEqual(frame["width"], 32)
            self.assertLessEqual(frame["height"], 24)


if __name__ == "__main__":
    unittest.main()
