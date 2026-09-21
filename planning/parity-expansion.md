# Full per-platform parity expansion

Owner decision (2026-09-21): drop the "first useful slice" boundary from the master plan.
Each direct adapter should expose everything its platform's official API offers, as typed
platform-specific operations. Generalized operations stay for the shared families
(publish, reads, comments, metrics); everything else ships as typed native modules per
platform, following the pattern in master plan §14.3. This supersedes the master plan's
"no universal parity" note as a scope decision; the honesty rules (evidence, outcomes,
support records) still apply to every new operation.

Parity means parity with each platform's official public API for third-party apps.
Operations the platform does not expose to apps remain documented as platform limits.

## Gap list by platform

Status key: SHIP = build it, GATED = build it but access needs approval/tier, NONE = the
platform offers no API for it (keep documented as a limit, never fake it).

### Bluesky (AT Protocol)

| Operation | Status | Notes |
| --- | --- | --- |
| Video upload + processing states | SHIP | app.bsky.video job states map to processing outcomes. |
| Reposts and quote posts | SHIP | Typed operations, native URIs preserved. |
| Post deletion | SHIP | Record delete in own repo. |
| Follows, blocks, mutes | SHIP | Graph module, typed. |
| Notifications read | SHIP | List + seen state. |
| Profile read/update | SHIP | Own profile record. |
| Chat (DMs) | SHIP | chat.bsky endpoints; consent and moderation rules documented. |
| Custom feeds / list feeds | SHIP | Read side. |

### X

| Operation | Status | Notes |
| --- | --- | --- |
| Video + GIF upload | SHIP | Chunked upload, STT processing states, media categories. |
| Polls | SHIP | Create with post. |
| Retweet / quote | SHIP | Typed engagement ops beside existing like/unlike. |
| Post deletion | SHIP | |
| Bookmarks | SHIP | |
| Follows | SHIP | |
| DMs | GATED | API tier dependent; expose with capability check per plan/scopes. |
| Streams / firehose | GATED | Enterprise tiers; document, do not fake. |

### Threads

| Operation | Status | Notes |
| --- | --- | --- |
| Replies: read, create, hide | SHIP | The API has these; the slice skipped them. |
| Quote posts and reposts | SHIP | |
| Post deletion | SHIP | |
| Profile reads | SHIP | |
| Keyword search | SHIP | |
| Mentions reads | SHIP | |
| DMs | NONE | No Threads messaging API for apps. |

### YouTube

| Operation | Status | Notes |
| --- | --- | --- |
| Scheduled publish (publishAt) | SHIP | Fits existing scheduling contract as platform-native scheduling. |
| Thumbnail set | SHIP | |
| Captions upload/list | SHIP | |
| Playlists CRUD + playlist items | SHIP | |
| Video update / delete | SHIP | |
| YouTube Analytics API | SHIP | Separate API product from Data API; separate scopes. |
| Live broadcasts | GATED | Data API supports; channel eligibility applies. |
| Community posts | NONE | No public API. |

### TikTok

| Operation | Status | Notes |
| --- | --- | --- |
| Draft upload path | SHIP | Inbox/draft flow beside direct post. |
| Own-video list/query | SHIP | Display scope. |
| Publish-status polling helper | SHIP | Explicit, bounded, still no hidden background polling. |
| Comments | NONE | Not in the Content Posting or Display APIs for standard apps. |
| DMs | NONE | Not offered. |

### Instagram

| Operation | Status | Notes |
| --- | --- | --- |
| Reels publishing | SHIP | Container kind exists in Graph API. |
| Stories publishing | SHIP | |
| Post deletion | SHIP | |
| Hashtag search | SHIP | |
| Publishing-limit check | SHIP | Rate-limit endpoint surfaced as typed read. |
| Mentions and tagged reads | SHIP | |
| Product tagging | GATED | Requires shop setup. |
| Messaging | GATED | Messenger Platform for IG; app review required. |

### LinkedIn

| Operation | Status | Notes |
| --- | --- | --- |
| Multi-image posts | SHIP | |
| Video upload | SHIP | registerUpload + processing states, same pattern as images. |
| Documents | SHIP | |
| Polls | SHIP | |
| Reactions | SHIP | Typed, beside existing comment ops. |
| Reshares | SHIP | |
| Post update / delete | SHIP | |
| Richer organization analytics | SHIP | Community Management endpoints, role-gated. |
| Articles | GATED | Verify current API product coverage before claiming. |
| Messaging | NONE | Closed to standard apps; partnership only. |

## Cross-cutting work every new operation needs

- Capability manifest entries and support records per operation, so capability checks stay truthful.
- Contract tests and mocked-transport fixtures, same standard as existing suites.
- Mock backend scenarios so the deterministic path covers the new operations.
- Media processing state machines where uploads are asynchronous (X chunked, Bluesky video, LinkedIn video, IG reels).
- Docs: extend each platform page and the capability matrix; landing prototype checklists regenerate from the same facts.
- Release gate additions for the new suites.

## Suggested build order

1. **Media parity.** X video/GIF, Bluesky video, LinkedIn multi-image + video, Instagram reels + stories. Kills the worst ✗ items.
2. **Conversation parity.** Threads replies, deletion everywhere, reposts/quotes, X polls, LinkedIn reactions/reshares.
3. **Platform extras.** YouTube playlists/captions/thumbnails/publishAt/Analytics, TikTok drafts and video list, IG hashtag search and limits, Bluesky graph/notifications.
4. **Messaging where real.** Bluesky chat, Instagram messaging (approval-gated), X DMs (tier-gated).

## Unchanged constraints

Live verification still requires owner-approved accounts, API products, and app review per
platform. Contract-tested is the local bar; live evidence is recorded separately. NONE
items stay on the docs and landing pages as platform limits so the checkmarks keep meaning
something.
