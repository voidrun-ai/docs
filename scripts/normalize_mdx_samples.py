#!/usr/bin/env python3
"""Normalize docs MDX samples: image field, Python create_sandbox/get_sandbox/list_sandboxes, exec .data."""

from __future__ import annotations

import re
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parent.parent

EXEC_LIKE = (
    "result",
    "run_result",
    "list_result",
    "test_result",
    "docker_check",
    "daemon_status",
    "install_result",
    "status_result",
    "pods_result",
    "svc_result",
    "mem_info",
    "cpu_info",
    "docker_stats",
)


def transform(text: str) -> str:
    text = text.replace("templateId:", "image:")
    text = text.replace("'templateId'", "'image'")
    text = text.replace('"templateId"', '"image"')
    text = text.replace("template_id=", "image=")

    text = text.replace("vr.sandboxes.create(", "vr.create_sandbox(")
    text = text.replace("vr.sandboxes.get(", "vr.get_sandbox(")

    text = re.sub(
        r"resp = vr\.sandboxes\.list\(([^)]*)\)",
        r"listed = vr.list_sandboxes(\1)",
        text,
    )
    text = text.replace("resp = vr.sandboxes.list()", "listed = vr.list_sandboxes()")

    text = re.sub(r"^\s*sandbox = resp\.data\s*\n", "", text, flags=re.M)
    text = re.sub(r"^\s*existing = resp\.data\s*\n", "", text, flags=re.M)

    text = re.sub(
        r"resp = vr\.get_sandbox\(([^)]+)\)\s*\n\s*(\w+) = resp\.data",
        r"\2 = vr.get_sandbox(\1)",
        text,
    )

    text = text.replace("len(resp.data)", "len(listed.sandboxes)")
    text = text.replace("for sb in resp.data:", "for sb in listed.sandboxes:")
    text = text.replace(
        'print(f"Total sandboxes: {len(resp.data)}")',
        'print(f"Total sandboxes: {listed.meta.total}")',
    )

    for var in EXEC_LIKE:
        text = text.replace(f"{var}.data.data.", f"{var}.data.")

    # CodeExecutionResult: common variable names from run_code / interpreter
    for var in ("code_result", "pyResult", "jsResult", "bashResult"):
        text = text.replace(f"{var}.data.stdout", f"{var}.stdout")
        text = text.replace(f"{var}.data.stderr", f"{var}.stderr")

    return text


def main() -> None:
    for path in sorted(DOCS_ROOT.rglob("*.mdx")):
        if path.parts[-2:] == ("scripts", "normalize_mdx_samples.py"):
            continue
        if "scripts" in path.parts and path.suffix != ".mdx":
            continue
        raw = path.read_text(encoding="utf-8")
        new = transform(raw)
        if new != raw:
            path.write_text(new, encoding="utf-8")
            print("updated", path.relative_to(DOCS_ROOT))


if __name__ == "__main__":
    main()
