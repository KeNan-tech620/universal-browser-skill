# Content Platform Matrix

This matrix summarizes what was actually observed in the current environment.

| Platform | Tested path | Current status | Notes |
|---|---|---|---|
| X / Twitter | x.com profile/search, xreach CLI | Blocked without auth | Signed-out page fetch unreliable; xreach not authenticated; browser-cookie extraction unavailable in current server env |
| Reddit | old.reddit.com subreddit page | Blocked in signed-out browser mode | Returned `whoa there, pardner!` network-policy block |
| YouTube | public watch page + yt-dlp | Partial | Browser shows visible metadata, but bot-check prompt appears; yt-dlp requires cookies |
| Hacker News | news.ycombinator.com | Publicly accessible | Front page and discussion metadata readable without login |
| Bilibili | search.bilibili.com/all | Publicly accessible for search | Search results, counts, sort buttons, and video cards visible |
| Douyin | direct video page | Publicly accessible for detail reading | Video title, creator block, stats, AI summary, and some comments visible; deeper interaction needs login |

## Rule of thumb

- Use full recipe files for platforms marked publicly accessible or partially accessible.
- Use boundary notes when auth, bot checks, or network policy blocks reliable access.
- Do not upgrade a partial or blocked path into a promised stable workflow.
