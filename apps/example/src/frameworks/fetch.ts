import type { ExampleHandler } from "../app.js";

/** Adapt the example's Request/Response handler to any fetch-compatible server. */
export function createFetchHandler(
  handler: ExampleHandler,
): (request: Request) => Promise<Response> {
  return (request) => handler.handle(request);
}
