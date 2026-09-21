# Implementation status

The selected M0–M7 local implementation is complete. This ledger maps the master-plan sections to implementation and verification evidence; the final command log and external release requirements are recorded in `release-readiness.md`. Implementation and contract tests are distinct from live verification, provider approval, publishing, and deployment. No live provider operation has been verified or released.

## Requirement evidence

| Area | Implemented evidence | Verification or remaining proof |
| --- | --- | --- |
| S01–S05 decisions, isolation, rebrand, tooling | Social SDK workspace/package identity, private release lock, inherited runtime/docs/integrations removed, LICENSE retained | Frozen install, source/build rebrand scan and packed-consumer checks passed. |
| S06–S09 core contracts and capabilities | Typed account/native/delivery/job/backend-record refs, target routing, preparation, discriminated outcomes, per-account options, explicitly unsafe native access, generated declarations | Core/negative type tests, capability drift and runtime method conformance passed. |
| S10 managed backends | Zernio and Post for Me request mapping, per-account results, media vault/presigned upload, native reads and metrics, managed scheduling | `managed-adapters`, `managed-outcomes`, `managed-media`, `lifecycle` fixtures; no live account evidence. |
| S10 direct backends | Bluesky, X, Threads, YouTube, TikTok, LinkedIn, Instagram | Per-adapter suites cover selected implementation contracts; account/API approval and live evidence remain separate. |
| S11 connections | Staged discover/select, atomic exchange claim, durable-store contracts, session/backend/tenant binding, shared-account grants, credential CAS/encryption | `oauth`, `server-lifecycle`, `authorization`, example storage tests. |
| S11 provider OAuth | Six direct OAuth providers plus maintained AT Protocol OAuth recipe and session transport | Callback validation, PKCE, scopes, exchange/refresh, bounded response fixtures. Provider setup is documented; live approval not verified. |
| S12 publication orchestration | Target overrides, reply/schedule fingerprints, tenant-scoped keys, durable idempotency, independent outcomes, explicit continuation/reconciliation | Core restart/replay/ambiguity and per-backend concurrency fixtures passed. |
| S12 scheduling/removal | Scoped cancelScheduled/deleteBackendRecord/removeFromPlatform APIs; owned single-destination managed records only | Six lifecycle tests. Zernio native unpublish supports its documented selected platforms; Post for Me record deletion does not claim native deletion. |
| S13 media | Bounded streaming, URL/host policies, scoped reusable managed handles, persisted Threads/Instagram containers, YouTube resumable session | Stream, transport, managed media, lifecycle and upload-budget tests. Final streaming memory benchmark passed. |
| S13 content | Unicode/UTF8/grapheme and X weighted text validation, explicit Bluesky language/DID-mention serialization, platform media/options, TikTok consent/creator choices | Platform preparation fixtures. Further contract coverage must follow verified provider constraints. |
| S14 reads/pagination | Native post/feed reads, account pages, comments/message cursors, scoped opaque cursors, lazy bounded iteration | Pagination/feed contract fixtures and executable snippets passed with backend dispatch queues. |
| Parity expansion | Typed native parity modules for Bluesky, X, Threads, YouTube, TikTok, Instagram, and LinkedIn; capability declarations for available, gated, and platform-limited operations | `parity-native.test.ts` covers deterministic Bluesky, X, and YouTube routes. Provider approval and live evidence remain external. |
| S14 analytics | Post/account metrics with source/units/interval/freshness and absent-versus-zero handling | Adapter suites passed; Post for Me has no documented account-metrics endpoint. |
| S14 comments/messages | Selected direct comments/replies, typed X/Bluesky reactions and Zernio conversation/message operations; permission and parent-reference checks | Direct adversarial parent-binding tests, pagination fixtures; message delivery/read receipts are not invented. |
| S15 webhooks | Provider-specific HMAC/shared-secret verification, lossless integer IDs, event normalization and record correlation, all-account tenant intersection | Eight webhook tests; Post for Me backend-record deletion is distinct from native removal. |
| S15 durable example worker | SQLite inbox and delivery index, managed/mock routing, quarantine, bounded batches, transactional application, separate removal reports | 19 example tests passed, including managed worker restart/replay and revoked membership checks. |
| S16 transport/errors/budgets | Writes once, bounded read retries, redacted errors/hooks, total context elapsed budgets, cancellation independent of cooperative fetch | Transport/budget tests. YouTube shared invocation deadlines and per-backend queues passed integration tests. |
| S17 packaging/runtime | ESM exports, Node22/24/Bun targets, packed consumer/CLI execution, zero import fetch checks | Final Node22/24/Bun packed-consumer and CLI runs passed; no CJS support claimed. |
| S18 performance | Reproducible bundle/preparation/dispatch and streamed-media measurements; static docs asset report | Final `planning/evidence/{performance,media-memory,docs-assets}.json` measurements passed configured budgets. |
| S19 mock/CLI/skill | Deterministic scenarios, offline diagnostic CLI, integration skill with executable recipes | CLI and skill tests; packed consumer exercise. |
| S20 example/framework recipes | Working account selection/composer/preview/outcomes/video/reconcile/metrics/comments/webhook UI; optional real backends; Fetch/Next/Hono wrappers | Mock browser flow and axe passed. Wrappers are contract-tested; no full Next/Hono app deployment claimed. |
| S21–S23 Blume/docs/home | Blume1.7.1 static docs under /docs, isolated minimal home, platform/backend/operation/auth/framework guides, source snippets | Strict build/check/validate have passed. Audit has one owner-dependent deployment.site warning. |
| S24 tests/security | Node/Bun suites, type tests, transport contracts, tenant/callback/media/event regression tests, browser evidence | Final SDK Bun/Node suites, Node22/24 example/recipe tests and browser evidence are linked in release-readiness.md. |
| S25 release gates | Frozen install, lint/format, types, Bun/Node/example/recipe checks, build, capabilities, rebrand, pack, benchmarks, strict docs audit | `release:ci` runs `scripts/release-gate.ts`; final gate passed. Exact log and runtime counts are retained under planning/evidence. |
| S26–S31 milestones, risks, handoff | Master plan, source captures, release lock and this evidence ledger | Integrated release gate and selected requirement audit completed; external live/release actions remain owner-dependent. |

## Milestones

| Milestone | Current state |
| --- | --- |
| M0 isolation | Complete locally; frozen install and source/build/package rebrand checks passed. |
| M1 core/mock | Complete; core/mock/concurrency contract tests passed. |
| M2 first adapters | Direct plus both managed publication/video fixtures implemented. |
| M3 lifecycle/security | Complete in selected paths; deadline/worker/ownership integration tests passed. |
| M4 full selected operations | Selected direct/managed operation slices complete, including feeds, account metrics and typed reactions. |
| M5 docs migration | Complete; generated support, strict types/build/links and audit verified. |
| M6 example/tooling | Mock example, framework wrappers, CLI and integration skill implemented and tested. |
| M7 verification/handoff | Complete locally; release gate, measurements, support audit and handoff recorded. |

## Remaining implementable work

No selected local implementation or deterministic verification task remains open. See `release-readiness.md` for operation-level limitations, exact command results and external release acceptance actions. No live verification, provider approval, publication or deployment is inferred from passing fixtures.

## Human actions

Owner-approved accounts, credentials, API products/scopes, provider review, and any metered or mutating live tests remain outside deterministic verification. Publishing and deployment need the new repository/package identity, canonical docs origin, and explicit owner authorization. They do not excuse unfinished local implementation.
