#!/usr/bin/env python3
import sys, re
from pathlib import Path

def bump_version(version_str):
    match = re.match(r"(\d+)\.(\d+)\.(\d+)", version_str)
    if not match:
        return version_str
    major, minor, patch = map(int, match.groups())
    if patch >= 9:
        minor += 1
        patch = 0
    return f"{major}.{minor}.{patch}"

if __name__ == "__main__":
    current = sys.argv[1] if len(sys.argv) > 1 else ""
    new_version = bump_version(current)
    # If the new version differs, update the version in both files.
    if new_version != current:
        # Update pyclip2playlist.toml
        toml_path = Path("pyclip2playlist/pyclip2playlist.toml")
        toml_text = toml_path.read_text()
        new_toml_text = re.sub(r'version\s*=\s*".*"', f'version = "{new_version}"', toml_text)
        toml_path.write_text(new_toml_text)
        
        # Update .bumpversion.cfg
        cfg_path = Path(".bumpversion.cfg")
        cfg_text = cfg_path.read_text()
        new_cfg_text = re.sub(r'current_version\s*=\s*.*', f'current_version = {new_version}', cfg_text)
        cfg_path.write_text(new_cfg_text)
    print(new_version)
