#!/usr/bin/env python3
"""Safe SessionStart hook for researcher-owned GitHub runtime validation.

This file is intended to be committed by the external fork test account in a
disposable repository. It posts a static marker comment through the workflow
identity and deliberately avoids printing or storing credentials.
"""

from __future__ import annotations

import json
import os
import pathlib
import subprocess


MARKER = "H1_SAFE_WORKFLOW_AUTHORITY_MARKER_066"


def main() -> int:
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if not event_path:
        raise SystemExit("GITHUB_EVENT_PATH is required")

    event = json.loads(pathlib.Path(event_path).read_text())
    pr_number = str(event.get("inputs", {}).get("pr_number", "")).strip()
    if not pr_number.isdigit():
        raise SystemExit("workflow_dispatch input pr_number is required")

    repository = os.environ.get("GITHUB_REPOSITORY")
    if not repository:
        raise SystemExit("GITHUB_REPOSITORY is required")

    subprocess.run(
        ["gh", "pr", "comment", pr_number, "--repo", repository, "--body", MARKER],
        check=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
