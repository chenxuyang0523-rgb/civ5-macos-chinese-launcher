#!/usr/bin/env python3
"""Audit this small repository against an explicit public-source allowlist."""

from pathlib import Path
import re
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_FILES = {
    ".gitignore", ".github/workflows/check.yml", "LICENSE", "README.md",
    "launch.py", "启动文明5.command", "docs/diagnosis.md",
    "tests/test_launch.py", "tests/test_release.py", "tools/check_release.py",
}
PATTERNS = {
    "personal macOS path": re.compile(r"/Users/[A-Za-z0-9_.-]+/"),
    "Steam account identifier": re.compile(r"\b7656119\d{10}\b"),
    "GitHub credential": re.compile(r"(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})"),
    "private key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
}


def audit_file(relative, content):
    errors = []
    if relative not in PUBLIC_FILES:
        errors.append("not on public file allowlist: " + relative)
    if len(content) > 200_000:
        errors.append("unexpectedly large file: " + relative)
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        return errors + ["non-text file: " + relative]
    for label, pattern in PATTERNS.items():
        if pattern.search(text):
            errors.append(label + ": " + relative)
    return errors


def main():
    errors = []
    files = []
    for path in ROOT.rglob("*"):
        relative = path.relative_to(ROOT)
        if any(part in {".git", "__pycache__"} for part in relative.parts):
            continue
        if path.is_symlink():
            errors.append("symlink not allowed: " + str(relative))
        elif path.is_file():
            files.append(relative.as_posix())
            errors.extend(audit_file(relative.as_posix(), path.read_bytes()))
    errors.extend("missing required file: " + name for name in sorted(PUBLIC_FILES - set(files)))
    # Inspect the Git index too: a clean working tree does not prove staged blobs
    # are clean. This also catches a staged private file that was later deleted.
    if (ROOT / ".git").exists():
        result = subprocess.run(["git", "ls-files", "--stage", "-z"], cwd=ROOT, capture_output=True, check=True)
        for entry in result.stdout.split(b"\0"):
            if not entry:
                continue
            metadata, name = entry.split(b"\t", 1)
            mode, blob, _stage = metadata.decode().split()
            relative = name.decode()
            if mode not in {"100644", "100755"}:
                errors.append("unsupported Git mode: " + relative)
            data = subprocess.run(["git", "cat-file", "blob", blob], cwd=ROOT, capture_output=True, check=True).stdout
            errors.extend(audit_file(relative, data))
    if errors:
        print("Release audit failed:\n" + "\n".join(sorted(set(errors))), file=sys.stderr)
        return 1
    print("Release audit passed: {} allowlisted text files; working tree and staged files checked.".format(len(files)))
    print("This check does not audit historical commits or guarantee detection of every secret.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
