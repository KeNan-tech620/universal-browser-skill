# Site Recipe: Hacker News Public Reading

## Site

- Name: Hacker News
- Entry URL: https://news.ycombinator.com/
- Workspace or account: public, signed-out view
- Auth required: no
- Human approval points: none

## Task

- Goal: inspect the HN front page or an item page and extract ranked stories plus discussion links
- Inputs:
  - front page or item URL
  - optional number of stories to collect
- Expected output:
  - rank
  - story title
  - outbound URL or source domain
  - points, author, age, and comment count when visible
- Stop rule: stop after the requested number of stories or after the target item page is verified

## Navigation landmarks

- Top bar links: `new`, `past`, `comments`, `ask`, `show`, `jobs`
- Ranked rows with numeric rank like `1.`
- Story links and source domains
- Metadata rows with points, author, age, and comment count
- `More` pagination link

## Safe workflow

1. Open the HN page and confirm the top navigation row.
2. Extract rank, title, domain, and metadata from each visible story block.
3. Follow the comment or age link to inspect a specific discussion when needed.
4. Use `More` only when more stories are explicitly requested, then re-snapshot and verify the story list changed.

## Verification checklist

- At least one ranked story captured with title and metadata
- Comment count or discussion link captured when present
- Page type identified as front page or item page

## Example result note

- Completed/blocked: completed
- Evidence: front page showed ranked stories like `Rob Pike's 5 Rules of Programming`, `Nightingale`, and `Death to Scroll Fade`, with visible points, authors, ages, and comment counts
- Follow-up: open an item page when discussion content is needed
