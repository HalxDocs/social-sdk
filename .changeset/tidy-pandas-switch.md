---
"@opencoredev/social-sdk": minor
---

Add X video and GIF chunked upload to the direct adapter. MP4 video (up to 512 MiB) and GIF (up to 15 MiB) Blobs upload via 1 MiB INIT/APPEND/FINALIZE segments with a bounded STATUS poll honoring `check_after_secs`. Chunk rejections (413), failed processing, and over-duration attach errors surface as terminal `media_error`; timeouts stay explicit for reconciliation. `posts.publish` accepts a single video or GIF per post and advertises the `video` format.
