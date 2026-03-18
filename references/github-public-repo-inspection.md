# Site Recipe: GitHub Public Repo Inspection

## Site

- Name: GitHub Repository Page
- Entry URL: https://github.com/KeNan-tech620/universal-browser-skill
- Workspace or account: public, signed-out view
- Auth required: no
- Human approval points: none

## Task

- Goal: inspect a public repository page and capture core metadata without using the API
- Inputs:
  - repository URL
  - optional sections to inspect: code root, releases, topics, license, issues tab
- Expected output:
  - owner, repo name, visibility
  - default branch or tag context
  - latest commit message and timestamp if visible
  - top-level folders and files
  - repo description, topics, release summary, and visible stars/forks/watchers
- Stop rule: stop after the requested metadata is verified on the repo page or adjacent tabs

## Navigation landmarks

- Header `owner / repo`
- Visibility badge such as `Public`
- Repository nav tabs: `Code`, `Issues`, `Pull requests`, `Actions`, `Security`
- File table under `Folders and files`
- `About` sidebar block with description and topics
- `Releases` sidebar block with latest release link

## Safe workflow

1. Open the repository page and verify the `owner / repo` heading.
2. Capture visibility and the main navigation tabs.
3. Read the `Folders and files` table for the latest commit message and top-level structure.
4. Inspect the `About` sidebar for description, topics, and license.
5. If release information is needed, follow the latest release link from the sidebar and re-snapshot there.
6. Report only the metadata that is visibly confirmed on the page.

## Risky or irreversible actions

- Publish: no
- Delete: no
- Send: no
- Pay: no
- Change settings: no

## Recovery notes

- If the file table is collapsed by layout changes, re-snapshot and anchor on `Folders and files`.
- If the repo page lands on a tagged tree instead of `main`, mention the visible branch or tag context explicitly.
- If stars or watchers are hidden behind login prompts, use the visible counts only.

## Verification checklist

- Owner and repo name confirmed
- Visibility confirmed
- Latest commit message or hash captured
- Top-level file/folder names captured
- About description and topics captured when present
- Release summary captured when requested

## Example result note

- Completed/blocked: completed
- Evidence: repo `KeNan-tech620/universal-browser-skill` showed `Public`, latest commit `feat: ship v2 authenticated admin fixture and playbook`, top-level entries `dist`, `references`, `scripts`, `SKILL.md`, and topics `browser-automation`, `ai-agents`, `web-automation`, `agent-skill`, `openclaw`
- Follow-up: open the release page if the asset or tag details are needed
