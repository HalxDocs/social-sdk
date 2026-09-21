# Endpoint source audit

Retrieved 2026-09-19. These are documentation observations, not live account verification. Local source snapshots are private implementation inputs and must stay outside the documentation corpus and package tarball.

| Backend                 | Source                                                              | Revision                              | Findings and implementation consequences                                                                                                                                                                                                                                                                                                                                 |
| ----------------------- | ------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Zernio                  | https://zernio.com/openapi.yaml                                     | 1.25.1                                | Production origin is `https://zernio.com/api`; endpoints use `/v1`. The selected specification is in `sources/zernio-selected-openapi.json`.                                                                                                                                                                                                                             |
| Zernio publishing       | https://docs.zernio.com/posts/create-post                           | Retrieved 2026-09-19                  | Inspect each `post.platforms` entry. HTTP 207 is successful transport with potentially failed targets. Replay responses can use `existingPost`, despite the 200 schema describing dry runs. Post-create uses `x-request-id` with approximately five-minute replay, separate from 24-hour content deduplication. Never reinterpret that as durable exactly-once behavior. |
| Zernio scheduling       | Same                                                                | Same                                  | Upstream publishes past dates immediately. SDK preflight must reject past scheduling before dispatch.                                                                                                                                                                                                                                                                    |
| Zernio media            | https://docs.zernio.com/guides/media-uploads                        | Retrieved 2026-09-19                  | Presign, PUT bytes without API Authorization, then attach `publicUrl`. PUT returns empty 200, not JSON. Presigned URL lasts one hour; temporary asset retention is seven days. Upstream may compress oversized files; validate selected platform limits and document upstream transformations.                                                                           |
| Zernio events           | https://docs.zernio.com/webhooks                                    | Retrieved 2026-09-19                  | Lowercase hex HMAC-SHA256 over raw bytes, `X-Zernio-Signature`. Event ID in signed body is canonical. No signed delivery timestamp protocol; durable replay protection is application-owned. Five-second acknowledgment budget.                                                                                                                                          |
| Post for Me             | https://api.postforme.dev/docs                                      | OpenAPI 3.0, API document version 1.0 | Embedded Scalar `data-configuration.content` contains the current specification. `/openapi.json` returns 404. Saved `sources/post-for-me-openapi.json` from the authoritative docs. Production endpoints use `/v1`.                                                                                                                                                      |
| Post for Me publishing  | Same, `SocialPostDto` and `SocialPostResultDto`                     | Same                                  | `processed` describes a finished parent. Read `/v1/social-post-results` and inspect `success` per account. `external_id` is correlation metadata; the schema does not establish native idempotency.                                                                                                                                                                      |
| Post for Me accounts    | Same, `SocialAccountDto`                                            | Same                                  | Account responses include access and refresh tokens. SDK mapping must allowlist public identity fields and never expose the original account payload. `external_id` cannot replace tenant grants.                                                                                                                                                                        |
| Post for Me connections | Same, `CreateSocialAccountProviderAuthUrlDto`                       | Same                                  | Default permission is posts; request `feeds` explicitly for feeds/metrics. Redirect override applies to custom credentials, not system credentials. Provider URL/state must stay intact.                                                                                                                                                                                 |
| Post for Me events      | https://www.postforme.dev/resources/real-time-updates-with-webhooks | Retrieved 2026-09-19                  | Compare `Post-For-Me-Webhook-Secret` with registered secret. This authenticates a shared secret header, not a body signature. One-second acknowledgment budget; durable acceptance must precede success.                                                                                                                                                                 |

Direct platform endpoint, scope, eligibility, media, and auth records are added as each adapter is implemented. No paid or authenticated operation has run during source research.

## Post for Me event identity contradiction

The webhook guide asks consumers to deduplicate unique event IDs. The public sender at `https://github.com/DayMoonDevelopment/post-for-me/blob/main/trigger/process-webhook-event.ts`, inspected 2026-09-19, sends only `{ event_type, data }`. Its internal ID is not in the body or headers. The helper therefore uses an explicit `body-digest` identity when no ID is supplied. This collapses byte-identical events, cannot distinguish two intentional identical deliveries, and does not deduplicate semantically equal JSON with different byte encoding. It must not be described as a provider event-ID guarantee. An authoritative live payload can refine this mapping later.

## Bluesky direct adapter

Retrieved 2026-09-19 from the AT Protocol and Bluesky public API references. These records describe the credential-ready adapter contract and do not constitute live account verification.

