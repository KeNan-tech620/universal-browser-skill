# Site Recipe: GitHub Public Repo Search

## Site

- Name: GitHub Search
- Entry URL: https://github.com/search?q=browser+automation&type=repositories
- Workspace or account: public, signed-out view
- Auth required: no
- Human approval points: none

## Task

- Goal: search public repositories, apply filters, paginate, and extract candidate repos
- Inputs:
  - query string
  - result type `repositories`
  - optional language filter
  - optional page stop rule
- Expected output:
  - result count
  - active filters
  - top repository names, URLs, descriptions, and visible star counts
- Stop rule: stop after the requested page count or once enough candidate repos have been collected

## Navigation landmarks

- Page heading: `repositories Search Results · <query>`
- Filter sidebar: `Filter by`
- Language links such as `Python`, `JavaScript`, `TypeScript`
- Result rows with repo heading links like `owner/repo`
- Pagination controls with `Page 1`, `Page 2`, and `Next Page`

## Safe workflow

1. Open the search URL with the requested query and repository type.
2. Confirm the main heading and total result count.
3. Capture the active query and any visible filter state.
4. Extract the visible result rows on the current page.
5. If a language filter is required, click a single language link, then re-snapshot and verify the heading and result count changed.
6. If more results are required, click `Next Page`, re-snapshot, and verify the page content changed before extracting more rows.
7. Deduplicate by repository URL.

## Risky or irreversible actions

- Publish: no
- Delete: no
- Send: no
- Pay: no
- Change settings: no

## Recovery notes

- If the search page redirects or the query resets, rebuild the URL directly with `q=` and `type=repositories`.
- If filters are unclear, record the visible heading plus the result count before extracting.
- If pagination is ambiguous, confirm at least one repo changed between pages.

## Verification checklist

- Query heading matches the requested search
- Active language filter is visible when used
- Result count captured
- At least one repository URL extracted from each page used
- Pagination state verified after each page change

## Example result note

- Completed/blocked: completed
- Evidence: `repositories Search Results · browser automation`, `9k results`, page 1 included `lightpanda-io/browser`, `SeleniumHQ/selenium`, `vercel-labs/agent-browser`; after filtering to `Python`, the page showed `2.9k results`
- Follow-up: continue to page 2 only if more candidates are needed
