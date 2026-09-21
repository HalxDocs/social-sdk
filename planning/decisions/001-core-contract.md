# ADR 001: Core references and fan-out contract

Status: accepted

## Decision

The SDK models a destination as a versioned, JSON-safe reference. Every
reference carries its backend instance, platform, and provider-owned identifier;
account handles are display data and never routing keys. A publication request
contains a shared content object and an explicit target list. A target can add
platform-specific options, content overrides, a reply reference, or a schedule.

`createSocial({ backend })` registers a single backend as `default`.
`createSocial({ backends })` requires account references to name one of the
registered instance keys. The client never changes that route or fails over to
another backend.

`posts.publish()` first asks the optional application authorization policy to
decide every target, then performs all local preparation checks. It dispatches
only when the complete request is authorized and locally valid. Dispatch is
per-target, bounded by the configured concurrency, and returns an outcome for
each target in input order. Adapter errors after dispatch become a failed or
unknown outcome; an unknown outcome is never reported as published.

An application idempotency key is scoped by tenant and operation. The optional
`IdempotencyStore` atomically claims the key with a SHA-256 payload fingerprint
and target set, and persists outcomes independently. Reusing a key with a
different payload conflicts. A restarted call never blindly replays targets
that were claimed without a saved outcome; those targets are returned as
`unknown` for reconciliation. Deterministic per-target keys are derived for
upstream adapters.

The core contains no provider imports, network calls, timers, telemetry, or
filesystem access. Adapter modules are optional and expose unavailable
capabilities instead of empty successful results. Native escape hatches require
an explicit `{ acknowledgeUnsafe: true }` acknowledgement so applications do
not mistake them for normalized tenant-enforced operations.

## Consequences

This gives direct and managed adapters one conformance surface while preserving
provider-specific state. A provider can return richer native data through its
typed adapter and `PlatformPostRef.native`. Durable idempotency and account
membership remain application-owned; the SDK supplies interfaces and a
deterministic in-memory test implementation, not a database or hosted service.
