import os
import shutil
import stat
from pathlib import Path


def install_hook() -> None:
    hook_path = Path.cwd() / ".git" / "hooks" / "pre-commit"
    if hook_path.exists():
        shutil.move(hook_path, hook_path.with_suffix(".bak"))  # type: ignore
        print("Backed up old hook to pre-commit.bak")
    with hook_path.open("w", encoding="utf-8") as f:
        f.write("#!/bin/sh\n")
        f.write("poetry run lint")
    # add +x flag
    st = os.stat(hook_path)
    os.chmod(hook_path, st.st_mode | stat.S_IEXEC)
    print("Hook successfully installed")
