import type {
  AccountRecord,
  BackendPostRef,
  ScheduledJobRef,
  ScheduleCancellation,
  AdapterOperationContext,
  CapabilityManifest,
  CommentRef,
  ConnectedAccountRef,
  ConversationRef,
  DeliveryOutcome,
  DeliveryRef,
  JsonObject,
  MediaAttachment,
  MediaRef,
  MetricValue,
  Page,
  OperationName,
  PlatformPostRef,
  PreparationIssue,
  PreparedPublishTarget,
} from "./types.js";

export interface AccountsAdapter {
  list(
    input: { readonly cursor?: string; readonly limit?: number },
    context: AdapterOperationContext,
  ): Promise<Page<AccountRecord>>;
  get(ref: ConnectedAccountRef, context: AdapterOperationContext): Promise<AccountRecord>;
}

export interface PostsAdapter {
  list?(
    account: ConnectedAccountRef,
    input: { readonly cursor?: string; readonly limit?: number },
    context: AdapterOperationContext,
  ): Promise<Page<JsonObject>>;
  /** Pure, local validation. This method must not perform I/O. */
  prepareTarget(target: PreparedPublishTarget): readonly PreparationIssue[];
  /** Executes exactly one target so the core can preserve independent outcomes. */
  publishTarget(
    target: PreparedPublishTarget,
    context: AdapterOperationContext,
  ): Promise<DeliveryOutcome>;
  getDelivery?(ref: DeliveryRef, context: AdapterOperationContext): Promise<DeliveryOutcome>;
  get?(ref: PlatformPostRef, context: AdapterOperationContext): Promise<JsonObject>;
  cancelScheduled?(
    ref: ScheduledJobRef,
    context: AdapterOperationContext,
  ): Promise<ScheduleCancellation>;
  deleteBackendRecord?(ref: BackendPostRef, context: AdapterOperationContext): Promise<void>;
  removeFromPlatform?(ref: PlatformPostRef, context: AdapterOperationContext): Promise<void>;
}

export interface MediaAdapter {
  upload(
    input: MediaAttachment,
    account: ConnectedAccountRef,
    context: AdapterOperationContext,
  ): Promise<MediaRef>;
}

export interface AnalyticsAdapter {
  getAccountMetrics?(
    account: ConnectedAccountRef,
    context: AdapterOperationContext,
  ): Promise<readonly MetricValue[]>;
  getPostMetrics(
    post: PlatformPostRef,
    context: AdapterOperationContext,
  ): Promise<readonly MetricValue[]>;
}

export interface CommentsAdapter {
  list(
    post: PlatformPostRef,
    input: { readonly cursor?: string; readonly limit?: number },
    context: AdapterOperationContext,
  ): Promise<Page<JsonObject>>;
  reply(
    comment: CommentRef,
    content: { readonly text: string },
    context: AdapterOperationContext,
  ): Promise<CommentRef>;
}

export interface MessagesAdapter {
  listConversations(
    account: ConnectedAccountRef,
    input: { readonly cursor?: string; readonly limit?: number },
    context: AdapterOperationContext,
  ): Promise<Page<JsonObject>>;
  listMessages(
    conversation: ConversationRef,
    input: { readonly cursor?: string; readonly limit?: number },
    context: AdapterOperationContext,
  ): Promise<Page<JsonObject>>;
  send(
    conversation: ConversationRef,
    content: { readonly text: string },
    context: AdapterOperationContext,
  ): Promise<JsonObject>;
}

export interface WebhookVerification {
  readonly valid: boolean;
  readonly method: "hmac" | "shared-secret" | "mock";
  readonly reason?: string;
}

export interface WebhooksAdapter {
  verify(
    input: { readonly headers: Headers; readonly body: Uint8Array },
    context: AdapterOperationContext,
  ): Promise<WebhookVerification>;
  decode(
    input: { readonly headers: Headers; readonly body: Uint8Array },
    context: AdapterOperationContext,
  ): Promise<JsonObject>;
}

export interface SocialAdapter<TNative = never> {
  readonly id: string;
  readonly capabilities: CapabilityManifest;
  readonly accounts?: AccountsAdapter;
  readonly posts?: PostsAdapter;
  readonly media?: MediaAdapter;
  readonly analytics?: AnalyticsAdapter;
  readonly comments?: CommentsAdapter;
  readonly messages?: MessagesAdapter;
  readonly webhooks?: WebhooksAdapter;
  readonly native?: TNative;
}

export function defineAdapter<TNative, TAdapter extends SocialAdapter<TNative>>(
  adapter: TAdapter,
): TAdapter {
  return adapter;
}

export interface AuthorizationDecision {
  readonly account: ConnectedAccountRef;
  readonly allowed: boolean;
  readonly reason?: string;
}

export interface AuthorizationPolicy {
  authorizeTargets(input: {
    readonly operation: OperationName;
    readonly accounts: readonly ConnectedAccountRef[];
    readonly context: AdapterOperationContext;
  }): Promise<readonly AuthorizationDecision[]>;
}

export interface CredentialStore<TCredential = unknown> {
  get(key: string): Promise<{ readonly value: TCredential; readonly revision: string } | undefined>;
  compareAndSet(input: {
    readonly key: string;
    readonly expectedRevision: string | undefined;
    readonly value: TCredential;
  }): Promise<{ readonly updated: boolean; readonly revision?: string }>;
  delete(key: string): Promise<void>;
}

export interface JobRunner<TJob extends JsonObject = JsonObject> {
  enqueue(input: {
    readonly type: string;
    readonly runAt: string;
    readonly payload: TJob;
  }): Promise<{ readonly jobId: string }>;
  cancel(jobId: string): Promise<boolean>;
}
