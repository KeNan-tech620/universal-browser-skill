# Site Recipe: ZSXQ Authenticated Reading and Original Image Extraction

## Site

- Name: 知识星球 / ZSXQ
- Entry URL: `https://wx.zsxq.com/login` or a specific group URL
- Workspace or account: authenticated browser session
- Auth required: yes
- Human approval points: QR login when the browser session is not already authenticated

## What was tested in this environment

### Login state

Opening `https://wx.zsxq.com/login` did **not** land on a QR login wall. It opened directly into an authenticated session with visible groups, search, tags, and topic feed.

### Topic and image detection

A browser evaluate pass over the first 8 `app-topic` nodes succeeded.

Observed result:

- topic IDs assigned successfully
- image IDs assigned for posts that contained images
- multiple posts reported `imageCount > 0`

### Original image resolution

A live browser evaluation against `capture-topic-5-img-1` succeeded and returned:

- an `images.zsxq.com` URL with `quality/100!`
- dimensions `1245x717`

The resolved URL was then downloaded locally and verified as a real JPEG file.

## Safe workflow

1. Open the ZSXQ target page in an authenticated browser tab.
2. If the session is not authenticated, show the login QR and wait for the user.
3. Use browser evaluation to assign stable IDs to the first N `app-topic` nodes and their candidate image elements.
4. Resolve original images by clicking the preview overlay and reading the full-screen image URL, preferring URLs with `quality/100!` and large `naturalWidth`.
5. Download resolved original image URLs locally when needed.
6. Report the post metadata and image output paths.

## Verified browser pattern

The following pattern worked in the current environment:

- `document.querySelectorAll('app-topic')`
- filter visible `img` elements with width/height >= 80
- preview overlay selector:
  - `.image-full-screen-container img.image.can-scale`

## Verification checklist

- Authenticated session confirmed
- Topic IDs assigned successfully
- At least one post with image IDs found
- Original image URL resolved from preview overlay
- Downloaded file verified locally

## Example result note

- Completed/blocked: completed
- Evidence: topic scan found posts with image IDs such as `capture-topic-5-img-1`; original image resolution returned an `images.zsxq.com` URL with `quality/100!`; downloaded file `/tmp/zsxq_test_original.jpg` was verified as a JPEG with dimensions `1245x717`
- Follow-up: for full export tasks, pair this workflow with the dedicated local `zsxq-original-images` skill when available
