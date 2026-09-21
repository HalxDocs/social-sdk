# Social SDK — Agent Kickoff

Use this prompt in the **local Social SDK clone** of Email SDK, with `SOCIAL_SDK_MASTER_PLAN.md` attached or available in the working directory. Do not run it against the original project's production checkout.

---

You are implementing Social SDK in a clone of the Email SDK repository. Read **all of `SOCIAL_SDK_MASTER_PLAN.md`** before changing architecture. It is the complete build specification and acceptance contract, not background reading. Put a copy under `planning/` if it is only available as an attachment; do not include private planning material in public docs.

Your job is to **implement the product and complete the docs migration**, not generate another plan or stop after scaffolding. Audit the repository briefly, preserve unrelated owner work, isolate old release/deployment targets, create a requirement/evidence ledger, then follow milestones M0–M7 in dependency order. Continue with independent work when a credential or approval is missing.

Build a modular TypeScript SDK for social platforms: account connections, media/publishing, content reads, basic analytics, comments, supported messaging, and events. Direct platform integrations are first-class; Zernio and Post for Me are optional managed backends. No mandatory Social SDK cloud, database, queue, React, or AI framework. Keep typed platform/provider-specific features and honest capabilities rather than reducing everything to basic posting or pretending every backend supports everything.

Reuse useful workspace, build, release, and test infrastructure, but replace Email SDK's domain model and **all active branding, docs, exports, dependencies, examples, metadata, telemetry, release destinations, and old website integrations**. Preserve required licenses/attribution. Do not touch or push to the original Email SDK remote, reuse old production deployment identifiers, publish packages, or deploy without explicit authorization.

**Replace Fumadocs completely with Blume at https://useblume.dev/.** Use the installed version's documented configuration and components. Build the complete docs under `/docs` with a minimal root home using Blume's existing styling, theme tokens, and a little factual copy. The owner is designing the final landing page separately: do not create an elaborate marketing page or overwrite their design work. Keep the home isolated and document how to replace it. Static docs must not advertise a live MCP endpoint that has not been deployed.

Prioritize precise resource/account references, server-side tenant authorization, per-destination outcomes, safe media handling, explicit consent where required, bounded retries, uncertain-write reconciliation, backend-specific webhook verification, and no hidden background requests or telemetry. The master plan defines the detailed contracts and tests.

Deliver the deterministic mock backend, one complete integration example, executable docs snippets, agent integration skill, safe small diagnostic CLI, consumer tarball/runtime tests, and measured performance/bundle reports. Test a direct adapter and both managed adapters early, including a video workflow. Do not call missing credentials a successful live verification, present `processed` as published, or implement unsupported operations as fake successes.

Track every selected requirement through code, tests, docs, and evidence. Explicitly distinguish implemented, contract-tested, live-verified, approval-dependent, and deferred work. Keep our own cloud, additional managed providers, reviews, ads, blogs, telephony, and a large UI framework outside this build.

At completion, provide the report required by section 29: what works, precise support coverage, rebrand/Blume changes, exact verification commands and results, measured performance, remaining blockers, actual local run commands, and the owner landing-page/release handoff. Do not claim the entire plan is finished when selected work is omitted. Finish all implementable work and name the exact remaining human actions without fabricating them.
