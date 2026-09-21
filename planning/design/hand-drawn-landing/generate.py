#!/usr/bin/env python3
"""Generate the per-platform SEO pages and sitemap.xml for the hand-drawn landing prototype.

Run from this directory: python3 generate.py
Facts come from apps/docs/docs/platforms/*.mdx. Keep them honest when editing.
"""

import html
import pathlib
import re

BASE_URL = "https://social-sdk.example"  # placeholder until the real domain exists

LOGOS = {
    "bluesky": '<path fill="#1185fe" d="M5.202 2.857C7.954 4.922 10.913 9.11 12 11.358c1.087-2.247 4.046-6.436 6.798-8.501C20.783 1.366 24 .213 24 3.883c0 .732-.42 6.156-.667 7.037-.856 3.061-3.978 3.842-6.755 3.37 4.854.826 6.089 3.562 3.422 6.299-5.065 5.196-7.28-1.304-7.847-2.97-.104-.305-.152-.448-.153-.327 0-.121-.05.022-.153.327-.568 1.666-2.782 8.166-7.847 2.97-2.667-2.737-1.432-5.473 3.422-6.3-2.777.473-5.899-.308-6.755-3.369C.42 10.04 0 4.615 0 3.883c0-3.67 3.217-2.517 5.202-1.026"/>',
    "x": '<path fill="#111111" d="M14.234 10.162 22.977 0h-2.072l-7.591 8.824L7.251 0H.258l9.168 13.343L.258 24H2.33l8.016-9.318L16.749 24h6.993zm-2.837 3.299-.929-1.329L3.076 1.56h3.182l5.965 8.532.929 1.329 7.754 11.09h-3.182z"/>',
    "threads": '<path fill="#111111" d="M18.263 11.097c-.03-3.486-1.92-5.586-5.111-5.586-2.13 0-3.922.963-4.863 2.499l2.062 1.438c.535-.843 1.272-1.543 2.628-1.543 1.528 0 2.318.85 2.544 2.431a15 15 0 0 0-2.236-.173c-4.125 0-6.068 1.867-6.068 4.336s1.943 3.99 4.804 3.99c3.139 0 5.013-2.115 5.781-4.735.798.361 1.348 1.204 1.348 2.47 0 3.387-3.907 5.232-7.22 5.232-4.885 0-8.077-3.207-8.077-8.424 0-6.392 4.223-10.487 9.9-10.487 3.808 0 5.69 1.671 6.97 3.914l2.108-1.475C21.44 2.078 18.331 0 13.663 0 6.227 0 1.168 5.277 1.168 12.934c0 7 4.953 11.066 10.856 11.066 4.878 0 9.809-2.846 9.809-7.716 0-2.545-1.46-4.231-3.569-5.187m-6.33 4.855c-1.077 0-2.026-.512-2.026-1.453 0-1.483 1.822-1.934 3.606-1.934.678 0 1.34.045 1.927.173-.422 1.927-1.671 3.215-3.508 3.214Z"/>',
    "youtube": '<path fill="#ff0033" d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/>',
    "tiktok": '<path fill="#111111" d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/>',
    "instagram": '<path fill="#e4405f" d="M7.0301.084c-1.2768.0602-2.1487.264-2.911.5634-.7888.3075-1.4575.72-2.1228 1.3877-.6652.6677-1.075 1.3368-1.3802 2.127-.2954.7638-.4956 1.6365-.552 2.914-.0564 1.2775-.0689 1.6882-.0626 4.947.0062 3.2586.0206 3.6671.0825 4.9473.061 1.2765.264 2.1482.5635 2.9107.308.7889.72 1.4573 1.388 2.1228.6679.6655 1.3365 1.0743 2.1285 1.38.7632.295 1.6361.4961 2.9134.552 1.2773.056 1.6884.069 4.9462.0627 3.2578-.0062 3.668-.0207 4.9478-.0814 1.28-.0607 2.147-.2652 2.9098-.5633.7889-.3086 1.4578-.72 2.1228-1.3881.665-.6682 1.0745-1.3378 1.3795-2.1284.2957-.7632.4966-1.636.552-2.9124.056-1.2809.0692-1.6898.063-4.948-.0063-3.2583-.021-3.6668-.0817-4.9465-.0607-1.2797-.264-2.1487-.5633-2.9117-.3084-.7889-.72-1.4568-1.3876-2.1228C21.2982 1.33 20.628.9208 19.8378.6165 19.074.321 18.2017.1197 16.9244.0645 15.6471.0093 15.236-.005 11.977.0014 8.718.0076 8.31.0215 7.0301.0839m.1402 21.6932c-1.17-.0509-1.8053-.2453-2.2287-.408-.5606-.216-.96-.4771-1.3819-.895-.422-.4178-.6811-.8186-.9-1.378-.1644-.4234-.3624-1.058-.4171-2.228-.0595-1.2645-.072-1.6442-.079-4.848-.007-3.2037.0053-3.583.0607-4.848.05-1.169.2456-1.805.408-2.2282.216-.5613.4762-.96.895-1.3816.4188-.4217.8184-.6814 1.3783-.9003.423-.1651 1.0575-.3614 2.227-.4171 1.2655-.06 1.6447-.072 4.848-.079 3.2033-.007 3.5835.005 4.8495.0608 1.169.0508 1.8053.2445 2.228.408.5608.216.96.4754 1.3816.895.4217.4194.6816.8176.9005 1.3787.1653.4217.3617 1.056.4169 2.2263.0602 1.2655.0739 1.645.0796 4.848.0058 3.203-.0055 3.5834-.061 4.848-.051 1.17-.245 1.8055-.408 2.2294-.216.5604-.4763.96-.8954 1.3814-.419.4215-.8181.6811-1.3783.9-.4224.1649-1.0577.3617-2.2262.4174-1.2656.0595-1.6448.072-4.8493.079-3.2045.007-3.5825-.006-4.848-.0608M16.953 5.5864A1.44 1.44 0 1 0 18.39 4.144a1.44 1.44 0 0 0-1.437 1.4424M5.8385 12.012c.0067 3.4032 2.7706 6.1557 6.173 6.1493 3.4026-.0065 6.157-2.7701 6.1506-6.1733-.0065-3.4032-2.771-6.1565-6.174-6.1498-3.403.0067-6.156 2.771-6.1496 6.1738M8 12.0077a4 4 0 1 1 4.008 3.9921A3.9996 3.9996 0 0 1 8 12.0077"/>',
    "linkedin": '<rect width="24" height="24" rx="4" fill="#0A66C2"/><path fill="#fff" d="M6.2 8.1H3.5V20h2.7V8.1ZM4.85 4A1.65 1.65 0 1 0 4.85 7.3 1.65 1.65 0 0 0 4.85 4ZM20.5 13.17c0-3.58-1.91-5.25-4.46-5.25-2.06 0-2.98 1.13-3.49 1.92V8.1H9.84V20h2.71v-5.89c0-1.55.29-3.05 2.21-3.05 1.9 0 1.92 1.78 1.92 3.15V20h2.72l1.1-6.83Z"/>',
}

