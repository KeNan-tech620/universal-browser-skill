# Site Note: X Public Access Boundary and Fallbacks

Use this note when a task mentions X but the environment may not have a valid X login.

## What was tested in this environment

The following checks were run on the server/browser environment used for this skill:

1. `web_fetch https://x.com/github`
2. `web_fetch https://x.com/search?q=browser%20automation&src=typed_query`
3. `xreach tweet <tweet-url> --json`
4. `xreach auth check`
5. `xreach auth browsers`
6. `xreach auth extract --browser chrome`
7. Browser open to `https://x.com/i/flow/login`

## Observed results

### Signed-out web fetch

Both public profile and search URLs returned:

- `Something went wrong, but don’t fret — let’s give it another shot.`

This means unauthenticated HTML fetch is not reliable enough to treat as a real extraction path here.

### xreach CLI

`xreach tweet` failed with:

- `Not authenticated.`

`xreach auth check` also reported:

- `Not authenticated`

### Browser extraction support

`xreach auth browsers` reported:

- `No supported browsers found`

`xreach auth extract --browser chrome` failed because the Chrome cookie file was missing.

### Browser login page

Opening the X login flow in the browser produced a dialog that said:

- `Something went wrong. Try reloading.`

## Practical rule

For this environment, treat X as:

- **blocked without auth** for reliable browser or CLI extraction
- **usable only after auth is restored** through a valid browser profile or manual cookies

## What to do when a user asks for X work

### If auth is available

Use `references/x-authenticated-search.md`.

### If auth is not available

Be explicit:

- state that X search and tweet extraction are blocked by missing auth in the current environment
- do not claim that signed-out scraping is stable
- ask for or prepare one of these auth paths:
  - attached browser already logged into X
  - `xreach auth set --auth-token <token> --ct0 <token>`
  - browser-cookie extraction from a supported profile when available

## Fallbacks when the user still wants progress

These are weaker than direct X access and should be described as fallbacks, not equivalents:

- Search-engine discovery of public X links
- User-provided tweet/profile URLs for later inspection after auth is restored
- Alternative public sources discussing the same topic

## Reporting language

Preferred wording:

- `X real-time search is blocked in the current environment because no authenticated X session is available.`
- `I can continue after restoring X auth, or I can use a weaker fallback such as search-engine discovery of public X links.`
