# Chinese Demand Platform Matrix

This matrix focuses on high-demand Chinese platforms and records what was actually observed in the current environment.

| Platform | Tested path | Current status | Notes |
|---|---|---|---|
| 小红书 | browser + local xiaohongshu MCP | Partial | Browser direct access is risk-controlled, but a local MCP binary service was installed, connected, and tested up to `未登录`; remaining blocker is account login state |
| 微信公众号 | `miku_ai` search + local article reader | Working | Search returned article URLs; reader exported markdown and images successfully |
| 知识星球 / ZSXQ | authenticated browser + original-image workflow | Working in authenticated session | Browser was already logged in; topic scanning and original image resolution succeeded |

## Rule of thumb

- For WeChat articles, prefer the local article reader over raw browser scraping.
- For ZSXQ, prefer authenticated browser extraction and original image resolution via preview overlay.
- For XiaoHongShu, do not promise direct use until the MCP service and login state are configured.
