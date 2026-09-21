import defaultMdxComponents from "fumadocs-ui/mdx";
import type { MDXComponents } from "mdx/types.js";

// Fumadocs calls its two-column card container `Cards`; the docs content uses
// the more descriptive `CardGroup` name inherited from the previous renderer.
// Keep that content readable while mapping it to the native Fumadocs component.
const mdxComponents = {
  ...defaultMdxComponents,
  CardGroup: defaultMdxComponents.Cards,
};

export function useMDXComponents(components?: MDXComponents) {
  return { ...mdxComponents, ...components } satisfies MDXComponents;
}
