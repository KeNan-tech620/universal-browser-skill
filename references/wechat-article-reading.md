# Site Recipe: WeChat Article Search and Reading

## Site

- Name: WeChat Official Accounts / 公众号文章
- Search path: `miku_ai.get_wexin_article(...)`
- Read path: `~/.agent-reach/tools/wechat-article-for-ai/main.py`
- Workspace or account: no WeChat login was needed for the tested article reader path
- Auth required: not for the tested read path; anti-bot handling is delegated to the local reader tool
- Human approval points: none for the tested article

## What was tested

### Search

A Python search using `miku_ai.get_wexin_article('AI 智能体', 3)` returned candidate public article URLs.

### Reading

The local reader was run against one result URL:

```bash
cd ~/.agent-reach/tools/wechat-article-for-ai
python3 main.py "<mp.weixin article url>"
```

Observed result:

- article processed successfully
- title captured
- author captured
- markdown file saved
- 5 images downloaded successfully

## Verified output from this environment

- Title: `普通人如何用AI工具变现？新一批AI智能体培训开班啦，小白可学！`
- Author: `长安潮生活`
- Output markdown path:
  - `~/.agent-reach/tools/wechat-article-for-ai/output/普通人如何用AI工具变现？新一批AI智能体培训开班啦，小白可学！/普通人如何用AI工具变现？新一批AI智能体培训开班啦，小白可学！.md`
- Downloaded images:
  - `images/img_001.jpg` through `images/img_005.png`

## Safe workflow

1. Search candidate article URLs with `miku_ai.get_wexin_article(...)` when the user gives a topic instead of a URL.
2. Run the local reader on the chosen `mp.weixin.qq.com` article URL.
3. Verify the reader output contains title, author, markdown content, and downloaded images.
4. Use the saved markdown and images as the extraction result instead of relying on raw browser scraping.

## Verification checklist

- Search returned candidate URLs
- Reader completed without fatal error
- Markdown output file exists
- At least one image file exists when the article contains images
- Title and author are visible in the exported markdown

## Example result note

- Completed/blocked: completed
- Evidence: the reader exported markdown and 5 images for `普通人如何用AI工具变现？新一批AI智能体培训开班啦，小白可学！`, with author `长安潮生活`
- Follow-up: if a specific article URL is already known, skip search and run the reader directly
