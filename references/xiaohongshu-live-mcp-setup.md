# Site Recipe: XiaoHongShu MCP Live Setup

## Goal

Bring XiaoHongShu support from `not configured` to `service installed + MCP connected + login pending/completed`.

## What was actually achieved in this environment

### 1. Found a non-Docker path

The upstream project `xpzouying/xiaohongshu-mcp` provides Linux prebuilt binaries.

Verified release asset:

- `xiaohongshu-mcp-linux-amd64.tar.gz`

This means XiaoHongShu support does **not** strictly depend on Docker.

### 2. Installed the MCP service locally

Binaries were placed under:

- `~/.agent-reach/tools/xiaohongshu-mcp/`

Installed files:

- `xiaohongshu-mcp-linux-amd64`
- `xiaohongshu-login-linux-amd64`

### 3. Started the MCP server successfully

The server started and logged:

- `Registered 13 MCP tools`
- `启动 HTTP 服务器: :18060`

### 4. Connected mcporter successfully

The server was added to mcporter as:

- `xiaohongshu -> http://localhost:18060/mcp`

Schema listing succeeded and exposed tools such as:

- `check_login_status`
- `get_login_qrcode`
- `get_feed_detail`
- `favorite_feed`
- `like_feed`

### 5. Confirmed the current blocker

Calling `check_login_status` returned:

- `未登录`

This means the installation and MCP wiring are already working. The remaining blocker is **account login state**.

## Current status in plain words

XiaoHongShu is now in this state:

- ✅ binary MCP service installed
- ✅ local HTTP MCP service running
- ✅ mcporter connected
- ✅ tool list available
- ❌ XiaoHongShu account not logged in yet

That is a much more advanced state than `not configured`.

## Safe workflow

1. Ensure the local MCP service is running on `http://localhost:18060/mcp`.
2. Verify the MCP link with:
   - `mcporter list xiaohongshu --schema --json`
3. Check auth with:
   - `mcporter call xiaohongshu.check_login_status`
4. If not logged in, complete login by QR/cookies using the XiaoHongShu account owner.
5. Re-check login status.
6. Only after login succeeds, test search/detail tools.

## Operational notes

- Direct browser browsing of `xiaohongshu.com` from this server still hits risk control.
- MCP installation is no longer the bottleneck.
- The real remaining bottleneck is authenticated session establishment.

## Verification checklist

- MCP server process is running
- mcporter can list the XiaoHongShu tool schema
- `check_login_status` executes successfully
- login state is clearly reported as logged in or not logged in

## Example result note

- Completed/blocked: partially completed
- Evidence: local `xiaohongshu-mcp` binary service started, `mcporter` listed 13 tools, `check_login_status` returned `未登录`
- Follow-up: complete QR or cookie login to unlock real search and note-detail calls
