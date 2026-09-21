# Rebrand inventory

This file records inherited product surfaces removed or intentionally retained during the Social SDK isolation. It is an internal audit and is allowlisted by the automated legacy-name check.

## Repository boundary

| Surface               | Before                                                                         | Current treatment                                                                         | Evidence                             |
| --------------------- | ------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------- | ------------------------------------ |
| Git remote            | `opencoredev/social-sdk`                                                       | Retained; fetch and push URLs already identify the new repository. No push was performed. | `git remote -v`                      |
| Package workspace     | `email-sdk` and `@email-sdk/config`                                            | Replaced by the private Social SDK workspace and `@social-sdk/config`.                    | Root and package manifests           |
| Public package        | `@opencoredev/email-sdk`                                                       | Proposed `@opencoredev/social-sdk`, version `0.0.0`, with `private: true`.                | `packages/social-sdk/package.json`   |
| CLI                   | `email-sdk`                                                                    | Removed. A new diagnostic CLI can be exported only after implementation and tests.        | Package manifest                     |
| Release automation    | Automatic Changesets publication from `main`                                   | Removed. The root release command fails closed.                                           | Root manifest and workflow inventory |
| CI live checks        | Inherited provider credentials and authentication jobs                         | Removed. CI is offline and deterministic.                                                 | `.github/workflows/ci.yml`           |
| Documentation         | Fumadocs application and old production deployment wiring                      | Removed. Blume work lives in `apps/docs`.                                                 | Workspace tree                       |
| Content and telemetry | Notra fetches, PostHog clients and release annotations                         | Removed. No replacement telemetry is enabled.                                             | Rebrand scan                         |
| Component             | `@opencoredev/convex-email`                                                    | Removed; no placeholder social component was created.                                     | Workspace tree                       |
| Distribution extras   | Homebrew formula and update automation                                         | Removed until a real package is published.                                                | Workspace tree                       |
| Brand assets          | Envelope logos, backgrounds, screenshots, and social cards                     | Removed. New assets must be specific to implemented Social SDK surfaces.                  | Asset inventory                      |
| Email runtime         | Provider adapters, SMTP/MIME, templates, fallback routes, and old live scripts | Removed rather than ported.                                                               | Workspace and scripts inventory      |
| Attribution           | MIT license and Git history                                                    | Preserved.                                                                                | `LICENSE`, `.git`                    |

## Removed paths

The isolation removes the inherited runtime packages, old docs application, legacy skills, live-provider scripts, old release and blog workflows, deployment configuration, formula, launch smoke fixture, email-specific issue templates, old pending Changesets, and brand artwork.

These removals are recoverable from Git history. They do not delete or rewrite the repository history.

## Active identity

- Product: Social SDK
- Proposed package: `@opencoredev/social-sdk`
- Package state: private and unpublished
- Documentation application: `apps/docs`
- Canonical production origin: unset pending an owner-approved domain
- Release workflow: absent
- Deployment workflow and project ID: absent
- Telemetry: absent

## Remaining manual checks

Before release, inspect newly generated site images and packed artifacts visually, verify npm ownership and trusted-publisher configuration against the new repository, approve a canonical origin, and rerun the scanner against built docs and tarball contents.

## Blume disabled-feedback artifact

Blume 1.7.1 emits a PageFeedback client chunk even when `feedback: false`. No generated HTML or other asset references that chunk in the static build. It contains optional compatibility callbacks for third-party analytics globals, rather than a configured tracker for this site. The build now disables feedback and removes only this unreachable generated chunk after checking that no other output references its filename. A future build that references it fails the pruning check. The rebrand gate scans the remaining built SDK and docs output, including LLM/search assets.