| Operation              | Endpoint                                                             | Implementation note                                                                                                                                                        |
| ---------------------- | -------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Account identity       | `com.atproto.server.getSession` session fields and configured DID    | The adapter keeps the caller's DID as the stable account reference and does not trust a handle as identity. OAuth/session acquisition remains application-owned.           |
| Text/image publication | `com.atproto.repo.createRecord` with collection `app.bsky.feed.post` | The adapter sends a caller-authorized repository DID, UTC `createdAt`, optional link facets with UTF-8 byte offsets, and image embeds after `com.atproto.repo.uploadBlob`. |
| Native post reads      | `app.bsky.feed.getPosts`                                             | Returned URI and CID are preserved as native metadata.                                                                                                                     |
| Thread/reply reads     | `app.bsky.feed.getPostThread`                                        | A reply uses the returned parent URI/CID and preserves an existing root reference when present. Unknown or non-Bluesky reply refs are rejected.                            |
| Media                  | `com.atproto.repo.uploadBlob`                                        | Uploads use the configured service, bearer authorization, HTTPS, bounded image input (10 MiB), and caller cancellation. Video is explicitly unavailable in this slice.     |

Primary references: https://atproto.com/specs/atp, https://docs.bsky.app/docs/api/com-atproto-repo-create-record, https://docs.bsky.app/docs/api/com-atproto-repo-upload-blob, https://docs.bsky.app/docs/api/app-bsky-feed-get-posts, and https://docs.bsky.app/docs/api/app-bsky-feed-get-post-thread. No live Bluesky credential or public mutation was used.

## X and Threads direct adapters

Retrieved 2026-09-19. These implementations use caller-supplied existing OAuth access tokens and injected fetch; no credentials or live mutations were used.

| Platform | Endpoint family                                            | Implemented behavior                                                                       |
| -------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| X        | POST api.x.com/2/tweets                                    | Text, media ID attachments, reply target, and per-target published outcome.                |
| X        | POST upload.twitter.com/1.1/media/upload.json              | Blob media upload with bearer authorization; the v2 post call receives returned media IDs. |
| X        | GET api.x.com/2/tweets/:id                                 | Native post reads and public_metrics mapping for likes, reposts, replies, and quotes.      |
| X        | GET api.x.com/2/users/:id                                  | User `public_metrics` fields (`followers_count`, `following_count`, `tweet_count`, `listed_count`) are requested with `user.fields`; the adapter verifies the returned user ID and omits absent counters. |
| Threads  | POST graph.threads.net/{version}/{user-id}/threads         | Text and container creation with reply target and content type selection.                  |
| Threads  | POST graph.threads.net/{version}/{user-id}/threads_publish | Explicit container publication and published ID mapping.                                   |
| Threads  | GET graph.threads.net/{version}/{media-id}                 | Native reads and selected insight fields exposed as metrics.                               |
| Threads  | GET graph.threads.net/{version}/{threads-user-id}/threads_insights | User insights use `threads_manage_insights`; the adapter requests documented numeric metrics, maps total values or the latest time-series value, and does not expose demographics. |

Primary references: https://developer.x.com/en/docs/x-api/tweets/manage-tweets/api-reference/post-tweets, https://developers.facebook.com/docs/threads/posts, and https://developers.facebook.com/docs/threads/replies. Media URL preparation and creator approval remain provider/account-dependent.

## Instagram direct adapter

The captured 2026-09-19 Instagram Publishing guide is authoritative for this slice. The adapter uses Instagram Login professional-account tokens on graph.instagram.com v25.0, requires public HTTPS image/video URLs, and keeps container continuation explicit. GET /<IG_CONTAINER_ID>?fields=status_code is used to reconcile IN_PROGRESS, FINISHED, PUBLISHED, ERROR, and EXPIRED; it never starts hidden polling. Carousel children are created before the parent, and an ambiguous child failure retains created IDs in error details for application persistence and reconciliation.

