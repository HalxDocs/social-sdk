import { zernio } from "@opencoredev/social-sdk/cloud/zernio";
import { postForMe } from "@opencoredev/social-sdk/cloud/post-for-me";
import { bluesky } from "@opencoredev/social-sdk/bluesky";
import { mockBackend, type MockScenario } from "@opencoredev/social-sdk/testing";
import type { ExampleOptions } from "./app.js";

/** Explicit local-demo setup. Application authentication replaces this demo session in production. */
export function exampleBackendConfig(
  env: Readonly<Record<string, string | undefined>>,
): ExampleOptions {
  const kind = env["EXAMPLE_BACKEND"] ?? "mock";
  const backendName = kind === "mock" ? "default" : kind;
  const required = (key: string) => {
    const value = env[key];
    if (!value?.trim()) throw new Error(`${key} is required for ${kind}`);
    return value;
  };
  if (kind === "mock") {
    const scenario = env["EXAMPLE_SCENARIO"] ?? "mixed-success-failure";
    if (
      ![
        "immediate-text-success",
        "media-processing-then-success",
        "mixed-success-failure",
        "accepted-response-lost",
        "expired-permission",
        "reconnect-required",
      ].includes(scenario)
    )
      throw new Error("Unsupported EXAMPLE_SCENARIO");
    return {
      backendName,
      backend: mockBackend({ backendInstance: backendName, scenario: scenario as MockScenario }),
    };
  }
  const ids = new Set(
    required("EXAMPLE_ACCOUNT_IDS")
      .split(",")
      .map((id) => id.trim())
      .filter(Boolean),
  );
  const shared = {
    backendName,
    session: { principal: "local-demo-user", tenantId: "local-demo-tenant" },
    membership: (session: { tenantId: string }, accountId: string) =>
      session.tenantId === "local-demo-tenant" && ids.has(accountId),
  };
  switch (kind) {
    case "zernio":
      return {
        ...shared,
        backend: zernio({
          apiKey: required("ZERNIO_API_KEY"),
          ...(env["ZERNIO_WEBHOOK_SECRET"] ? { webhookSecret: env["ZERNIO_WEBHOOK_SECRET"] } : {}),
        }),
      };
    case "post-for-me":
      return {
        ...shared,
        backend: postForMe({
          apiKey: required("POST_FOR_ME_API_KEY"),
          ...(env["POST_FOR_ME_WEBHOOK_SECRET"]
            ? { webhookSecret: env["POST_FOR_ME_WEBHOOK_SECRET"] }
            : {}),
        }),
      };
    case "bluesky":
      return {
        ...shared,
        backend: bluesky({
          backend: backendName,
          auth: {
            service: required("BLUESKY_SERVICE"),
            did: required("BLUESKY_DID"),
            accessJwt: required("BLUESKY_ACCESS_JWT"),
          },
        }),
      };
    default:
      throw new Error("EXAMPLE_BACKEND must be mock, zernio, post-for-me, or bluesky");
  }
}
