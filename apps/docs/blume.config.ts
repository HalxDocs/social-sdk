import { defineConfig } from "blume";

export default defineConfig({
  title: "Social SDK",
  description:
    "Typed social platform integrations for TypeScript applications, with direct routes, optional managed backends, and deterministic testing.",
  logo: {
    image: "/icon.svg",
    text: "Social SDK",
    href: "/",
  },
  basePath: "/docs",
  feedback: false,
  redirects: [
    { from: "/analytics", to: "/reads#post-metrics", status: 301 },
    { from: "/messaging", to: "/comments#messages", status: 301 },
  ],
  content: {
    root: "docs",
    pages: "pages",
  },
  navigation: {
    sidebar: {
      display: "group",
      items: [
        {
          label: "Get started",
          icon: "rocket",
          collapsed: false,
          items: [
            { label: "Install", root: "/getting-started/installation" },
            { label: "Quickstart", root: "/getting-started/mock-quickstart" },
          ],
        },
        { label: "Platforms", root: "/platforms", icon: "globe-2" },
        {
          label: "Direct platforms",
          icon: "plug",
          collapsed: true,
          items: [
            { label: "Bluesky", root: "/platforms/bluesky", icon: "/integrations/bluesky.svg" },
            { label: "X", root: "/platforms/x", icon: "/integrations/x.svg" },
            { label: "Threads", root: "/platforms/threads", icon: "/integrations/threads.svg" },
            { label: "YouTube", root: "/platforms/youtube", icon: "/integrations/youtube.svg" },
            { label: "TikTok", root: "/platforms/tiktok", icon: "/integrations/tiktok.svg" },
            {
              label: "Instagram",
              root: "/platforms/instagram",
              icon: "/integrations/instagram.svg",
            },
            { label: "LinkedIn", root: "/platforms/linkedin", icon: "/integrations/linkedin.svg" },
          ],
        },
        {
          label: "Backends",
          icon: "server",
          items: [
            { label: "Choose a backend", root: "/backends", icon: "route" },
            { label: "Direct", root: "/backends/direct", icon: "route" },
            { label: "Managed setup", root: "/backends/managed", icon: "settings-2" },
            { label: "Zernio", root: "/backends/zernio", icon: "/integrations/zernio.svg" },
            {
              label: "Post for Me",
              root: "/backends/post-for-me",
              icon: "/integrations/post-for-me.svg",
            },
          ],
        },
        {
          label: "Guides",
          icon: "book-open",
          items: [
            "/authentication",
            "/publishing",
            "/reads",
            "/comments",
            "/events",
            "/getting-started/framework-recipes",
            "/agents/integrate-social-sdk",
            "/agents/integration-checklist",
          ],
        },
        {
          label: "Concepts",
          icon: "shapes",
          items: [
            "/concepts/integration-model",
            "/concepts/architecture",
            "/concepts/references-and-outcomes",
            "/concepts/tenant-authorization",
          ],
        },
        {
          label: "Reference",
          icon: "book-open",
          items: [
            { label: "API overview", root: "/reference" },
            "/reference/capabilities",
            "/reference/pagination",
            "/reference/cli",
            "/operations",
          ],
        },
        {
          label: "Contribute",
          icon: "files",
          items: ["/testing/evidence-levels", "/contributing"],
        },
      ],
    },
  },
  theme: {
    accent: "teal",
    mode: "system",
    radius: "md",
  },
  ai: {
    llmsTxt: true,
    mcp: {
      enabled: false,
    },
  },
  deployment: {
    output: "static",
  },
});
