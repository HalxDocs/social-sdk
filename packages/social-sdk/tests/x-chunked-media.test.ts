/* oxlint-disable anti-slop/require-readable-spacing -- compact mocked transport fixtures. */
import { it } from "node:test";
import assert from "node:assert/strict";
import { createSocial, connectedAccountRef } from "../src/index.js";
import { x } from "../src/platforms/x.js";

const account = connectedAccountRef({ backend: "default", platform: "x", accountId: "u1" });
const auth = { userId: "u1", accessToken: "test" };

function videoBlob(bytes: number): Blob {
  return new Blob([new Uint8Array(bytes)], { type: "video/mp4" });
}

function gifBlob(bytes: number): Blob {
  return new Blob([new Uint8Array(bytes)], { type: "image/gif" });
}

it("X video publish uses 1 MiB chunked upload and attaches the finalized media", async () => {
  const paths: string[] = [];
  const segments: string[] = [];
  const size = 2 * 1024 * 1024 + 512 * 1024;

  const social = createSocial({
    backend: x({
      auth,
      fetch: async (input, init) => {
        const url = new URL(String(input));
        paths.push(url.pathname);

        if (url.pathname === "/2/media/upload/initialize") {
          const body = JSON.parse(String(init?.body));
          assert.equal(body.media_category, "tweet_video");
          assert.equal(body.total_bytes, size);

          return Response.json({ data: { id: "video1" } });
        }

        if (url.pathname.endsWith("/append")) {
          assert.ok(init?.body instanceof FormData);
          segments.push(String(init.body.get("segment_index")));

          return new Response(null, { status: 204 });
        }

        if (url.pathname.endsWith("/finalize")) return Response.json({ data: { id: "video1" } });

        const body = JSON.parse(String(init?.body));
        assert.deepEqual(body.media, { media_ids: ["video1"] });

        return Response.json({ data: { id: "post1" } });
      },
    }),
  });

  const result = await social.posts.publish({
    targets: [{ account }],
    content: {
      text: "Video",
      media: [
        {
          kind: "video",
          mimeType: "video/mp4",
          filename: "clip.mp4",
          byteSize: size,
          source: { kind: "blob", blob: videoBlob(size), fingerprint: "video1" },
        },
      ],
    },
  });

  assert.equal(result.outcomes[0]?.state, "published");
  assert.deepEqual(segments, ["0", "1", "2"]);
  assert.deepEqual(paths, [
    "/2/media/upload/initialize",
    "/2/media/upload/video1/append",
    "/2/media/upload/video1/append",
    "/2/media/upload/video1/append",
    "/2/media/upload/video1/finalize",
    "/2/tweets",
  ]);
});

it("X GIF upload polls processing_info until succeeded", async () => {
  const paths: string[] = [];
  let statusCalls = 0;

  const social = createSocial({
    backend: x({
      auth,
      fetch: async (input, init) => {
        const url = new URL(String(input));
        paths.push(url.pathname);

        if (url.pathname === "/2/media/upload/initialize") {
          const body = JSON.parse(String(init?.body));
          assert.equal(body.media_category, "tweet_gif");

          return Response.json({ data: { id: "gif1" } });
        }

        if (url.pathname.endsWith("/append")) return new Response(null, { status: 204 });

        if (url.pathname.endsWith("/finalize"))
          return Response.json({
            data: { id: "gif1", processing_info: { state: "pending", check_after_secs: 0 } },
          });

        if (url.pathname === "/2/media/upload") {
          statusCalls++;

          return statusCalls === 1
            ? Response.json({
                data: { id: "gif1", processing_info: { state: "in_progress", check_after_secs: 0 } },
              })
            : Response.json({ data: { id: "gif1", processing_info: { state: "succeeded" } } });
        }

        return Response.json({ data: { id: "post2" } });
      },
    }),
  });

  const blob = gifBlob(100);
  const result = await social.posts.publish({
    targets: [{ account }],
    content: {
      text: "GIF",
      media: [
        {
          kind: "image",
          mimeType: "image/gif",
          filename: "clip.gif",
          byteSize: blob.size,
          source: { kind: "blob", blob, fingerprint: "gif1" },
        },
      ],
    },
  });

  assert.equal(result.outcomes[0]?.state, "published");
  assert.equal(statusCalls, 2);
  assert.ok(paths.includes("/2/media/upload"));
});

it("X chunked upload maps a 413 chunk rejection to media_error without retrying the post", async () => {
  let appends = 0;

  const social = createSocial({
    backend: x({
      auth,
      fetch: async (input) => {
        const url = new URL(String(input));

        if (url.pathname === "/2/media/upload/initialize")
          return Response.json({ data: { id: "video2" } });

        if (url.pathname.endsWith("/append")) {
          appends++;

          return new Response("", { status: 413 });
        }

        throw new Error(`unexpected request to ${url.pathname}`);
      },
    }),
  });

  const blob = videoBlob(100);
  const result = await social.posts.publish({
    targets: [{ account }],
    content: {
      text: "Video",
      media: [
        {
          kind: "video",
          mimeType: "video/mp4",
          filename: "clip.mp4",
          byteSize: blob.size,
          source: { kind: "blob", blob, fingerprint: "video2" },
        },
      ],
    },
  });

  assert.equal(result.outcomes[0]?.state, "failed");
  assert.equal(appends, 1);

  if (result.outcomes[0]?.state === "failed") {
    assert.equal(result.outcomes[0].code, "media_error");
    assert.match(result.outcomes[0].message, /chunk rejected/);
  }
});

it("X failed media processing never creates a post", async () => {
  let tweets = 0;

  const social = createSocial({
    backend: x({
      auth,
      fetch: async (input) => {
        const url = new URL(String(input));

        if (url.pathname === "/2/media/upload/initialize")
          return Response.json({ data: { id: "video3" } });

        if (url.pathname.endsWith("/append")) return new Response(null, { status: 204 });

        if (url.pathname.endsWith("/finalize"))
          return Response.json({
            data: { id: "video3", processing_info: { state: "failed" } },
          });

        tweets++;

        return Response.json({ data: { id: "post3" } });
      },
    }),
  });

  const blob = videoBlob(100);
  const result = await social.posts.publish({
    targets: [{ account }],
    content: {
      text: "Video",
      media: [
        {
          kind: "video",
          mimeType: "video/mp4",
          filename: "clip.mp4",
          byteSize: blob.size,
          source: { kind: "blob", blob, fingerprint: "video3" },
        },
      ],
    },
  });

  assert.equal(result.outcomes[0]?.state, "failed");
  assert.equal(tweets, 0);
});

it("X validates chunked media locally without network access", () => {
  let calls = 0;
  const social = createSocial({
    backend: x({
      auth,
      fetch: async () => {
        calls++;

        return Response.json({ data: { id: "never" } });
      },
    }),
  });

  const mixed = social.posts.prepare({
    targets: [{ account }],
    content: {
      text: "Mixed",
      media: [
        {
          kind: "video",
          mimeType: "video/mp4",
          filename: "clip.mp4",
          source: { kind: "blob", blob: videoBlob(10), fingerprint: "mix" },
        },
        {
          kind: "image",
          mimeType: "image/png",
          filename: "still.png",
          source: {
            kind: "blob",
            blob: new Blob([new Uint8Array(10)], { type: "image/png" }),
            fingerprint: "still",
          },
        },
      ],
    },
  });

  assert.equal(mixed.ok, false);
  assert.equal(calls, 0);
});
