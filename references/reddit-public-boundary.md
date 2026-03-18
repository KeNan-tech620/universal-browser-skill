# Site Note: Reddit Public Access Boundary

## What was tested

A signed-out browser request was made to:

- `https://old.reddit.com/r/artificial/`

## Observed result

The page returned a block screen with:

- heading `whoa there, pardner!`
- message `Your request has been blocked due to a network policy.`

It also suggested logging in or using developer credentials.

## Practical rule for this environment

Treat Reddit as:

- **blocked in signed-out browser mode** from this server/network
- potentially usable only after auth or via an alternate sanctioned access path

## What to do when a user asks for Reddit work

### If direct browser access is required

- be explicit that public Reddit browsing is blocked in the current environment
- do not claim normal signed-out access is stable

### Possible recovery paths

- logged-in browser session approved by the user
- an allowed API or alternate fetch path outside this browser-only workflow
- search-engine discovery of Reddit links as a weaker fallback

## Reporting language

Preferred wording:

- `Reddit public browsing is blocked by a network policy in the current environment.`
- `I can continue with a logged-in browser session or use a weaker fallback such as search-engine discovery of Reddit links.`
