#!/usr/bin/env python3
"""Create a browser workflow site recipe markdown file."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "site-recipe"


TEMPLATE = """# Site Recipe: {site_name}

## Site

- Name: {site_name}
- Entry URL: {entry_url}
- Workspace or account: [fill in]
- Auth required: [yes/no]
- Human approval points: [login / 2FA / CAPTCHA / publish / delete / payment]

## Task

- Goal: {goal}
- Inputs: [fill in]
- Expected output: [fill in]
- Stop rule: [fill in]

## Navigation landmarks

- Home or landing markers: [fill in]
- Search box markers: [fill in]
- Table or list markers: [fill in]
- Submit or export markers: [fill in]
- Success indicators: [fill in]

## Safe workflow

1. Open or focus `{entry_url}`.
2. Confirm the correct account or workspace.
3. Capture an interactive snapshot.
4. Execute the task in short inspect -> act -> verify loops.
5. Confirm the final success signal before reporting completion.

## Risky or irreversible actions

- Publish: [yes/no + notes]
- Delete: [yes/no + notes]
- Send: [yes/no + notes]
- Pay: [yes/no + notes]
- Change settings: [yes/no + notes]

## Recovery notes

- If login expires: [fill in]
- If a modal blocks interaction: [fill in]
- If the page opens a new tab: [fill in]
- If refs become stale: re-snapshot the same tab and reacquire fresh refs.
- If export runs asynchronously: [fill in]

## Verification checklist

- Correct account or workspace confirmed
- Filters or date range confirmed
- Intended entity confirmed
- Success signal captured
- Final artifact or data verified

## Example result note

- Completed/blocked: [fill in]
- Evidence: [fill in]
- Follow-up: [fill in]
"""


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Create a browser workflow site recipe markdown file."
    )
    parser.add_argument("site_name", help="Human-readable site name, e.g. 'Shopify Admin'")
    parser.add_argument("--url", default="[fill in]", help="Entry URL for the site")
    parser.add_argument("--goal", default="[fill in]", help="Primary workflow goal")
    parser.add_argument(
        "--output",
        help="Output file path. Defaults to ./references/<slug>.md",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    content = TEMPLATE.format(
        site_name=args.site_name.strip(),
        entry_url=args.url.strip(),
        goal=args.goal.strip(),
    )

    output = Path(args.output) if args.output else Path("references") / f"{slugify(args.site_name)}.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(content, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
