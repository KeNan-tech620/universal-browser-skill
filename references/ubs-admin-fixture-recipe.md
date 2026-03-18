# Site Recipe: UBS Admin Fixture

## Site

- Name: UBS Admin Fixture
- Entry URL: http://127.0.0.1:8124/admin
- Workspace or account: `alpha` or `beta`
- Auth required: yes
- Human approval points: none

## Task

- Goal: Log in, filter dashboard records, paginate, open detail, upload import, and download export
- Inputs:
  - username: `admin`
  - password: `demo-pass`
  - workspace: `alpha` or `beta`
  - optional dashboard filters: `q`, `status`
  - optional upload file staged in the allowed upload directory
- Expected output:
  - verified login state
  - result summary and page number
  - selected record detail
  - uploaded file name if used
  - exported CSV path and contents summary
- Stop rule: stop after the target detail record is verified and the export file is confirmed on disk

## Navigation landmarks

- Home or landing markers: heading `UBS Admin Login` or `UBS Admin Dashboard`
- Search box markers: textbox `Search`
- Table or list markers: result summary plus record table with `ORD-*` IDs
- Submit or export markers: button `Apply filters`, link `Export CSV`, link `Download report`, button `Upload import`
- Success indicators: `Signed in as admin in workspace ...`, `Last upload: ...`, downloaded `ubs-export.csv`

## Safe workflow

1. Open `http://127.0.0.1:8124/admin` and expect a redirect to login when unauthenticated.
2. Fill `Username`, `Password`, and `Workspace` serially, then click `Sign in`.
3. Verify the dashboard heading, signed-in user, and workspace label.
4. Apply filters one at a time and re-snapshot until the result summary matches expectations.
5. Paginate with `Next page`, then verify the new page number before opening a record.
6. Open a detail page, verify the record ID in the heading, then trigger `Download report`.
7. If testing imports, upload one file and confirm `Last upload: <filename>` appears after the redirect.
8. Confirm the exported CSV exists in the default download directory and inspect the contents.

## Risky or irreversible actions

- Publish: no
- Delete: no
- Send: no
- Pay: no
- Change settings: no

## Recovery notes

- If login expires: reopen `/admin` and verify that the site redirects back to login, then sign in again.
- If a modal blocks interaction: not expected in this fixture.
- If the page opens a new tab: not expected in this fixture.
- If refs become stale: re-snapshot the same tab and reacquire fresh refs.
- If export runs asynchronously: not applicable; this fixture downloads immediately.
- If filters reset after an upload redirect: re-verify the dashboard state and reapply filters before exporting.

## Verification checklist

- Correct workspace confirmed in the dashboard header
- Filters and page number confirmed in the result summary
- Intended record ID confirmed on the detail page
- Uploaded file name confirmed after import
- Final CSV file verified on disk and read back

## Example result note

- Completed/blocked: completed
- Evidence: logged into workspace `beta`, reached page 2, opened `ORD-1004`, uploaded `admin-import.csv`, downloaded `/root/Downloads/ubs-export.csv`
- Follow-up: if the upload redirect resets filters, reapply them before exporting