PLATFORMS = [
    {
        "slug": "bluesky",
        "name": "Bluesky",
        "title": "Bluesky API for TypeScript | Social SDK",
        "desc": "Publish text and image posts to Bluesky from a TypeScript server: session-based auth, native AT URIs, replies, metrics, and honest per-post outcomes.",
        "h1": "Post to Bluesky from your server.",
        "sub": "Bring an existing session from the official AT Protocol OAuth client. The adapter handles records, facets, and image limits.",
        "quip": "records, facets, and CIDs, handled",
        "status": ("posted &#10003;", "#2f6f4f"),
        "caps": [
            ("ok", "text posts, with Bluesky's grapheme-aware length rules"),
            ("ok", "images and video upload, with provider processing states"),
            ("ok", "replies, reposts, quote posts, and deletion"),
            ("ok", "follows, blocks, mutes, and notification reads"),
            ("ok", "chat conversations and messages"),
            ("ok", "post and account metrics, likes included"),
        ],
        "code": """import { createSocial, connectedAccountRef } from "@opencoredev/social-sdk";
import { bluesky } from "@opencoredev/social-sdk/bluesky";

const social = createSocial({
  backend: bluesky({ auth: { service, did, accessJwt } }),
});

const result = await social.posts.publish({
  targets: [{ account }],
  content: { text: "A Bluesky post" },
});
// success returns the record's AT URI and CID""",
    },
    {
        "slug": "x",
        "name": "X",
        "title": "X API for TypeScript | Social SDK",
        "desc": "Publish to X from TypeScript with weighted 280-character rules, image uploads, replies, lifetime metrics, and reconciliation for uncertain writes.",
        "h1": "Publish to X without guessing.",
        "sub": "An existing bearer token and user ID. No tweet ID back means the outcome stays unknown until you reconcile, not a fake success.",
        "quip": "280 weighted characters, counted the way X counts",
        "status": ("posted &#10003;", "#2f6f4f"),
        "caps": [
            ("ok", "text posts under X's weighted 280-character rules"),
            ("ok", "images, video, and GIF uploads with async processing states"),
            ("ok", "polls, replies, reposts, quotes, and deletion"),
            ("ok", "bookmarks and follows"),
            ("ok", "native reads, lifetime metrics, and likes"),
            ("gated", "DM reads and filtered streams, on the matching X API tier"),
        ],
        "code": """import { createSocial, connectedAccountRef } from "@opencoredev/social-sdk";
import { x } from "@opencoredev/social-sdk/x";

const social = createSocial({
  backend: x({ auth: { userId, accessToken } }),
});

const result = await social.posts.publish({
  targets: [{ account }],
  content: { text: "A server-side update" },
});
// no tweet ID returned? outcome is "unknown": reconcile, don't re-post""",
    },
    {
        "slug": "threads",
        "name": "Threads",
        "title": "Threads API for TypeScript | Social SDK",
        "desc": "Publish Threads text, media, and carousels from TypeScript. Container-based publishing with processing outcomes preserved for explicit reconciliation.",
        "h1": "Threads posts, carousels included.",
        "sub": "A user token and Threads user ID. Publishing has two phases, and the SDK tells you which one you're in.",
        "quip": "ten children, one parent, one carousel",
        "status": ("processing&#8230;", "#57534c"),
        "caps": [
            ("ok", "text, one HTTPS image or video, and ten-item carousels"),
            ("ok", "replies, quote posts, and reposts"),
            ("ok", "keyword search and mention reads"),
            ("ok", "post deletion"),
            ("ok", "reads and lifetime metrics"),
            ("no", "DMs: Threads offers no messaging API"),
        ],
        "code": """import { createSocial, connectedAccountRef } from "@opencoredev/social-sdk";
import { threads } from "@opencoredev/social-sdk/threads";

const social = createSocial({
  backend: threads({ auth: { userId, accessToken } }),
});

const result = await social.posts.publish({
  targets: [{ account }],
  content: { text: "Hello Threads" },
});
// container created but no post ID yet? outcome is "processing\"""",
    },
    {
        "slug": "youtube",
        "name": "YouTube",
        "title": "YouTube upload API for TypeScript | Social SDK",
        "desc": "Upload videos to YouTube from TypeScript with resumable sessions, explicit visibility and audience flags, and processing states mapped honestly.",
        "h1": "Upload to YouTube and know when it's live.",
        "sub": "OAuth token and channel ID in, resumable upload out. \"uploaded\" maps to processing. \"processed\" maps to published. Nothing is rounded up.",
        "quip": "crash mid-upload? resume the session",
        "status": ("upload processing&#8230;", "#57534c"),
        "caps": [
            ("ok", "video upload with resumable, persistable sessions"),
            ("ok", "publish scheduling, thumbnails, and captions"),
            ("ok", "playlists, video updates, and deletion"),
            ("ok", "reads, lifetime stats, and Analytics API reports"),
            ("ok", "comment listing and replies"),
            ("gated", "live broadcasts, behind channel eligibility"),
        ],
        "code": """import { createSocial, connectedAccountRef } from "@opencoredev/social-sdk";
import { youtube } from "@opencoredev/social-sdk/youtube";

const social = createSocial({
  backend: youtube({ auth: { accessToken, channelId } }),
});

const result = await social.posts.publish({
  targets: [{
    account,
    options: { title: "A release", visibility: "private", madeForKids: false },
  }],
  content: { text: "Description", media: [video] },
});
// watch URL appears only once YouTube returns a verified video ID""",
    },
    {
        "slug": "tiktok",
        "name": "TikTok",
        "title": "TikTok API for TypeScript | Social SDK",
        "desc": "Publish TikTok video and photo posts from TypeScript with the creator consent flow, verified media origins, and explicit processing checks.",
        "h1": "TikTok publishing, consent included.",
        "sub": "The creator sees their real privacy options before anything posts. The adapter refuses to publish without that consent.",
        "quip": "the creator picks the privacy level, not you",
        "status": ("queued", "#57534c"),
        "caps": [
            ("ok", "direct posts and the inbox draft path"),
            ("ok", "one video or up to 35 photos, with cover choice"),
            ("ok", "creator preview: privacy levels from the creator's account"),
            ("ok", "own-video listing and explicit publish-status checks"),
            ("ok", "account metrics"),
            ("no", "comments and DMs: TikTok's APIs don't offer them"),
        ],
        "code": """import { createSocial, connectedAccountRef } from "@opencoredev/social-sdk";
import { tiktok } from "@opencoredev/social-sdk/tiktok";

const social = createSocial({
  backend: tiktok({ auth: { accessToken, openId }, verifiedMediaOrigins }),
});

const result = await social.posts.publish({
  targets: [{ account, options: { consentGiven: true, creatorInfo, privacy } }],
  content: { text: "A creator-approved caption", media: [video] },
});
// no consent, no creator info? preparation fails before any request""",
    },
    {
        "slug": "instagram",
        "name": "Instagram",
        "title": "Instagram API for TypeScript | Social SDK",
        "desc": "Publish images, video, and carousels to Instagram professional accounts from TypeScript, with container processing, comments, and Insights metrics.",
        "h1": "Instagram publishing for professional accounts.",
        "sub": "Public HTTPS media goes into containers, containers get published, and every processing state comes back to you unchanged.",
        "quip": "containers first, publish second",
        "status": ("processing&#8230;", "#57534c"),
        "caps": [
            ("ok", "images, video, and carousels from public HTTPS URLs"),
            ("ok", "Reels and Stories publishing"),
            ("ok", "deletion, hashtag search, and publishing-limit reads"),
            ("ok", "tagged and mention reads"),
            ("ok", "comment reads, replies, and Insights metrics"),
            ("gated", "product tagging and messaging, behind Meta app review"),
        ],
        "code": """import { createSocial, connectedAccountRef } from "@opencoredev/social-sdk";
import { instagram } from "@opencoredev/social-sdk/instagram";

const social = createSocial({
  backend: instagram({ auth: { accessToken, accountId } }),
});

const prepared = social.posts.prepare({
  targets: [{ account }],
  content: {
    text: "A professional-account update",
    media: [{ kind: "image", source: { kind: "https-url", url } }],
  },
});
// a text-only Instagram post fails right here, before any request""",
    },
    {
        "slug": "linkedin",
        "name": "LinkedIn",
        "title": "LinkedIn API for TypeScript | Social SDK",
        "desc": "Post to LinkedIn as a member or organization from TypeScript, with registered image uploads, native URNs, comments, and social-action counts.",
        "h1": "Post to LinkedIn as a member or an org.",
        "sub": "You name the author URN and the API version. Unsupported formats fail preparation instead of being quietly changed.",
        "quip": "member or org, you say which URN",
        "status": ("posted &#10003;", "#2f6f4f"),
        "caps": [
            ("ok", "text, multi-image, video, and document posts"),
            ("ok", "polls, reactions, reshares, updates, and deletion"),
            ("ok", "comment reads and replies"),
            ("ok", "social-action counts and organization analytics"),
            ("gated", "articles, approval dependent"),
            ("no", "messaging: LinkedIn keeps it closed to standard apps"),
        ],
        "code": """import { createSocial, connectedAccountRef } from "@opencoredev/social-sdk";
import { linkedin } from "@opencoredev/social-sdk/linkedin";

const social = createSocial({
  backend: linkedin({
    auth: { accessToken, author: "urn:li:organization:123" },
    apiVersion: "202609",
  }),
});

const prepared = social.posts.prepare({
  targets: [{ account }],
  content: { text: "A short update" },
});
// the native URN comes back in the x-restli-id header, and is kept""",
    },
]


