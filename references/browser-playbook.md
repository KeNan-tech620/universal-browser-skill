# Browser Playbook

Use this file after loading `SKILL.md` when the task needs more specific tactics.

## 1. Start with the smallest reliable loop

Prefer this sequence:

1. Open or focus the page
2. Capture an interactive snapshot
3. Identify candidate elements by role, label, or visible text
4. Take one action
5. Re-snapshot
6. Verify the expected state change

Avoid long blind action chains. Browser work is fragile when the page is dynamic.

## 2. Extraction patterns

### Article or details page

Extract only the fields the task needs, usually from this list:

- title
- subtitle or summary
- author
- publish time or update time
- main body
- tags or categories
- media URLs
- primary CTA or status

Verify that the title or unique identifier matches the intended page before reporting.

### Search results or feeds

Capture a stable schema before iterating:

- item title
- item URL
- author or source
- timestamp
- score, likes, comments, views, or price if relevant

Deduplicate by URL or another stable key.

### Tables and dashboards

Record:

- visible column names
- active sort order
- filters or date range
- total row count if available

If the table is virtualized, do not assume invisible rows were captured. Scroll or paginate deliberately.

## 3. Pagination and infinite scroll

Define a stop rule before iterating:

- maximum pages
- maximum items
- date threshold
- stop when no new IDs appear

For each iteration:

1. Capture page number or a visible anchor item
2. Advance one page or scroll one chunk
3. Re-snapshot
4. Confirm that new items appeared
5. Merge and deduplicate

Stop immediately when the next step produces no new items.

## 4. Forms and editors

Before filling a form, inspect:

- field labels
- placeholders
- helper text
- required markers
- current default values
- validation messages

Use this order:

1. Fill stable text fields
2. Select dropdowns, radios, or toggles
3. Upload files
4. Review summary or preview
5. Submit
6. Verify success

Typical success signals:

- success toast
- redirect to a detail page
- new row in a table
- saved timestamp
- disabled dirty-state indicator
- visible confirmation message

## 5. Authenticated sites

Use the user-approved browser session when possible.

Rules:

- Never ask for passwords in chat if an attached logged-in browser is available.
- Pause for the human on login, 2FA, CAPTCHA, passkeys, email approvals, or device confirmations.
- After login, re-snapshot the post-login page and verify the active account or workspace.
- Mention the active workspace or account in the final answer for anything business-critical.

## 6. Uploads and downloads

### Uploads

Before uploading:

- confirm the local file path exists
- verify the file name and type
- check size limits if visible

After uploading:

- verify the file name is shown in the UI
- wait for processing indicators to finish
- confirm the attachment appears in the final saved state

### Downloads

Before downloading:

- record the expected file type and file name pattern
- verify whether the action generates a file immediately or queues a background export

After downloading:

- confirm the file exists at the expected path if the tool exposes it
- mention the file name in the result

## 7. Common failure modes

### Stale refs

Cause: the page re-rendered.

Fix: re-snapshot the same tab and reacquire fresh refs.

### Wrong tab or wrong workspace

Cause: popup, redirect, or auto-opened tab.

Fix: focus the intended tab and verify page identity before continuing.

### Hidden modal or cookie banner

Cause: overlay blocks clicks.

Fix: close or accept the overlay explicitly, then re-snapshot.

### Infinite spinner or queued export

Cause: background work is still running.

Fix: wait for a concrete success signal, not an arbitrary time delay.

### Action ambiguity

Cause: there are multiple similar buttons or links.

Fix: anchor the element by nearby text, section heading, row context, or dialog title.

## 8. Site recipe guidance

Create a site recipe when any of these are true:

- the task will repeat
- the site has login or workspace switching
- the workflow has 4 or more steps
- the page has risky actions
- the site is dynamic enough that future runs need landmarks and recovery notes

Use `references/site-recipe-template.md` and generate a skeleton with `scripts/new_site_recipe.py`.
