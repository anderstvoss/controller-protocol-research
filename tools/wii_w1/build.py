"""Build the original W1 bounded probes; performs no host configuration changes."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import shlex

REVISION = '50161b913d0f82950c292465625e9cdd8854daf2'


def build(repo, output, sdl_pkg_config_path):
    """Require the recorded source head, pin Cargo, and select distro SDL explicitly."""
    repo, output = Path(repo).resolve(), Path(output).resolve()
    if output.is_relative_to(repo) or output.is_relative_to(Path(__file__).resolve().parents[2]):
        raise ValueError('Use a scratch output directory outside both repositories')
    actual = subprocess.check_output(['git', '-C', str(repo), 'rev-parse', 'HEAD'], text=True).strip()
    if actual != REVISION:
        raise ValueError('W1 probes require the exact recorded virtualgamepad revision')
    if subprocess.check_output(['git', '-C', str(repo), 'status', '--porcelain'], text=True).strip():
        raise ValueError('W1 probes require a clean virtualgamepad worktree')
    here = Path(__file__).resolve().parent
    (output / 'src').mkdir(parents=True, exist_ok=True)
    dependencies = ''.join(name + '={path=' + json.dumps(str(repo / 'crates' / name)) + '}\n'
                           for name in ['gr-curated-controllers', 'gr-realization-api'])
    (output / 'Cargo.toml').write_text('[package]\nname="wii-w1-host-probe"\nversion="0.0.0"\nedition="2024"\n[dependencies]\n' + dependencies + 'serde_json="=1.0.145"\n')
    shutil.copyfile(here / 'host_probe.rs', output / 'src/main.rs')
    shutil.copyfile(here / 'Cargo.lock', output / 'Cargo.lock')
    subprocess.run(['cargo', 'build', '--locked', '--offline', '--manifest-path', str(output / 'Cargo.toml')], check=True)
    env = dict(os.environ, PKG_CONFIG_PATH='', PKG_CONFIG_LIBDIR=sdl_pkg_config_path)
    def pkg(*args):
        return subprocess.check_output(['pkg-config', *args, 'sdl3'], env=env, text=True).strip()
    if pkg('--modversion') != '3.2.10':
        raise ValueError('Select the recorded SDL3.2.10 installation explicitly')
    library_dir = pkg('--variable=libdir')
    subprocess.run(['cc', '-std=c11', '-Wall', '-Wextra', '-Werror', str(here / 'sdl_probe.c'),
                    *shlex.split(pkg('--cflags', '--libs')), '-Wl,-rpath,' + library_dir,
                    '-o', str(output / 'sdl_probe')], check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--virtualgamepad', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--sdl-pkg-config-path', required=True)
    args = parser.parse_args()
    build(args.virtualgamepad, args.output, args.sdl_pkg_config_path)


if __name__ == '__main__':
    main()
