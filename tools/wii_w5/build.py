"""Build original W5 gyro-diagnosis tools against the unchanged reviewed runtime."""
import argparse
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess

REVISIONS = {'baseline': 'b23cb416397ec4698c4a2576f7504061447b286d'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case', choices=REVISIONS, required=True)
    parser.add_argument('--virtualgamepad', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--sdl-pkg-config-path')
    parser.add_argument('--dolphin', action='store_true', help='Build the separate direct-Dolphin holder/trace variant')
    args = parser.parse_args()
    repo, output = args.virtualgamepad.resolve(), args.output.resolve()
    here = Path(__file__).resolve().parent
    if output.is_relative_to(repo) or output.is_relative_to(here.parents[1]):
        raise ValueError('Use scratch output outside both repositories')
    actual = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != REVISIONS[args.case]:
        raise ValueError('Wrong comparison revision')
    if subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain'], text=True).strip():
        raise ValueError('Use a clean comparison checkout')
    (output / 'src').mkdir(parents=True, exist_ok=True)
    dependencies = ''.join(n + '={path=' + json.dumps(str(repo / 'crates' / n)) + '}\n'
                           for n in ['gr-curated-controllers', 'gr-realization-api'])
    (output / 'Cargo.toml').write_text('[package]\nname="wii-w2-host-probe"\nversion="0.0.0"\nedition="2024"\n[dependencies]\n' + dependencies + 'serde_json="=1.0.145"\n')
    shutil.copyfile(here / ('dolphin_host_probe.rs' if args.dolphin else 'host_probe.rs'), output / 'src/main.rs')
    shutil.copyfile(here / 'Cargo.lock', output / 'Cargo.lock')
    subprocess.run(['cargo', 'build', '--locked', '--offline', '--manifest-path', str(output / 'Cargo.toml')], check=True)
    if args.dolphin:
        shutil.copyfile(here / 'dolphin_child.py', output / 'dolphin_child.py')
        subprocess.run(['cc', '-shared', '-fPIC', '-Wall', '-Wextra', '-Werror',
                        str(here / 'dolphin_trace.c'), '-ldl', '-o', str(output / 'trace.so')], check=True)
        return
    if not args.sdl_pkg_config_path:
        raise ValueError('Select the recorded SDL pkg-config directory explicitly')
    env = dict(os.environ, PKG_CONFIG_PATH='', PKG_CONFIG_LIBDIR=args.sdl_pkg_config_path)

    def pkg(*options):
        return subprocess.check_output(['pkg-config', *options, 'sdl3'], env=env, text=True).strip()

    if pkg('--modversion') != '3.2.10':
        raise ValueError('Select the recorded SDL3.2.10 installation explicitly')
    subprocess.run(['cc', '-shared', '-fPIC', '-Wall', '-Wextra', '-Werror', str(here / 'trace.c'), '-ldl', '-o', str(output / 'trace.so')], check=True)
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(here / 'sdl_probe.c'),
                    *shlex.split(pkg('--cflags', '--libs')), '-ldl', '-Wl,-rpath,' + pkg('--variable=libdir'),
                    '-o', str(output / 'sdl_probe')], check=True)


if __name__ == '__main__':
    main()
