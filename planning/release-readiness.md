# Release readiness

The selected M0–M7 implementation is complete locally and the deterministic release gate passed on September 19, 2026, US Eastern time. This is not a claim of live platform approval or a published release. The full command log is [release-ci.txt](evidence/release-ci.txt); its digest and counts are in [release-checks.json](evidence/release-checks.json).

## Implemented

`@opencoredev/social-sdk` provides modular TypeScript/ESM entrypoints for the client, server helpers, testing backend, two managed backends, and seven direct platforms. The core includes account/native-post/delivery/scheduled-job/backend-record references, platform-specific options, local preparation, tenant authorization, per-target durable idempotency, bounded per-backend concurrency, per-destination outcomes, explicit reconciliation, scoped pagination, bounded media streaming, and redacted errors. No hosted Social SDK service, database, queue, React dependency, telemetry, startup requests, or implicit polling is required by the SDK.

| Backend | Implemented scope and material limits |
| --- | --- |
| Bluesky direct | Credential-ready JWT or maintained OAuth session transport; account/profile counts; text/images with language tags, explicit DID mentions and rich-text link facets, native reads, author feed, strong reply relationships, engagement counts, like/unlike record helpers. Direct video is outside the selected Bluesky slice and explicitly unavailable. |
| X direct | Account authorization, text/media publication and processing, native post/feed reads, replies, returned post/account counts, typed like/unlike helpers. API scopes, plan access, and billing still apply. |
| Threads direct | Account connection, text/image/video/carousel containers, explicit publish/status continuation, reads/feed/replies and post/account insights. Daily/unknown metric periods are preserved. |
| YouTube direct | Channel discovery, resumable video uploads, status/read/uploads feed, comments/replies, returned video/channel statistics. Analytics-history API and automatic polling are not claimed; hidden subscriber counts remain absent. |
| TikTok direct | Creator information and explicit preview/consent/privacy/interaction/disclosure choices; verified-URL photo/video or draft transfer, explicit status/native IDs, video reads/feed and account/post counts. Audit, verified origins and requested permissions remain required. |
| Instagram direct | Instagram Login professional accounts; image/video/carousel container publication and explicit continuation, native reads/feed, comments/replies, post insights and current follower/media counts. No personal-account eligibility or unsupported inbox is inferred. |
| LinkedIn direct | Member/organization discovery, public text/single-image publishing, image registration/status, native reads/author feed, comment replies and returned social-action counts. Organization follower counts require administrator access. Member analytics, video and multi-image publication are not claimed by this selected slice. |
| Zernio managed | Account connections, selected-platform publication/scheduling/status, media upload, native/feed reads, post metrics and add-on follower snapshots, comments/replies, supported conversations/messages, verified events. Cancel schedule, delete draft backend record, and selected-platform native unpublish are distinct operations with single-destination ownership checks. |
| Post for Me managed | Project-scoped connections/accounts, media, selected-platform publication/scheduling/results, native feeds with optional post metrics, verified shared-secret events. Schedule cancellation retains a draft; backend-record deletion does not claim native removal. Its documented API has no account-level metric or implemented inbox/comment endpoint in this slice. |

The generated [capability matrix](../apps/docs/docs/reference/capabilities.mdx) and [machine-readable manifests](evidence/capability-manifests.json) contain 321 declarations. These are operation-specific and now include the parity expansion declarations. Native helpers bypass normalized client authorization/concurrency and are documented as credential-ready server operations requiring application authorization.

Server helpers implement staged connection selection, state/session/tenant binding, denial/cancellation/expiry, exchange claims, credential CAS and refresh contracts. The Bluesky recipe uses `@atproto/oauth-client-node` for AT Protocol OAuth rather than a simplified exchange. Provider-specific webhook verification and durable event correlation preserve uncertain writes, duplicate/out-of-order events and removal reports.

The deterministic mock, diagnostic CLI, integration skill, Fetch/Next/Hono recipes and SQLite example are implemented. The example exercises account selection, preparation, mixed results, video processing, explicit reconciliation, metrics, comment replies and a durable webhook worker. It rechecks membership before processing queued events.

## Documentation and rebrand

Fumadocs, inherited email runtime/packages/content, Notra integration, telemetry, old release workflow, deployment identifiers, Homebrew formula and brand assets were removed. Required LICENSE attribution remains. Rebrand checks cover source, build outputs and the packed consumer.

Blume 1.7.1 owns the static docs under `/docs`, including platform/backend setup, auth, publishing/media, reads, analytics, comments, messaging, events, framework recipes, diagrams, CLI and machine-readable documentation. The isolated root page at `apps/docs/pages/index.astro` is a small replaceable home using Blume styling. No live MCP endpoint is advertised. See [landing-page-handoff.md](landing-page-handoff.md).

## Verification

The complete gate passed:

```bash
SOCIAL_NODE22_BIN=/home/leo/.npm/_npx/f6c81a5e22bed22a/node_modules/node/bin/node bun run release:ci
```

On other machines, omit `SOCIAL_NODE22_BIN` or point it to a local Node 22.12+ binary. The gate always tests the active Node runtime; the variable adds the second runtime.

