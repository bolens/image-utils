#!/usr/bin/env python3
"""Exercise the built CLI image on disposable bind mounts, without networking."""
import argparse
import os
import shutil
from pathlib import Path
import subprocess
import tempfile

SUITE = 'image-utils'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', default='docker')
    parser.add_argument('--image', default=SUITE + ':local')
    args = parser.parse_args()
    uid = os.getuid() or 10001
    gid = os.getgid() if os.getuid() else 10001
    with tempfile.TemporaryDirectory(prefix=SUITE + '-docker-') as tmp:
        root = Path(tmp)
        root.chmod(0o755)
        inputs, outputs = root / 'input', root / 'output'
        inputs.mkdir()
        outputs.mkdir()
        if os.getuid() == 0:
            os.chown(outputs, uid, gid)
        options = ['--rm', '--network=none', '--read-only', '--cap-drop=ALL',
                   '--security-opt=no-new-privileges', '--tmpfs', '/tmp:rw,nosuid,nodev,mode=1777',
                   '--user', f'{uid}:{gid}', '--workdir', '/output',
                   '--mount', f'type=bind,src={inputs},dst=/input,readonly',
                   '--mount', f'type=bind,src={outputs},dst=/output']
        if Path(args.engine).name == 'podman':
            options += ['--userns=keep-id']

        def run(*command, entry=None, code=0, default_user=False):
            opts = options.copy()
            if default_user:
                i = opts.index('--user')
                del opts[i:i + 2]
                if '--userns=keep-id' in opts:
                    opts.remove('--userns=keep-id')
            if entry:
                opts += ['--entrypoint', entry]
            result = subprocess.run([args.engine, 'run', *opts, args.image, *map(str, command)],
                                    capture_output=True, text=True, timeout=180)
            if result.returncode != code:
                raise AssertionError(f'{command!r}: expected {code}, got {result.returncode}\n'
                                     f'{result.stdout}\n{result.stderr}')
            return result.stdout

        def unchanged(path, original):
            if path.read_bytes() != original:
                raise AssertionError(f'Source changed: {path.name!r}')

        def owned(path):
            if path.stat().st_uid != uid or path.stat().st_gid != gid:
                raise AssertionError(f'Output ownership differs from {uid}:{gid}: {path}')

        if run('-u', entry='id', default_user=True).strip() != '10001':
            raise AssertionError('Image must default to UID 10001')
        run('--help')
        run('not-a-tool', code=2)
        run('--version')
        source = inputs / '-雪 [*]\n.ppm'
        source.write_bytes(b'P6\n2 1\n255\n' + bytes((255, 0, 0, 0, 255, 0)))
        run('ppm-to-png', '--apply', '-o', '/output/seed.png', '/input/' + source.name)
        source = inputs / '-雪 [*]\n.png'
        shutil.move(outputs / 'seed.png', source)
        before = source.read_bytes()
        pixels = run('/input/' + source.name, '-depth', '8', 'txt:-', entry='magick')
        if '#FF0000' not in pixels or '#00FF00' not in pixels:
            raise AssertionError('PNG pixel values changed')
        for fmt in ('jpg', 'webp', 'tiff', 'avif', 'jxl', 'ppm'):
            target = '/output/converted.' + fmt
            run('png-to-' + fmt, '-o', target, '/input/' + source.name)
            if (outputs / ('converted.' + fmt)).exists():
                raise AssertionError('Planning wrote an image')
            run('png-to-' + fmt, '--apply', '-o', target, '/input/' + source.name)
            run('image-verify', target)
            owned(outputs / ('converted.' + fmt))
        target = '/output/converted.webp'
        original = (outputs / 'converted.webp').read_bytes()
        run('png-to-webp', '--apply', '-o', target, '/input/' + source.name, code=1)
        unchanged(outputs / 'converted.webp', original)
        unchanged(source, before)
        (inputs / 'bad.png').write_bytes(b'not an image')
        run('png-to-webp', '--apply', '-o', '/output/failed', '/input/bad.png', code=1)
        if (outputs / 'failed').exists():
            raise AssertionError('Failed operation published output')
        print(SUITE + ': Docker acceptance passed (no skips)')


if __name__ == '__main__':
    main()
