# Site Recipe: Bilibili Public Search

## Site

- Name: Bilibili Search
- Entry URL: https://search.bilibili.com/all?keyword=AI
- Workspace or account: public, signed-out view
- Auth required: no for basic search result browsing
- Human approval points: login only if later actions require commenting or account features

## Task

- Goal: search public Bilibili content and extract visible video candidates
- Inputs:
  - search keyword
  - optional sort mode
  - optional page number
- Expected output:
  - active keyword
  - visible category counts
  - top visible video titles, URLs, authors, dates, play counts, and durations
- Stop rule: stop after the requested number of pages or enough candidate videos are collected

## Navigation landmarks

- Search textbox containing the keyword
- Category tabs like `视频`, `直播`, `专栏`, `用户`
- Sort buttons such as `综合排序`, `最多播放`, `最新发布`
- Result cards with video title, uploader, date, play count, and duration
- Pagination controls including `下一页`

## Safe workflow

1. Open the search URL and confirm the keyword remains in the search box.
2. Record the visible category counts and the active sort mode.
3. Extract visible result cards one by one.
4. If the user requests a different ranking, click one sort button, re-snapshot, and verify the result list changed.
5. Use `下一页` only when more results are needed, then re-snapshot and confirm the page changed.

## Verification checklist

- Keyword visible in the search box
- At least one category count captured
- At least three result cards extracted with title and URL
- Sort mode or page change verified when used

## Example result note

- Completed/blocked: completed
- Evidence: keyword `AI` remained visible, categories showed counts such as `视频 99+` and `直播 32`, and visible results included titles like `从 LLM 到 Agent Skill，一期视频带你打通底层逻辑！` and `OpenClaw到底是什么？一只龙虾如何搅动整个AI圈！`
- Follow-up: open a specific BV page when detailed video inspection is needed
