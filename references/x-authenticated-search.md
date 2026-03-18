# Site Recipe: X Authenticated Search and Tweet Inspection

## Site

- Name: X / Twitter
- Entry URL: https://x.com/search?q=browser%20automation&src=typed_query
- Workspace or account: authenticated X session
- Auth required: yes
- Human approval points: login, 2FA, CAPTCHA, suspicious-login prompts

## Task

- Goal: search X posts, open target tweets or profiles, and extract structured results
- Inputs:
  - search query
  - optional author handle
  - optional result type or timeframe if the UI exposes them
  - optional target tweet URL for direct inspection
- Expected output:
  - query used
  - visible result set or target tweet fields
  - tweet URLs, author handles, timestamps, and visible engagement metrics when shown
- Stop rule: stop after the requested number of tweets are verified or the requested target tweet/profile has been inspected

## Navigation landmarks

- Search page or query string under `https://x.com/search`
- Tweet cards containing author handle, timestamp, text, and action counts
- Profile page with handle and timeline
- Direct tweet page with the target tweet expanded

## Safe workflow

1. Verify an authenticated X session exists before starting. Prefer a user-approved browser session or valid `xreach` auth cookies.
2. If using browser automation, open the target search or tweet URL and confirm the page is not blocked by a login wall or generic error screen.
3. If using `xreach`, validate auth first with `xreach auth check`.
4. Run one search or open one target tweet at a time.
5. Re-snapshot after filter changes, timeline switches, or opening a tweet thread.
6. Extract only visible, attributable fields: handle, tweet text, timestamp, URL, and visible counts.
7. If the session expires or X returns a generic error, stop and re-establish auth before continuing.

## Auth setup options

### Browser-session path

- Use an attached browser profile that is already logged into X
- Expect human help for login, 2FA, CAPTCHA, or device approval

### xreach CLI path

- Check auth: `xreach auth check`
- List browser extraction support: `xreach auth browsers`
- Try browser extraction: `xreach auth extract --browser chrome`
- Manual cookies fallback: `xreach auth set --auth-token <token> --ct0 <token>`

## Recovery notes

- If signed-out browser pages show `Something went wrong` or a login wall, treat the flow as blocked until auth is restored.
- If `xreach auth browsers` reports no supported browsers, browser-cookie extraction is unavailable in the current environment.
- If `xreach auth extract --browser chrome` fails because the cookie file is missing, use a supported browser profile or set cookies manually.
- If search is blocked but a direct tweet URL is available, try direct tweet inspection after auth is restored.

## Verification checklist

- Auth state verified before search
- Query or target tweet URL recorded
- At least one tweet card or target tweet visibly confirmed
- Extracted data tied to visible UI state, not guesses
- Session/blocker state reported when auth is missing

## Example result note

- Completed/blocked: blocked without auth in the current server environment
- Evidence: `xreach auth check` returned `Not authenticated`; `xreach auth browsers` returned `No supported browsers found`; `xreach auth extract --browser chrome` failed with missing cookie file
- Follow-up: restore X auth via a supported browser profile or manual `auth_token` + `ct0` cookies, then rerun the search or tweet inspection flow
