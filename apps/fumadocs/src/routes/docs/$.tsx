import { createFileRoute, notFound } from "@tanstack/react-router";
import { createServerFn } from "@tanstack/react-start";
import browserCollections from "collections/browser";
import { useFumadocsLoader } from "fumadocs-core/source/client";
import { DocsLayout } from "fumadocs-ui/layouts/docs";
import { DocsBody, DocsDescription, DocsPage, DocsTitle } from "fumadocs-ui/layouts/docs/page";
import { useRef } from "react";
import { z } from "zod";

import { useMDXComponents } from "@/components/mdx";
import { baseOptions } from "@/lib/layout.shared";
type DocsRequest = { slugs: string[] };

const getDocsData = createServerFn({ method: "GET" })
  .inputValidator(z.object({ slugs: z.array(z.string()) }))
  .handler(async ({ data }: { data: DocsRequest }) => {
  const { source } = await import("@/lib/source");
  const page = source.getPage(data.slugs);
  if (!page) return null;
  return {
    path: page.path,
    pageTree: await source.serializePageTree(source.getPageTree()),
    markdownUrl: data.slugs.length ? `/docs/${data.slugs.join("/")}.md` : "/docs/index.md",
  };
  });

type LoaderData = {
  path: string;
  pageTree: { $fumadocs_loader: "page-tree"; data: unknown };
  markdownUrl: string;
};

export const Route = createFileRoute("/docs/$")({
  component: Page,
  loader: async ({ params }) => {
    const slugs = params._splat?.split("/").filter(Boolean) ?? [];
    const data = await getDocsData({ data: { slugs } });
    if (!data) throw notFound();
    return data as LoaderData;
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
  // The tree is global navigation. Keep the same object as pages change so
  // the sidebar does not reset its open sections or scroll position.
  const pageTree = useRef(loaded.pageTree).current;
  return (
    <DocsLayout {...baseOptions()} tree={pageTree as never}>
      {contentLoader.useContent(loaded.path)}
    </DocsLayout>
  );
}
