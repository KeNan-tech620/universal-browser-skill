---
name: universal-browser-skill
description: Universal browser automation and extraction for AI agents working across arbitrary websites, web apps, dashboards, and admin consoles. Use when an agent must inspect a page, navigate a multi-step flow, search, extract structured data, fill forms, upload or download files, handle pagination or infinite scroll, work inside an authenticated browser session with user approval, or turn a repeated web workflow into a reusable site recipe. Best for browser-tool-driven tasks where no stable API is available or the UI is the source of truth.
---

# Universal Browser Skill

Use this skill to complete browser-first tasks on unknown or semi-known websites without hardcoding brittle selectors up front.

## Quick start

1. Classify the goal: extract, act, or monitor.
2. Open or focus the target site.
3. Capture an interactive snapshot with stable refs.
4. Work in short loops: inspect -> act -> re-snapshot -> verify.
5. Report the result with evidence.
6. If the workflow is likely to repeat, create a site recipe with `scripts/new_site_recipe.py` and `references/site-recipe-template.md`.
7. For login-gated dashboards or back-office tools, read `references/authenticated-admin-playbook.md` first.
8. For local repeatable verification, run `scripts/serve_test_backend.py` and use it as a login-state + admin-flow fixture.

## Operating rules

- Prefer semantic page understanding over raw CSS selectors.
- Reuse the same tab `targetId` after each snapshot.
- Prefer `refs="aria"` or other stable tool-native refs when supported.
- Re-snapshot after navigation, modal changes, accordion expansion, filtering, sorting, or list refresh.
- Change one thing at a time, then verify the page state before continuing.
- Serialize field entry on the same page. Do not run multiple text-entry actions in parallel unless the environment explicitly guarantees isolated focus.
- Stop and ask for help on login approval, 2FA, CAPTCHA, payment, posting, deletion, or other irreversible actions.
- Confirm uploads and downloads by checking the visible file name, success toast, or resulting file path.
- If the host environment restricts upload paths or uses a default download directory, stage files into the allowed upload location first and verify the final download path after clicking.
- Keep destructive actions explicit. Do not rely on ambiguous buttons like "Submit" or "Delete" without a final state check.

## Workflow

### 1. Profile the site

Capture the minimum context needed to work safely:

- Entry URL
- Current auth state
- Page type: article, search results, feed, table, dashboard, form, wizard, settings page
- Primary entities: rows, cards, messages, products, orders, files, users
- Risks: publication, deletion, money movement, account settings, messaging, rate limits

For repeat work, store these details in a site recipe.

### 2. Choose the execution pattern

#### A. Single-page extraction

Use for one article, one profile, one details page, or one dashboard view.

- Capture the page structure first.
- Extract only the fields needed for the task.
- Verify that the content belongs to the intended entity before reporting.

#### B. Search or filter flow

Use for keyword search, faceted filtering, or feed narrowing.

- Find the visible search box or filter controls from the snapshot.
- Apply one filter at a time.
- Re-snapshot and confirm that the result set changed as expected.
- Record the exact filters used in the final answer.

#### C. Paginated or infinite list

Use for tables, feeds, result pages, or admin lists.

- Define a stop rule before iterating: item count, time window, page count, or "until no more results".
- Deduplicate by URL, ID, title, timestamp, or a stable tuple.
- Re-snapshot after each page turn or lazy-load expansion.
- Stop when the stop rule is met, not when the page merely looks long enough.

#### D. Form or wizard

Use for sign-up flows, content editors, admin panels, or settings pages.

- Read labels, helper text, defaults, and validation hints before typing.
- Fill the form field-by-field, verifying each critical field.
- Prefer explicit submit buttons over pressing Enter blindly.
- After submission, verify success through a toast, redirect, saved state, new row, or confirmation message.

#### E. Repeated workflow

Use when the same site action will recur.

- Create a site recipe.
- Save stable page landmarks, risky steps, success signals, and common failure modes.
- Keep the recipe short enough to reuse without re-discovering the site from scratch.

## Recovery rules

- If refs become stale, re-snapshot the same tab instead of guessing.
- If the page changes unexpectedly, identify the new page type before acting again.
- If a hidden dialog blocks progress, dismiss or resolve it explicitly.
- If the site needs human approval, pause and request it rather than working around protections.
- If anti-bot friction appears, slow down, prefer visible UI actions, and avoid repeated retries that could lock the account.

## Output contract

When finishing a task, return:

1. Result: completed, partially completed, or blocked
2. What was actually done
3. Evidence: URLs, titles, counts, timestamps, exported file names, or visible confirmation text
4. Any remaining blocker or follow-up

## Resources

- Read `references/browser-playbook.md` for extraction, tables, forms, pagination, and auth handoff patterns.
- Read `references/authenticated-admin-playbook.md` for login-state and complex back-office workflows.
- Read `references/site-recipe-template.md` when documenting a repeated site workflow.
- Read `references/ubs-admin-fixture-recipe.md` for a complete authenticated admin example.
- Read `references/github-public-repo-search.md`, `references/github-public-repo-inspection.md`, and `references/github-release-asset-download.md` for real public-site examples.
- Read `references/x-authenticated-search.md` and `references/x-public-access-boundary.md` for X/Twitter-specific guidance, auth requirements, and tested fallbacks.
- Read `references/content-platform-matrix.md` for the current content-platform access map, plus the platform-specific files for Hacker News, Reddit, YouTube, Bilibili, and Douyin.
- Run `scripts/new_site_recipe.py` to create a reusable site recipe skeleton.
- Run `scripts/serve_test_backend.py` to spin up a local authenticated admin fixture for stress tests.
