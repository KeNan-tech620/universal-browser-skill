# Site Recipe: YouTube Public Watch Page with Bot-Check Boundary

## Site

- Name: YouTube
- Entry URL: https://www.youtube.com/watch?v=aqz-KE-bpKQ
- Workspace or account: signed-out view
- Auth required: not always for page metadata, but often required for stable extraction and external tooling
- Human approval points: Google sign-in, bot-check, CAPTCHA, account verification

## What was tested

### Browser page

A signed-out browser load of a public watch page showed:

- video title
- channel name and subscriber count
- view count and age
- share/save buttons
- related video list
- a visible prompt: `Sign in to confirm you’re not a bot`

### External fetcher

`yt-dlp --dump-json` failed with:

- `Sign in to confirm you’re not a bot`

## Practical rule

For this environment, treat YouTube as:

- **partially readable without login** for visible page metadata in the browser
- **not reliably extractable without cookies** for full automated metadata/subtitle fetch via command-line tooling

## Safe workflow

1. Open the public watch page in the browser.
2. Extract only what is visibly confirmed on the page: title, channel, visible subscribers, views, age, description snippet, and related videos.
3. If subtitles, deeper metadata, or reliable automation are required, restore auth/cookies first.
4. Report the bot-check prompt when present instead of pretending extraction is complete.

## Verification checklist

- Title visible
- Channel visible
- View count and age visible
- Bot-check prompt state recorded when present

## Example result note

- Completed/blocked: partially completed
- Evidence: browser showed the title `Big Buck Bunny 60fps 4K - Official Blender Foundation Short Film`, channel `Blender`, `1.22M subscribers`, `23M views`, and a `Sign in to confirm you’re not a bot` prompt
- Follow-up: use a logged-in browser or cookies if subtitle or full metadata extraction is required