The Instagram Graph `IG User` fields reference (retrieved 2026-09-19, https://developers.facebook.com/docs/instagram-api/reference/ig-user) documents `followers_count` and `media_count`. The direct adapter requests those fields from `/me`, verifies `user_id`, and returns only present numeric counters; no account insights time series or deprecated `impressions` metric is claimed.

## LinkedIn and upload/identifier follow-up, 2026-09-19

LinkedIn REST Posts and Images sources are captured in `sources/linkedin-posts.txt` and `sources/linkedin-images.txt`. The adapter requires an explicit YYYYMM version and author URN. Post creation reads `x-restli-id` from an empty 201 response. Image registration is separate from publication; the image owner and AVAILABLE status are checked before creating the post. This implementation selects text and one image, not organic sponsored-carousel behavior.

Additional primary sources captured locally:

- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/comments-api?view=li-lms-2026-09
- https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/network-update-social-actions?view=li-lms-2026-09
- https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2

Comments use composite comment URNs and verify the parent through the declared post route before replying. Metrics expose only returned social-action counts, with no invented impression count or measurement timestamp. Community Management feed permissions differ from basic publishing scopes. OIDC `/userinfo` does not prove an organization role; connection selection still needs explicit implementation and role evidence.

YouTube upload regression tests verify that empty 403/503 responses remain failures and that short/overlong sources cannot send the final chunk. `native.resumeUpload` queries a saved session before resuming at the confirmed offset. Public results never expose the secret upload URI.

The bounded JSON transport preserves integer tokens outside JavaScript's safe range as decimal strings. TikTok's raw numeric ID fixture `9007199254740993` now becomes that exact native ID rather than a rounded reference. All evidence in this entry is offline contract testing; no provider live verification was performed.

## Direct OAuth connection helpers, 2026-09-19

Provider authorization/token and identity endpoints are implemented as server-only helpers with injected fetch, strict redirect rejection, bounded response bodies, and request timeouts. Google/YouTube follows [Google OAuth](https://developers.google.com/identity/protocols/oauth2/web-server); X follows [X OAuth 2.0](https://developer.x.com/en/docs/authentication/oauth-2-0/authorization-code); TikTok follows [TikTok Login Kit](https://developers.tiktok.com/doc/login-kit-web); Threads follows [Threads authorization](https://developers.facebook.com/docs/threads/get-started/get-access-tokens-and-permissions); Instagram follows [Instagram Login](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login); and LinkedIn follows [Sign In with LinkedIn/OIDC](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2). X uses API v2 OAuth and PKCE; TikTok uses v2 authorization/token endpoints with comma-separated scopes and PKCE; Threads uses the Threads authorization/token and versioned Graph identity endpoints; Instagram uses Instagram Login and versioned Graph identity endpoints; LinkedIn uses OIDC `/userinfo` plus the organizational ACL endpoint. Threads and Instagram expose the documented `th_exchange_token`/`ig_exchange_token` and refresh endpoints. LinkedIn requires an explicit YYYYMM API version and returns account references as `urn:li:person:*` or ACL-authorized `urn:li:organization:*`; an ACL response is never silently ignored. No provider credential or live mutation was used.

## Bluesky OAuth client recipe, 2026-09-19

The maintained `@atproto/oauth-client-node` package (0.5.7) is used for the server recipe in `examples/snippets/bluesky-oauth.ts`. Its `NodeOAuthClient` owns PKCE, PAR, DPoP, authorization-server/resource metadata discovery, issuer and identity checks, callback validation, token refresh, and session restoration. The recipe injects `NodeSavedStateStore` and `NodeSavedSessionStore` implementations and never implements a parallel code exchange. Primary references: [AT Protocol OAuth](https://atproto.com/specs/oauth) and the [oauth-client-node README](https://github.com/bluesky-social/atproto/tree/main/packages/oauth/oauth-client-node). Fixture tests cover callback URL parsing, application state preservation, DID-bound session restore, and state/session row persistence; no live authorization or provider mutation was used.


## Additional read and engagement contracts

LinkedIn organization follower counts use `GET /rest/networkSizes/{organizationUrn}?edgeType=COMPANY_FOLLOWED_BY_MEMBER`, with the caller's explicit monthly API version. `organizationalEntityFollowerStatistics` no longer returns total follower counts. Sources captured in `sources/linkedin-organization-lookup.txt` and `sources/linkedin-followers.txt` from Microsoft Learn on 2026-09-19. This operation requires organization administrator access; no member-profile analytics is inferred.

X reactions use the official `POST /2/users/{id}/likes` and `DELETE /2/users/{id}/likes/{tweet_id}` contracts captured in `sources/x-like.md` and `sources/x-unlike.md`. A success must contain the requested `data.liked` boolean. The helper does not infer confirmation from HTTP 200 alone and never retries a dispatched mutation.


Bluesky reactions follow the official `app.bsky.feed.like` and `com.atproto.repo.deleteRecord` lexicons, captured in `sources/bluesky-like.json` and `sources/bluesky-delete-record.json` from the bluesky-social/atproto repository. The like subject retains both URI and CID. Delete acts only on a returned like URI under the authenticated DID; it cannot delete another repository’s record or reinterpret a post URI as a like.


Bluesky language/mention serialization follows the official `app.bsky.feed.post` and `app.bsky.richtext.facet` lexicons captured in `sources/bluesky-post.json` and `sources/bluesky-facet.json`. Language tags map to `langs` with its maximum of three. Explicit DID mentions retain UTF-8 byte boundaries, reject overlaps and make no implicit handle-resolution requests. A regression test verifies actual createRecord output after an emoji and confirms invalid options fail before I/O.
