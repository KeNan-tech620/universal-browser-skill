# Site Recipe: Douyin Public Video Inspection

## Site

- Name: Douyin Video Page
- Entry URL: https://www.douyin.com/video/7616007470403029753
- Workspace or account: mostly public video view, signed-out state
- Auth required: no for basic video and some comment reading; yes for commenting and deeper account actions
- Human approval points: login, follow, like, comment, or account-specific actions

## Task

- Goal: inspect a public Douyin video page and extract visible metadata, chapter summary, creator info, and visible comments
- Inputs:
  - target Douyin video URL
- Expected output:
  - video title
  - creator name and high-level profile stats when visible
  - visible engagement numbers
  - publish time when visible
  - summary/chapters and sample visible comments
- Stop rule: stop after the target video identity and visible metadata are confirmed

## Navigation landmarks

- Main video heading
- Creator block with account name and follower/like counts
- Visible engagement row with likes/comments/collections/shares
- Publish time line
- AI-generated summary or chapter points when present
- Comments section with visible login boundary for deeper interaction

## Safe workflow

1. Open the direct video URL and verify the page is a video detail page, not a generic redirect.
2. Extract the main title and creator block.
3. Record visible engagement numbers and publish time.
4. If an AI-generated summary or chapter list is present, capture it as supporting structure.
5. Read only visible comments; do not assume full comment access if the page asks the user to log in for more.

## Verification checklist

- Target video title visible
- Creator name visible
- At least one engagement metric captured
- Publish time captured when shown
- Comment/login boundary captured when present

## Example result note

- Completed/blocked: completed
- Evidence: the page showed the title `第25集 | 「赚钱」这件事不存在失败，要么成功，要么学到东西`, creator `百万钱叔`, visible stats like `26.7K`, `728`, `14.7K`, `7087`, publish time `2026-03-12 01:38`, an AI-generated chapter summary, and a visible prompt `登录后可查看更多评论`
- Follow-up: log in only if interactive actions or deeper comment traversal are required
