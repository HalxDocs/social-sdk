import { docs } from "collections/server";
import { loader } from "fumadocs-core/source";
import { createElement } from "react";

const platformIcons = new Set(["bluesky", "x", "threads", "youtube", "tiktok", "instagram", "linkedin"]);

export const source = loader({
  source: docs.toFumadocsSource(),
  baseUrl: "/docs",
  icon: (icon) => {
    if (!icon || !platformIcons.has(icon.toLowerCase())) return undefined;
    const slug = icon.toLowerCase();
    return createElement("img", {
      src: `/integrations/${slug}.svg`,
      alt: "",
      "aria-hidden": true,
      className: `fd-platform-icon fd-platform-icon-${slug}`,
      width: 18,
      height: 18,
    });
  },
});

export function markdownUrl(slugs: string[]) {
  return slugs.length ? `/docs/${slugs.join("/")}.md` : "/docs/index.md";
}
