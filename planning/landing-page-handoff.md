# Landing page handoff

The current root page is a deliberately small placeholder for the owner-designed landing page. Blume owns the site shell and generated documentation. The replacement must preserve the route and docs mount described below.

## Route boundary

- `apps/docs/pages/index.astro` owns `/`.
- `apps/docs/pages/_home/` contains components used only by the placeholder home.
- `apps/docs/docs/` is Blume's public content root.
- `basePath: "/docs"` in `apps/docs/blume.config.ts` mounts generated documentation at `/docs` without adding a `docs` group to its navigation.
- `deployment.base` remains unset. It would move the entire site, including `/`, and is not the docs mount setting.

The future home can replace `pages/index.astro` and delete or replace `_home/` without moving `apps/docs/docs`, changing `basePath`, or modifying generated `.blume/` files.

## Shared Blume surface

The placeholder imports `PageLayout` from `blume/components/layout/PageLayout.astro`. This layout supplies the shared document shell, header, theme mode, fonts, search entry point, metadata, and structured data without the documentation sidebar or table of contents. The replacement may keep `PageLayout` or move to a fully owner-controlled Astro page after a deliberate review.

The configured design tokens are:

- accent: `teal`
- mode: `system`
- radius: `md`

No `theme.css` override is present. The home uses Blume's token-backed Tailwind utilities, so it follows light and dark modes. Add a root `theme.css` only for small shared token changes; do not edit `.blume/`, which the CLI regenerates.

## Assets and links

`apps/docs/public/icon.svg` is the temporary neutral Social SDK mark and favicon. It uses `currentColor` and contains no inherited Email SDK imagery. Replace it through `blume.config.ts` and `public/` when final brand assets exist.

The home links to:

- `/docs/getting-started/mock-quickstart`
- `/docs/backends/direct`
- `/docs/backends/managed`
- `/docs/concepts/*`
- `/docs/testing/evidence-levels`

A repository CTA is intentionally absent until the new repository URL is verified. Do not copy an Email SDK URL into the replacement.

## Content sources

The package name comes from the proposed public package identity, `@opencoredev/social-sdk`. Before release, verification must confirm scope ownership and that the package was actually published under that name.

The home heading is the exact required text: “Social platform integrations for TypeScript apps.” The operation summary follows the selected scope in the master specification. Capability links must remain aligned with implemented adapter manifests and evidence; remove or revise a claim if the corresponding implementation is not in the release.

The placeholder currently shows the verified mock constructor and publication snippet from the core contract (`createSocial`, `mockBackend`, `MemoryIdempotencyStore`, and `connectedAccountRef`). Keep the snippet synchronized with the compiled repository example when the package surface changes.

## Architecture diagrams

`docs/concepts/architecture.mdx` contains four Mermaid diagrams: backend routing, account connection and tenant ownership, per-target publication lifecycle, and durable webhook acceptance. They use Blume's built-in MDX Mermaid renderer and have adjacent text explaining the contract. Keep these diagrams aligned with adapter behavior; they are explanatory documentation, not an assertion that every backend implements every operation.

## Verification

From `apps/docs`, run:

```bash
bun run check-types
bun run validate
bun run build
bun run audit
```

Blume writes the static site to `apps/docs/dist`. Verify `/`, `/docs`, key nested routes, `llms.txt`, `llms-full.txt`, raw page Markdown, search, small-screen navigation, and both color modes. The site is static and does not expose or advertise `/mcp`.

Set an owner-approved production origin through `deployment.site` or the deployment platform before release. Do not invent a product domain. Preview builds must not become the canonical production origin.

The local Blume 1.7.1 audit is clean except for the expected `deployment.site is not set` warning. The canonical URL, sitemap, and absolute social metadata cannot be verified until the owner supplies the production origin. The temporary visual pass used a Tailscale-bound preview at `100.84.34.117:4177`, checked root and architecture routes at desktop and mobile widths in light and dark modes, then stopped the server and closed the browser session. The mobile DOM had no horizontal overflow (`scrollWidth === viewport width`).