| Check | Result |
| --- | --- |
| Frozen install, lint, format, workspace types and negative type tests | Passed |
| SDK tests | 182 passed on Bun; 182 passed on Node 24 |
| Example tests | 19 passed on Bun |
| Example plus OAuth/setup recipes | 23 passed on Node 24 and 23 on Node 22.12; SQLite compatibility flag enabled |
| Agent recipes and executable snippets | 4 agent recipe tests passed; snippets compiled and deterministic examples ran |
| Workspace build and capability conformance | Passed; 321 declarations checked against runtime methods |
| Rebrand | Passed; 697 files scanned, plus packed-consumer checks |
| Tarball consumers and CLI | Node 22.12.0, Node 24.20.0, Bun 1.4.2; all 12 entrypoints imported with zero network calls |
| Package size | 155 files; 170,710 compressed bytes; 923,470 unpacked bytes |
| Blume production build, strict types and link validation | Passed; no broken links |
| Blume audit | 3,040 audits, zero errors, one owner-dependent `deployment.site` warning |

Bun and CI are pinned to the tested 1.4.2 version. The final gate used those pins and passed a frozen install without dependency changes. The final evidence/docs edits were checked after the gate.

Measured on Linux x64, AMD Ryzen 9 9955HX, Bun 1.4.2:

- Core bundle: 6,655 gzip bytes; core plus selected managed backend: 18,256 gzip bytes.
- Twenty-target preparation p95: 0.0105 ms; one-target SDK dispatch overhead p95: 0.0420 ms, excluding upstream network latency.
- The 512 MiB streaming fixture held at most 524,288 outstanding source bytes. Sampled ArrayBuffer growth was 87,293,952 bytes; no whole-video buffering. The consuming fetch was injected, not a live upload.
- Blume whole-build JavaScript: 5,265,095 raw / 1,551,340 gzip bytes; CSS: 241,467 raw / 34,968 gzip bytes. This includes optional search/diagram chunks and is not a page-load network measurement.

Exact methodology and samples: [performance](evidence/performance.json), [media memory](evidence/media-memory.json), [docs assets](evidence/docs-assets.json). All configured budgets passed.

Earlier browser acceptance used server Chromium at 1280×900 and 390×844. Mock publication/video/reconciliation/events/metrics/comments passed; axe reported zero violations; docs search, navigation and Mermaid rendered with no console errors. Only the development server’s browser and network were tested, not a laptop or phone. Temporary preview servers were stopped. See [browser evidence](evidence/browser-checks.json).

## Live coverage

No live provider account, platform operation, paid API request, publication, comment, message, schedule, deletion, upload, OAuth exchange or webhook delivery was verified. Evidence is deterministic fixtures, official source contracts, package consumers and the mock browser flow. No missing credential is counted as a pass. External-link/network audits were not run against a deployed docs origin.

## Remaining work

No selected local implementation or deterministic verification task remains open. External release acceptance still requires:

1. Owner-approved test accounts, credentials, app products/scopes and API access for each intended backend/platform. Run authorized live connection/read/media/publication/event checks with explicit targets and spending/mutation limits; record results separately from fixtures.
2. Provider approvals where applicable: X API access/billing, Meta account/app permissions, TikTok audit/verified origins and creator consent, YouTube audit/quota, LinkedIn product access/admin roles, and managed provider plans/add-ons.
3. Owner-approved canonical docs origin and hosting project to resolve the single Blume audit warning and verify absolute canonical/social/sitemap URLs.
4. Verified new GitHub repository/npm scope identity, publishing credentials/OIDC, release version and explicit publish/deploy authorization.

Additional platforms, a hosted Social SDK cloud, CJS, a marketplace, direct Bluesky video and broad historical analytics remain outside the agreed slices. Unsupported API operations are not emulated through scraping.

## How to run

From the repository root:

```bash
bun install --frozen-lockfile
bun run build
bun run release:ci
bun run test:node
bun run --cwd apps/example dev
bun run --cwd apps/docs dev
```

The example defaults to the deterministic mock backend and binds to loopback on port 3030. Its Node runner enables `--experimental-sqlite` for Node 22.12. The docs dev server uses port 4000 and serves `/` plus `/docs`. Before sharing either server across devices, follow the repository’s verified private-preview workflow; no preview is currently running.

Diagnostics after building:

```bash
node packages/social-sdk/dist/cli.js adapters --json
node packages/social-sdk/dist/cli.js doctor --json
```

These commands do not authenticate or send a provider request. Real example backends require server-side configuration described in `apps/example/README.md`.

## Release controls

The package remains `private: true`; `bun run release` is deliberately locked. No code was pushed, published, merged or deployed. No inherited production target was reused. Local changes remain in this worktree for owner review. The minor changeset records the first independent Social SDK feature release, but does not authorize publication.

## Owner handoff

Replace only `apps/docs/pages/index.astro` and its private `_home` components for the final landing design; preserve Blume’s `/docs` mount and docs content. Approve the final branding/domain, new repository/package identity, release/deployment setup, and credentials/access for intended live checks. [landing-page-handoff.md](landing-page-handoff.md) explains the route and styling boundaries.
