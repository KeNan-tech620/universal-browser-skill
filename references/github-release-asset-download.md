# Site Recipe: GitHub Release Asset Download

## Site

- Name: GitHub Releases
- Entry URL: https://github.com/KeNan-tech620/universal-browser-skill/releases/tag/v2.0.0
- Workspace or account: public, signed-out view
- Auth required: no
- Human approval points: none

## Task

- Goal: open a public GitHub release, verify the asset list, download a specific asset, and confirm the downloaded file on disk
- Inputs:
  - release URL
  - target asset name
  - expected download directory when known
- Expected output:
  - release title and tag
  - release notes summary
  - asset name, visible size, and downloaded file path
  - optional artifact integrity check by listing archive contents
- Stop rule: stop after the target asset exists on disk and matches the expected artifact name

## Navigation landmarks

- Breadcrumb `Releases > <tag>`
- Release heading such as `Universal Browser Skill v2.0.0`
- Tag line `Tag v2.0.0`
- Assets section expanded with named links
- Asset link such as `universal-browser-skill.skill`

## Safe workflow

1. Open the release URL and verify the release title and tag.
2. Read the release notes summary and confirm the `Assets` section is expanded.
3. Locate the target asset by exact file name.
4. Click the asset link.
5. Verify the file appears in the host's download directory.
6. If the artifact is an archive or package, inspect it locally to confirm it contains the expected files.

## Risky or irreversible actions

- Publish: no
- Delete: no
- Send: no
- Pay: no
- Change settings: no

## Recovery notes

- If clicking the asset does not visibly change the page, check the default download directory immediately.
- If multiple files with the same name exist, sort by modification time and use the newest path.
- If the downloaded file is suspiciously small, inspect its contents before reporting success.

## Verification checklist

- Release title and tag confirmed
- Asset file name and visible size captured
- Download path confirmed on disk
- Artifact contents inspected when practical

## Example result note

- Completed/blocked: completed
- Evidence: release `Universal Browser Skill v2.0.0`, asset `universal-browser-skill.skill`, visible size `15.5 KB`, downloaded file `/root/Downloads/universal-browser-skill.skill`, and archive contents included `SKILL.md`, `scripts/serve_test_backend.py`, and the `references/` files
- Follow-up: if a user wants installation, pass the downloaded `.skill` file into the appropriate skill-install flow
