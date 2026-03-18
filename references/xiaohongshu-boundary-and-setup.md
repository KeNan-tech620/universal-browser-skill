# Site Note: XiaoHongShu Boundary and Setup

## What was tested in this environment

### Browser path

A browser request to:

- `https://www.xiaohongshu.com/explore`

returned a risk-control page with:

- `安全限制`
- `IP at risk. Switch to a secure network and retry.`
- code `300012`

### MCP path

`agent-reach doctor` reported:

- `小红书笔记 — mcporter 已装但小红书 MCP 未配置`

Suggested setup from the doctor output:

```bash
docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp
mcporter config add xiaohongshu http://localhost:18060/mcp
```

### Local environment check

- `mcporter` exists
- configured MCP servers currently include `exa`, `douyin`, and `weibo`
- `xiaohongshu` is **not configured**
- `docker` is **not installed** on this server right now

## Practical rule

For the current server environment, treat XiaoHongShu as:

- **blocked in direct browser mode** due to IP risk control
- **not ready in MCP mode** because the `xiaohongshu` MCP server is not configured

## What to do when a user asks for XiaoHongShu work

### If the goal is immediate browsing from this server

Be explicit that direct public access is currently blocked.

### If the goal is to make XiaoHongShu work properly

Required recovery steps:

1. Provide a reachable XiaoHongShu MCP service
2. Configure it into `mcporter`
3. Import/login cookies as needed
4. Re-test search and note-detail flows

## Recovery options

### Option A: local MCP server

When Docker is available:

```bash
docker run -d --name xiaohongshu-mcp -p 18060:18060 xpzouying/xiaohongshu-mcp
mcporter config add xiaohongshu http://localhost:18060/mcp
```

### Option B: existing remote MCP service

If the user already has a remote XiaoHongShu MCP endpoint, add it directly:

```bash
mcporter config add xiaohongshu https://HOST_OR_IP:PORT/mcp
```

Then complete cookie/login setup inside that MCP service.

## Reporting language

Preferred wording:

- `小红书在当前服务器环境里被风控拦住了，浏览器直开会出现 IP at risk。`
- `同时 mcporter 里还没有配置 xiaohongshu MCP，所以这条链路现在也没法直接跑。`
- `要恢复可用，需要先把小红书 MCP 服务配起来，再导入登录态。`