def highlight(code: str) -> str:
    out = html.escape(code, quote=False)
    out = re.sub(r"&quot;", '"', out)
    out = re.sub(r'("(?:[^"\\]|\\.)*")', r'<i class="s">\1</i>', out)
    out = re.sub(r"^(// .*)$", r'<i class="c">\1</i>', out, flags=re.M)
    out = re.sub(
        r"\b(import|from|const|await|true|false)\b(?![^<]*</i>)",
        r'<b class="k">\1</b>',
        out,
    )
    return out


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>%%TITLE%%</title>
<meta name="description" content="%%DESC%%" />
<link rel="canonical" href="%%BASE%%/%%SLUG%%/" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,380;9..144,430;9..144,560;9..144,640&family=Caveat:wght@500;600;700&display=swap" rel="stylesheet" />
<style>
  :root { --ink:#1c1a17; --ink-soft:#57534c; --marker:#e8542f; --hand:"Caveat",cursive; --serif:"Fraunces",Georgia,serif; --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace; }
  * { box-sizing:border-box; margin:0; padding:0; }
  body { background:#fff; color:var(--ink); font-family:var(--serif); font-weight:380; font-size:18px; line-height:1.6; -webkit-font-smoothing:antialiased; }
  .wrap { max-width:960px; margin:0 auto; padding:0 24px; }
  nav { display:flex; align-items:center; justify-content:space-between; padding:28px 0 0; }
  .logo { display:flex; align-items:center; gap:10px; text-decoration:none; color:var(--ink); }
  .logo b { font-weight:560; font-size:21px; white-space:nowrap; }
  .nav-links { display:flex; gap:24px; }
  .nav-links a { color:var(--ink); text-decoration:none; font-size:17px; }
  .nav-links a:hover { color:var(--marker); }
  header { padding:72px 0 8px; }
  .kicker { font-family:var(--hand); font-size:24px; color:var(--marker); transform:rotate(-1.4deg); display:inline-block; margin-bottom:14px; }
  h1 { font-weight:430; font-size:clamp(34px,5vw,56px); line-height:1.1; letter-spacing:-0.018em; max-width:20ch; }
  .sub { margin-top:20px; max-width:52ch; font-size:19px; color:var(--ink-soft); }
  .cta-row { margin-top:34px; display:flex; align-items:center; gap:26px; flex-wrap:wrap; }
  .brush-btn { position:relative; display:inline-block; text-decoration:none; padding:14px 30px; color:#fff; font-weight:560; font-size:18px; transform:rotate(-0.8deg); transition:transform .15s ease; }
  .brush-btn:hover { transform:rotate(0.6deg) scale(1.03); }
  .brush-btn svg { position:absolute; inset:-8px -12px; width:calc(100% + 24px); height:calc(100% + 16px); z-index:-1; }
  .cta-note { font-family:var(--hand); font-size:21px; color:var(--ink-soft); }
  .cta-note code { font-family:var(--mono); font-size:14px; color:var(--ink); }
  .stage { padding:26px 0 0; }
  .stage svg { width:100%; height:auto; display:block; }
  text.hand { font-family:var(--hand); }
  text.mono { font-family:var(--mono); }
  .wire { fill:none; stroke:#8a857c; stroke-width:1.8; stroke-dasharray:5 8; stroke-linecap:round; }
  .status { opacity:0; transition:opacity .4s ease, transform .4s cubic-bezier(.2,1.6,.4,1); transform:translateY(6px) scale(.9); transform-box:fill-box; transform-origin:center; }
  .status.on { opacity:1; transform:translateY(0) scale(1); }
  .ring.deliver { animation:thud .5s ease; transform-box:fill-box; transform-origin:center; }
  @keyframes thud { 0%{transform:scale(1)} 35%{transform:scale(1.08) rotate(-2deg)} 100%{transform:scale(1)} }
  .caps { padding:64px 0 0; }
  .caps h2 { font-weight:430; font-size:clamp(24px,3vw,34px); letter-spacing:-0.01em; }
  .caps ul { list-style:none; margin-top:26px; display:grid; grid-template-columns:1fr 1fr; gap:14px 40px; }
  .caps li { display:flex; gap:12px; align-items:baseline; font-size:17.5px; color:var(--ink-soft); }
  .caps li svg { flex:none; transform:translateY(3px); }
  .honesty { margin-top:30px; font-family:var(--hand); font-size:22px; color:var(--ink-soft); transform:rotate(-0.8deg); }
  .code-section { padding:64px 0 0; }
  .paper-note { position:relative; transform:rotate(0.8deg); max-width:760px; margin:0 auto; }
  .paper-note .tape { position:absolute; top:-14px; left:50%; width:110px; height:30px; transform:translateX(-50%) rotate(-2deg); background:rgba(232,84,47,.16); border-left:1px dashed rgba(232,84,47,.35); border-right:1px dashed rgba(232,84,47,.35); }
  .paper-note pre { padding:24px 26px; font-family:var(--mono); font-size:14px; line-height:1.75; background:#fff; overflow-x:auto; color:var(--ink); }
  .paper-note .note-border { position:absolute; inset:0; width:100%; height:100%; pointer-events:none; overflow:visible; }
  .paper-note .note-border rect { x:2px; y:2px; width:calc(100% - 4px); height:calc(100% - 4px); rx:4px; fill:none; stroke:var(--ink); stroke-width:2.2; filter:url(#roughen); }
  pre b.k { color:var(--marker); font-weight:400; font-style:normal; }
  pre i.s { color:#2f6f4f; font-style:normal; }
  pre i.c { color:#9b968d; font-style:normal; }
  footer { padding:80px 0 46px; }
  .rule { width:100%; height:14px; overflow:visible; }
  .foot-platforms { margin-top:24px; font-size:15px; color:var(--ink-soft); }
  .foot-platforms a { color:var(--ink-soft); text-decoration:none; margin-right:16px; }
  .foot-platforms a:hover { color:var(--ink); }
  .foot-row { margin-top:16px; display:flex; justify-content:space-between; align-items:baseline; flex-wrap:wrap; gap:14px; }
  .foot-row small { color:var(--ink-soft); font-size:15px; }
  @media (max-width:700px) { .caps ul { grid-template-columns:1fr; } }
  @media (prefers-reduced-motion:reduce) { .brush-btn { transition:none; } }
</style>
</head>
<body>
<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>
  <filter id="roughen" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="11" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
  <filter id="roughen2" x="-8%" y="-8%" width="116%" height="116%">
    <feTurbulence type="fractalNoise" baseFrequency="0.022" numOctaves="2" seed="4" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="4" xChannelSelector="R" yChannelSelector="G"/>
  </filter>
</defs></svg>

<div class="wrap">
  <nav>
    <a class="logo" href="../">
      <svg width="34" height="34" viewBox="0 0 34 34" fill="none" filter="url(#roughen)">
        <path d="M5 15 L19 8 L19 25 L5 19 Z" stroke="#1c1a17" stroke-width="2.2" stroke-linejoin="round"/>
        <path d="M5 15 L5 19" stroke="#1c1a17" stroke-width="2.2"/>
        <path d="M8 20.5 L9.5 27 L13 26" stroke="#1c1a17" stroke-width="2.2" stroke-linecap="round"/>
        <path d="M23 12 Q26 16.5 23 21" stroke="#e8542f" stroke-width="2.2" stroke-linecap="round" fill="none"/>
        <path d="M26.5 9.5 Q31 16.5 26.5 23.5" stroke="#e8542f" stroke-width="2.2" stroke-linecap="round" fill="none"/>
      </svg>
      <b>Social SDK</b>
    </a>
    <div class="nav-links">
      <a href="../">Home</a>
      <a href="/docs/platforms/%%SLUG%%">Docs</a>
    </div>
  </nav>

  <header>
    <span class="kicker">social SDK &#215; %%NAME%%</span>
    <h1>%%H1%%</h1>
    <p class="sub">%%SUB%%</p>
    <div class="cta-row">
      <a class="brush-btn" href="/docs/platforms/%%SLUG%%">
        <svg viewBox="0 0 300 72" preserveAspectRatio="none" aria-hidden="true">
          <path d="M14 22 C60 8, 240 4, 288 18 C298 34, 292 52, 270 60 C200 72, 60 70, 16 58 C4 46, 6 32, 14 22 Z" fill="#1c1a17" filter="url(#roughen2)"/>
        </svg>
        Read the %%NAME%% docs
      </a>
      <span class="cta-note">or just <code>bun add @opencoredev/social-sdk</code></span>
    </div>
  </header>

  <section class="stage" aria-label="Diagram: a post travelling from your app to %%NAME%%">
    <svg viewBox="0 0 960 300" fill="none">
      <g>
        <rect x="46" y="80" width="290" height="150" rx="6" stroke="#1c1a17" stroke-width="2.6" fill="#fff" filter="url(#roughen2)"/>
        <text class="hand" x="64" y="68" font-size="26" fill="#1c1a17">your app</text>
        <text class="mono" x="70" y="126" font-size="13.5" fill="#1c1a17"><tspan fill="#e8542f">await</tspan> social.posts.publish({</text>
        <text class="mono" x="84" y="152" font-size="13.5" fill="#1c1a17">targets: [%%SLUG%%],</text>
        <text class="mono" x="84" y="178" font-size="13.5" fill="#1c1a17">content,</text>
        <text class="mono" x="70" y="204" font-size="13.5" fill="#1c1a17">})</text>
      </g>
      <path class="wire" id="wire" d="M340 155 C460 150, 570 150, 688 152" filter="url(#roughen)"/>
      <g id="plane" opacity="0">
        <path d="M-13 -4 L13 0 L-9 8 L-5 0 Z M-9 8 L-8 13 L-4 5" stroke="#1c1a17" stroke-width="1.8" fill="#fff" stroke-linejoin="round"/>
      </g>
      <text class="hand" x="365" y="272" font-size="22" fill="#57534c" transform="rotate(-1.5 365 272)">%%QUIP%%</text>
      <g class="ring" id="ring">
        <circle cx="790" cy="152" r="60" stroke="#1c1a17" stroke-width="2.6" fill="#fff" filter="url(#roughen2)"/>
        <g transform="translate(766,128) scale(2)">%%LOGO%%</g>
        <text class="hand status" x="790" y="248" font-size="24" fill="%%STATUS_COLOR%%" text-anchor="middle">%%STATUS%%</text>
      </g>
    </svg>
  </section>

  <section class="caps">
    <h2>What works today</h2>
    <ul>
%%CAPS%%
    </ul>
    <p class="honesty">contract-tested against mocked transports. no live %%NAME%% account verified yet.</p>
  </section>

  <section class="code-section">
    <div class="paper-note">
      <span class="tape"></span>
      <svg class="note-border" aria-hidden="true"><rect/></svg>
      <pre>%%CODE%%</pre>
    </div>
  </section>

  <footer>
    <svg class="rule" viewBox="0 0 960 14" preserveAspectRatio="none">
      <path d="M4 8 Q120 3 240 8 T480 7 T720 9 T956 6" stroke="#1c1a17" stroke-width="2" fill="none" stroke-linecap="round" filter="url(#roughen)"/>
    </svg>
    <p class="foot-platforms">%%FOOT_LINKS%%</p>
    <div class="foot-row">
      <small>&#169; 2026 Social SDK. Open source. Platforms may charge for the accounts and operations you use.</small>
    </div>
  </footer>
</div>

<script>
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const plane = document.getElementById("plane");
  const wire = document.getElementById("wire");
  const ring = document.getElementById("ring");
  const status = document.querySelector(".status");
  if (reduced) { plane.remove(); status.classList.add("on"); }
  else {
    const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
    const ease = (t) => (t < 0.5 ? 2*t*t : 1 - Math.pow(-2*t + 2, 2) / 2);
    const tick = (cb) => {
      let done = false;
      const id = requestAnimationFrame((ts) => { done = true; cb(ts); });
      setTimeout(() => { if (!done) { cancelAnimationFrame(id); cb(performance.now()); } }, 40);
    };
    function fly() {
      return new Promise((doneFly) => {
        const len = wire.getTotalLength();
        const from = 6, to = len - 48, dur = 1600;
        let t0;
        function frame(now) {
          if (t0 === undefined) t0 = now;
          const t = Math.min((now - t0) / dur, 1);
          const d = from + (to - from) * ease(t);
          const p = wire.getPointAtLength(d);
          const q = wire.getPointAtLength(Math.min(d + 2, len));
          const a = Math.atan2(q.y - p.y, q.x - p.x) * 180 / Math.PI;
          plane.setAttribute("transform", `translate(${p.x} ${p.y}) rotate(${a})`);
          plane.setAttribute("opacity", t < 0.08 ? t/0.08 : t > 0.94 ? (1 - t)/0.06 : 1);
          if (t < 1) tick(frame);
          else {
            plane.setAttribute("opacity", 0);
            ring.classList.add("deliver");
            status.classList.add("on");
            setTimeout(() => ring.classList.remove("deliver"), 550);
            doneFly();
          }
        }
        tick(frame);
      });
    }
    (async () => {
      await sleep(700);
      while (true) {
        status.classList.remove("on");
        await sleep(700);
        await fly();
        await sleep(4200);
      }
    })();
  }
</script>
</body>
</html>
"""

CHECK = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" filter="url(#roughen)"><path d="M3 10 L7 14 L15 4" stroke="#2f6f4f" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/></svg>'
GATE = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" filter="url(#roughen)"><path d="M2.5 9 C4.5 5.5, 7 12.5, 9 9 C10.8 6, 13.5 11.8, 15.5 8.2" stroke="#d97706" stroke-width="2.6" stroke-linecap="round"/></svg>'
CROSS = '<svg width="18" height="18" viewBox="0 0 18 18" fill="none" filter="url(#roughen)"><path d="M4 4 L14 14 M14 4 L4 14" stroke="#e8542f" stroke-width="2.6" stroke-linecap="round"/></svg>'

ROOT = pathlib.Path(__file__).resolve().parent


def build() -> None:
    for p in PLATFORMS:
        icons = {"ok": CHECK, "gated": GATE, "no": CROSS}
        caps = "\n".join(
            f'      <li>{icons[kind]} <span>{html.escape(text, quote=False)}</span></li>'
            for kind, text in p["caps"]
        )
        foot = " ".join(
            f'<a href="../{q["slug"]}/">{q["name"]}</a>' for q in PLATFORMS if q["slug"] != p["slug"]
        )
        foot = f'<a href="../">Home</a> {foot}'
        page = (
            TEMPLATE
            .replace("%%TITLE%%", p["title"])
            .replace("%%DESC%%", p["desc"])
            .replace("%%BASE%%", BASE_URL)
            .replace("%%SLUG%%", p["slug"])
            .replace("%%NAME%%", p["name"])
            .replace("%%H1%%", p["h1"])
            .replace("%%SUB%%", p["sub"])
            .replace("%%QUIP%%", p["quip"])
            .replace("%%LOGO%%", LOGOS[p["slug"]])
            .replace("%%STATUS_COLOR%%", p["status"][1])
            .replace("%%STATUS%%", p["status"][0])
            .replace("%%CAPS%%", caps)
            .replace("%%CODE%%", highlight(p["code"]))
            .replace("%%FOOT_LINKS%%", foot)
        )
        out = ROOT / p["slug"] / "index.html"
        out.parent.mkdir(exist_ok=True)
        out.write_text(page)
        print(f"wrote {out.relative_to(ROOT)}")

    urls = [f"{BASE_URL}/"] + [f"{BASE_URL}/{p['slug']}/" for p in PLATFORMS]
    sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n'
    sitemap += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for u in urls:
        sitemap += f"  <url><loc>{u}</loc></url>\n"
    sitemap += "</urlset>\n"
    (ROOT / "sitemap.xml").write_text(sitemap)
    print("wrote sitemap.xml")


if __name__ == "__main__":
    build()
