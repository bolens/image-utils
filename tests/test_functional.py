import json
import shutil
import subprocess
import unittest
from test_common import Fixture, core


@unittest.skipUnless(shutil.which("magick"), "missing dependency: ImageMagick 7")
class Image(Fixture):
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
            capture_output=True,
        )
        if result.returncode:
            self.skipTest("ImageMagick lacks " + suffix + " encoding")
        shutil.copyfile(self.work / ("fixture." + suffix), path)
        return path

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
