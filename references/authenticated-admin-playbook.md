# Authenticated Admin Playbook

Use this file for login-gated dashboards, internal tools, admin consoles, and SaaS back offices.

## 1. Prove the auth state first

Before acting on an authenticated site, verify at least two of these:

- post-login heading or dashboard title
- signed-in user name or email
- workspace, org, project, store, or tenant label
- presence of logout, profile, or account menu
- protected route is reachable without redirecting back to login

Do not assume you are logged in just because the page loaded.

## 2. Login workflow

Use this sequence:

1. Open the protected route directly when possible
2. If redirected, snapshot the login page and identify required fields
3. Enter credentials serially, not in parallel
4. Submit using the visible login button
5. Re-snapshot the landing page
6. Verify user identity and workspace before touching data

Pause for human help on SSO, 2FA, passkeys, CAPTCHA, device approval, email codes, or policy prompts.

## 3. Back-office workflow

For admin dashboards, use this loop:

1. Record the current filters, search term, and page number
2. Apply one filter change at a time
3. Re-snapshot and verify the summary changed as expected
4. Paginate deliberately and track which records have already been seen
5. Open details only after confirming the target row ID or title
6. Return to the dashboard and verify you are still in the same workspace

## 4. Uploads and imports

- Stage files into the environment's allowed upload directory first when required
- Upload one file at a time
- Verify the uploaded file name through the UI or page state
- Wait for import completion or confirmation text
- Re-check filters and page context after the upload redirect; many back offices reset state after an import round-trip
- Report the uploaded file name and resulting status

## 5. Exports and downloads

- Record which filters were active before export
- Prefer exporting from a stable list view or detail view with explicit context
- After clicking export, verify the file path in the default download location if exposed
- Read the downloaded file when practical to ensure it contains the expected rows

## 6. Common admin-only failure modes

### Silent redirect back to login

Cause: expired session or missing cookie.

Fix: verify auth state again before assuming the action failed.

### Wrong workspace or tenant

Cause: remembered session points to another org or store.

Fix: confirm workspace label before any write, upload, export, or deletion.

### Shared-focus field corruption

Cause: multiple login or form inputs were typed in parallel on the same page.

Fix: reset the page if needed and enter fields serially, verifying the visible values before submit.

### Export mismatch

Cause: active filters differ from what the operator expects.

Fix: mention the active filters and page context in the result note.

### Import accepted but not processed

Cause: upload only staged the file; backend processing is asynchronous.

Fix: wait for a visible processing or completion signal rather than assuming success.
