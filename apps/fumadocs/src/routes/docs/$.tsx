import { createFileRoute, notFound } from "@tanstack/react-router";
import browserCollections from "../../../.source/browser";
import { useFumadocsLoader } from "fumadocs-core/source/client";
import { DocsLayout } from "fumadocs-ui/layouts/docs";
import { DocsBody, DocsDescription, DocsPage, DocsTitle } from "fumadocs-ui/layouts/docs/page";

import { useMDXComponents } from "@/components/mdx";
import { baseOptions } from "@/lib/layout.shared";
import { markdownUrl, source } from "@/lib/source";

type LoaderData = {
  path: string;
  pageTree: Awaited<ReturnType<typeof source.serializePageTree>>;
  markdownUrl: string;
};

export const Route = createFileRoute("/docs/$")({
  component: Page,
  loader: async ({ params }) => {
    const slugs = params._splat?.split("/").filter(Boolean) ?? [];
    const page = source.getPage(slugs);
    if (!page) throw notFound();
    return {
      path: page.path,
      pageTree: await source.serializePageTree(source.getPageTree()),
      markdownUrl: markdownUrl(page.slugs),
    } satisfies LoaderData;
  },
});

const contentLoader = browserCollections.docs.createClientLoader({
  component({ toc, frontmatter, default: MDX }) {
    return (
      <DocsPage toc={toc}>
        <DocsTitle>{frontmatter.title}</DocsTitle>
        {frontmatter.description ? <DocsDescription>{frontmatter.description}</DocsDescription> : null}
        <DocsBody><MDX components={useMDXComponents()} /></DocsBody>
      </DocsPage>
    );
  },
});

function Page() {
  const data = Route.useLoaderData() as LoaderData;
  const loaded = useFumadocsLoader(data);
  return (
    <DocsLayout {...baseOptions()} tree={loaded.pageTree}>
      {contentLoader.useContent(loaded.path)}
    </DocsLayout>
  );
}
