# -*- coding: utf-8 -*-
"""aspnet batch 1: api-design, authn-authz, authorization, caching-background."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import apply

apply("tutorials/aspnet/api-design.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What does idempotent mean, and which HTTP methods are?</summary>
      <p>An operation is <strong>idempotent</strong> if making the same request many times has the <strong>same effect on
      server state</strong> as making it once. The responses can differ — a second <code>DELETE</code> may return 404 where the
      first returned 204 — but the state of the system ends up the same.</p>
      <pre>  GET    /orders/42          safe and idempotent: reads only
  PUT    /orders/42  {...}   idempotent: sets the same full state every time
  DELETE /orders/42          idempotent: gone after one call or five
  POST   /orders             NOT idempotent: every call creates another order
  PATCH  /orders/42          depends: "set status to shipped" is, "add one item" is not</pre>
      <p>By specification, <code>GET</code>, <code>HEAD</code>, <code>OPTIONS</code>, <code>PUT</code> and
      <code>DELETE</code> are idempotent; <code>POST</code> is not; and <code>PATCH</code> is not guaranteed to be. A related
      term is <strong>safe</strong>: a safe method has no side effects at all. Every safe method is idempotent, but
      <code>PUT</code> and <code>DELETE</code> are idempotent without being safe.</p>
      <p>The reason it matters is <strong>retries</strong>. Networks fail after the server has done the work but before the
      response arrives, and the client cannot tell the difference between "never processed" and "processed, reply lost".
      Clients, proxies and resilience handlers therefore retry — and they retry idempotent requests freely, because repeating
      them is harmless. Retrying a <code>POST</code> that places an order places it twice.</p>
      <p>Two consequences follow. An API must <strong>honour</strong> the semantics it advertises: a <code>GET</code> that
      changes state will be triggered by crawlers, prefetchers and caches. And operations that must be retryable but are not
      naturally idempotent need help — an <code>Idempotency-Key</code> header whose result the server stores and replays, or a
      <code>PUT</code> to a client-generated identifier.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> Why should a list endpoint return an object rather than a bare array?</summary>
      <p>Because an object can <strong>grow without breaking clients</strong>, and an array cannot.</p>
      <pre>  // bare array: nowhere to put anything but the items
  [ { "id": 1, ... }, { "id": 2, ... } ]

  // envelope: room for metadata, today or later
  {
    "items": [ { "id": 1, ... }, { "id": 2, ... } ],
    "nextCursor": "eyJpZCI6Mn0",
    "totalCount": 1234
  }</pre>
      <p>Almost every list endpoint eventually needs <strong>metadata</strong>: a cursor or page number for pagination, a total
      count, a flag saying results were truncated, links to the next page. With an envelope, adding a field is an
      <strong>additive, non-breaking change</strong> — existing clients ignore fields they do not know. With a bare array, the
      top-level JSON value <em>is</em> the list, so adding pagination means changing the response's type from an array to an
      object. Every client that parses the root as an array breaks, and the change requires a new API version.</p>
      <p>That is why it pays to wrap list responses from the first release, even when there is nothing to put beside the items
      yet. The cost is one extra level of nesting; the alternative is a versioning exercise the first time the list gets large
      enough to need paging — which is exactly when many clients already depend on it.</p>
      <p>A consistent envelope has a second benefit: every list endpoint in the API has the same shape, so clients write
      <strong>one</strong> pagination helper instead of one per endpoint. Keep the same discipline for single resources
      without over-doing it: returning the resource object directly is fine, because an object can already gain
      fields.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> Explain the difference between offset and keyset pagination and when to use each.</summary>
      <p><strong>Offset pagination</strong> skips a number of rows: <code>?page=3&amp;pageSize=20</code> becomes
      <code>ORDER BY Id OFFSET 40 ROWS FETCH NEXT 20 ROWS ONLY</code>. <strong>Keyset pagination</strong> — also called seek or
      cursor pagination — continues from the last row seen, using the sort key:</p>
      <pre>  -- offset: the database reads and discards 100,000 rows to return 20
  SELECT ... ORDER BY CreatedAt DESC, Id DESC OFFSET 100000 ROWS FETCH NEXT 20 ROWS ONLY;

  -- keyset: an index seek straight to the starting point
  SELECT ... WHERE (CreatedAt &lt; @lastCreatedAt)
               OR (CreatedAt = @lastCreatedAt AND Id &lt; @lastId)
  ORDER BY CreatedAt DESC, Id DESC FETCH NEXT 20 ROWS ONLY;</pre>
      <p>Offset has two problems. <strong>Cost grows with depth</strong>: the database still reads every skipped row, so page
      5,000 is far slower than page 1. And it is <strong>unstable under change</strong>: if a row is inserted or deleted
      before the current position while a client is paging, every later row shifts, so the client sees duplicates or skips
      items entirely.</p>
      <p>Keyset fixes both. With an index on the sort columns, every page costs the same, and inserts elsewhere cannot shift
      the position because it is defined by values, not by a count. Its limits: no jumping to an arbitrary page number,
      a total count needs a separate query, and it needs a <strong>unique, deterministic sort key</strong> — hence the
      <code>Id</code> tie-breaker. The last row's values are usually encoded into an <strong>opaque cursor</strong> so clients
      cannot depend on the scheme.</p>
      <p>Use offset for small, bounded tables and admin screens that genuinely need page numbers. Use keyset for large or
      fast-changing data: feeds, infinite scroll, public APIs, and anything a client might iterate to the end, such as a sync
      or an export.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> How do you prevent lost updates in a REST API?</summary>
      <p>A <strong>lost update</strong> happens when two clients read the same version of a resource, both modify it, and the
      second save silently overwrites the first. Neither client sees an error; one user's change simply disappears.</p>
      <p>The standard HTTP answer is <strong>optimistic concurrency with ETags</strong>. The server includes a version
      identifier with every read, and the client must send it back on every write:</p>
      <pre>  GET /orders/42
  → 200 OK   ETag: "AAAAAAAAB9E="

  PUT /orders/42    If-Match: "AAAAAAAAB9E="
  → 200 OK   ETag: "AAAAAAAAB+A="          the version matched; the save succeeded
  → 412 Precondition Failed               someone else saved first

  PUT /orders/42    (no If-Match)
  → 428 Precondition Required             the API refuses unconditional writes</pre>
      <p>On a <strong>412</strong>, the client reloads the current version and either re-applies its change or shows the user
      the conflict. Returning <strong>428</strong> when <code>If-Match</code> is missing is what makes the protection real:
      without it, any client that forgets the header silently gets last-write-wins behaviour.</p>
      <p>In ASP.NET Core with EF Core, the ETag is typically derived from a <code>rowversion</code> concurrency token. The
      handler sets the token's original value from <code>If-Match</code>, and a
      <code>DbUpdateConcurrencyException</code> maps to 412. The check is then enforced by the database's
      <code>WHERE</code> clause, so it cannot race.</p>
      <p>Other techniques narrow the problem rather than solve it. <code>PATCH</code> with only the changed fields reduces
      collisions but still loses updates to the same field. <strong>Atomic operations</strong> — "increment stock by one"
      rather than "set stock to 41" — avoid the read-modify-write cycle entirely where the domain allows. Last-write-wins is
      acceptable only when it is a deliberate choice.</p></details>''',
}, mistakes='''      <tr><td>Returning 200 with an error in the body</td><td>Clients, proxies and monitoring count failures as successes</td><td>Real status codes with problem details</td></tr>
      <tr><td>Keyset pagination on a non-unique sort key</td><td>Rows sharing a value are skipped or repeated between pages</td><td>Add a unique tie-breaker such as <code>Id</code></td></tr>
      <tr><td>Weak ETags with <code>If-Match</code></td><td><code>If-Match</code> uses strong comparison, so weak ETags never match</td><td>Strong ETags derived from a <code>rowversion</code></td></tr>
      <tr><td>Exposing raw key values as cursors</td><td>Clients construct cursors and couple to the schema</td><td>Opaque, encoded cursors</td></tr>''',
takeaways='''      <li>Idempotency is about the resulting server state, not identical responses — a repeated DELETE may 404 and still be idempotent.</li>
      <li>Retries happen at every layer (clients, proxies, resilience handlers), so design every write for being received twice.</li>
      <li>Keyset pagination needs a unique, indexed sort key; add the primary key as a tie-breaker.</li>
      <li>Keep cursors opaque so the pagination scheme can change without breaking clients.</li>
      <li>Offset pagination remains the right choice for small, bounded data that genuinely needs page numbers.</li>
      <li><code>If-Match</code> requires strong ETags; derive them from a database version such as a <code>rowversion</code>.</li>''')

apply("tutorials/aspnet/authn-authz.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What is the difference between authentication and authorization?</summary>
      <p><strong>Authentication</strong> answers <em>who is calling?</em> It verifies a credential — a cookie, a bearer
      token, a client certificate — and produces an identity. In ASP.NET Core, an authentication <strong>scheme</strong>
      validates the credential and populates <code>HttpContext.User</code> with a <code>ClaimsPrincipal</code>.</p>
      <p><strong>Authorization</strong> answers <em>may this caller do this?</em> It evaluates that principal against
      policies — roles, claims, scopes, or rules about a specific resource — and allows or refuses the request.</p>
      <pre>  app.UseAuthentication();   // who is calling? builds HttpContext.User
  app.UseAuthorization();    // may they? evaluates [Authorize] and policies

  401 Unauthorized  no valid identity: "authenticate, then try again"   (challenge)
  403 Forbidden     identity known, permission missing: "you may not"   (forbid)</pre>
      <p>The two map onto different failure responses. A missing or invalid credential gets a <strong>401</strong> — a
      <em>challenge</em>, telling the client to authenticate; for a cookie scheme that is a redirect to a login page, for a
      JWT scheme a <code>WWW-Authenticate</code> header. An authenticated caller without permission gets a <strong>403</strong> —
      <em>forbid</em> — and authenticating again will not help. Despite its name, 401 "Unauthorized" really means
      unauthenticated.</p>
      <p>A detail that surprises people: authentication <strong>does not reject anonymous requests</strong>. A request with no
      credential passes through authentication with an empty principal, and it is authorization — an <code>[Authorize]</code>
      attribute or a fallback policy — that turns it away. That is why the order of the middleware matters, and why an
      endpoint with no authorization metadata is public even when authentication is configured.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> Why are JWT access tokens short-lived?</summary>
      <p>Because a JWT is <strong>self-contained</strong>. An API validates it by checking its signature and expiry, without
      contacting the issuer or a database. That is its great strength — cheap, stateless validation in every service — and
      also its weakness: there is <strong>no central place to revoke it</strong>. A token that has been issued stays valid
      until it expires.</p>
      <p>So the lifetime <em>is</em> the exposure window. If an access token is stolen — from a log file, a compromised
      browser extension, a leaked HTTP trace — the attacker can use it until its <code>exp</code>. A 24-hour token means a
      day of access; a 10-minute token means ten minutes.</p>
      <p>There is a second reason: <strong>claims are a snapshot</strong>. Roles and permissions are written into the token
      when it is issued. A user who is demoted, disabled or removed from a tenant keeps the old permissions until the token
      expires, so a short lifetime also bounds how long stale authorisation data can be used.</p>
      <p>Short lifetimes would force users to log in constantly, so they are paired with <strong>refresh tokens</strong>:
      long-lived, stored server-side, revocable, and exchanged for a fresh access token. Revoking the refresh token ends the
      session within one access-token lifetime.</p>
      <p>The trade-off is traffic to the token endpoint, which is why lifetimes of five to fifteen minutes are common. Remember
      the default <code>ClockSkew</code> of five minutes extends the effective lifetime. When immediate revocation is a hard
      requirement, the options reintroduce state: a deny-list checked on every request, or opaque reference tokens validated
      by introspection.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> When would you choose cookies over JWTs?</summary>
      <p>The comparison is slightly misframed: a cookie is a <strong>transport</strong> — where the credential lives and how
      it is sent — while a JWT is a <strong>format</strong>. A JWT can travel in a cookie. The real question is whether the
      browser holds a credential that JavaScript can read, or one the browser sends automatically and scripts cannot
      touch.</p>
      <p>Choose <strong>cookies</strong> for <strong>browser applications talking to their own backend</strong>: server-rendered
      apps, and single-page apps served from the same site. An <code>HttpOnly</code>, <code>Secure</code>,
      <code>SameSite</code> cookie cannot be read by JavaScript, so an XSS bug cannot steal the session and send it elsewhere.
      The browser sends it automatically, and a server-side session can be revoked instantly. The cost is
      <strong>CSRF</strong>: because the browser attaches the cookie automatically, you need <code>SameSite</code> and, for
      state-changing requests, antiforgery tokens.</p>
      <p>Choose <strong>bearer JWTs</strong> for <strong>non-browser clients and service-to-service calls</strong>: mobile apps,
      command-line tools, third-party integrations, and microservices that each validate tokens independently. Bearer tokens
      are not sent automatically, so CSRF does not apply — but in a browser, a token stored where JavaScript can read it is
      exposed to any XSS.</p>
      <pre>  Browser ──HttpOnly cookie──▶ BFF ──bearer JWT──▶ Orders API
                                    └──bearer JWT──▶ Billing API</pre>
      <p>For SPAs that call APIs, the recommended pattern combines both: a <strong>backend-for-frontend</strong> holds the
      tokens server-side and gives the browser only a session cookie. The browser gets cookie security; the APIs get bearer
      tokens.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> What does refresh-token rotation with reuse detection protect against?</summary>
      <p>It protects against a <strong>stolen refresh token being used indefinitely</strong>. A refresh token is long-lived and
      can mint new access tokens, so without further protection, stealing one — from a compromised device, a leaked log, an
      XSS attack on an app that stores it in the browser — gives an attacker a session that lasts as long as the token.</p>
      <p><strong>Rotation</strong> means every use of a refresh token returns a <strong>new</strong> refresh token and
      invalidates the old one. <strong>Reuse detection</strong> means that if an already-used token is ever presented again,
      the server treats it as proof of theft — two parties hold the same token — and <strong>revokes the whole token
      family</strong>:</p>
      <pre>  RT1 → refresh → AT2 + RT2        RT1 marked used
  RT2 → refresh → AT3 + RT3        RT2 marked used
  RT1 presented again              reuse detected → revoke RT1..RT3 → sign in again</pre>
      <p>Whoever uses the stolen token second triggers detection. If the attacker refreshes first, the legitimate user's next
      refresh presents a used token and the family is revoked, killing the attacker's copy too. If the user refreshes first,
      the attacker's attempt is detected. Either way, the theft window shrinks to at most one rotation.</p>
      <p>Making it work in production takes care. Store tokens <strong>hashed</strong>, record a family identifier, and make
      the check-and-rotate <strong>atomic</strong>, or two concurrent requests can both succeed. Legitimate concurrency — two
      browser tabs refreshing at once — can look like reuse, so allow a short grace period or single-flight refreshes in the
      client.</p>
      <p>What it does not protect against is a stolen <em>access</em> token, which remains valid until it expires — the reason
      those stay short-lived.</p></details>''',
}, mistakes='''      <tr><td>403 for a missing credential, or 401 for a missing permission</td><td>Clients cannot tell "sign in" from "you may not"</td><td>401 to challenge, 403 to forbid</td></tr>
      <tr><td>Decoding a JWT without validating it</td><td>Forged or expired tokens are trusted</td><td>Let the JWT bearer handler validate signature, issuer, audience and lifetime</td></tr>
      <tr><td>Not restricting accepted signing algorithms</td><td>Algorithm confusion can bypass the signature check</td><td>Set <code>ValidAlgorithms</code> explicitly</td></tr>
      <tr><td>Reuse detection with no allowance for concurrent refreshes</td><td>Two tabs refreshing at once log the user out</td><td>A short grace period or single-flight refresh</td></tr>''',
takeaways='''      <li>Authentication establishes who is calling; authorization decides what that caller may do.</li>
      <li>401 is a challenge to authenticate; 403 refuses a caller whose identity is already known.</li>
      <li>Anonymous requests pass through authentication unchanged — authorization is what rejects them.</li>
      <li>Claims in a token are a snapshot from the moment of issue, so short lifetimes also bound stale permissions.</li>
      <li>Cookie versus JWT is a question of where the credential lives and who can read it; a JWT can travel in a cookie.</li>
      <li>A rotated refresh token presented twice proves theft, so revoke the whole family, atomically.</li>''')

apply("tutorials/aspnet/authorization.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What is the difference between role-based and policy-based authorization?</summary>
      <p><strong>Role-based</strong> authorization checks whether the user holds a named role:
      <code>[Authorize(Roles = "Admin,Manager")]</code>. It is simple, but it couples every endpoint to your organisation
      chart. When the rules change — support staff may now issue refunds under £50 — you have to find and edit every endpoint
      that lists roles, and a typo in a role string fails silently.</p>
      <p><strong>Policy-based</strong> authorization has the endpoint name the <strong>capability</strong> it needs, and defines
      what satisfies that capability in one place:</p>
      <pre>  builder.Services.AddAuthorizationBuilder()
      .AddPolicy("CanRefundOrders", p =&gt; p
          .RequireAuthenticatedUser()
          .RequireRole("Admin", "Support")
          .AddRequirements(new MaxRefundRequirement(50m)));

  [Authorize(Policy = "CanRefundOrders")]
  public IActionResult Refund(int id) { ... }</pre>
      <p>A policy is a set of <strong>requirements</strong>, and each requirement is checked by one or more
      <strong>handlers</strong>. Requirements can express anything: roles, claims, OAuth scopes, a minimum account age,
      membership of the right tenant, or rules that need a database. Handlers are plain classes, so they can be unit tested
      and injected with services.</p>
      <p>The key insight is that the two are not rivals: roles are simply <strong>one input to a policy</strong>. In fact,
      ASP.NET Core implements <code>Roles = "..."</code> as a policy requirement internally. The benefit of policies is the
      indirection: the endpoint states <em>what</em> it needs, the policy states <em>who</em> qualifies, and changing the
      rule is a single, reviewable edit.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> What does a fallback policy do?</summary>
      <p>The fallback policy applies to every endpoint that has <strong>no authorization metadata at all</strong> — no
      <code>[Authorize]</code>, no <code>RequireAuthorization()</code>, and no <code>[AllowAnonymous]</code>. Without one,
      such endpoints are <strong>public</strong>. Setting it makes the application <strong>secure by default</strong>:</p>
      <pre>  builder.Services.AddAuthorizationBuilder()
      .SetFallbackPolicy(new AuthorizationPolicyBuilder()
          .RequireAuthenticatedUser()
          .Build());

  app.MapGet("/health", () =&gt; "ok").AllowAnonymous();      // public by explicit choice
  app.MapPost("/login", Login).AllowAnonymous();</pre>
      <p>The benefit is about failure modes. Without a fallback, forgetting <code>[Authorize]</code> on a new endpoint exposes
      it to the internet, and nothing warns you. With a fallback, forgetting an attribute leaves the endpoint requiring an
      authenticated user; the failure is a 401 found in testing, not a data leak found by an attacker. Being public becomes
      an <strong>explicit, greppable decision</strong> — every <code>AllowAnonymous</code> is visible in code review.</p>
      <p>It is distinct from the <strong>default policy</strong>, which is what a bare <code>[Authorize]</code> with no policy
      name uses. The default policy applies to endpoints that asked for authorization; the fallback applies to endpoints that
      did not ask at all.</p>
      <p>Two practical cautions. Health probes, login and other genuinely public endpoints must be marked
      <code>AllowAnonymous</code>, or orchestrator probes start failing. And the fallback only covers requests that reach
      the authorization middleware — static files served by middleware registered <em>before</em>
      <code>UseAuthorization</code> are not protected by it.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> In a custom handler, when should you call <code>context.Fail()</code>?</summary>
      <p>A handler has three possible outcomes, and they compose differently:</p>
      <pre>  context.Succeed(requirement);   // "yes" — satisfies the requirement
  return Task.CompletedTask;      // "no opinion" — other handlers may still succeed
  context.Fail();                 // "veto" — the requirement fails whatever others say</pre>
      <p>Handlers for the same requirement combine as a logical <strong>OR</strong>: if any handler succeeds, the
      requirement is met. That is what lets you register an <code>IsOwnerHandler</code> and an <code>IsAdminHandler</code> for
      an <code>EditOrder</code> requirement and have either grant access.</p>
      <p><code>context.Fail()</code> breaks that composition on purpose: it makes the requirement fail <strong>even if another
      handler succeeds</strong>. So call it only for a <strong>definitive, overriding denial</strong> — a condition that must
      block access no matter what else is true: the account is suspended, the token has been revoked, the user is
      impersonating someone and the operation is forbidden during impersonation, or the request comes from a blocked
      network.</p>
      <p>The common mistake is calling <code>Fail()</code> when a handler merely <strong>cannot judge</strong> — for example,
      the owner handler finds no user-id claim. Returning without succeeding is the right response there: it says "not
      through me", and leaves the admin handler free to grant access. Calling <code>Fail()</code> instead vetoes the admin
      too, producing baffling 403s for users who should be allowed.</p>
      <p>Rule of thumb: <code>Succeed</code> when you can grant, return silently when you cannot, and reserve
      <code>Fail</code> for facts that must win over every other rule. Log the reason when you do, because a veto is
      otherwise invisible in the resulting 403.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> Why can't an attribute policy express "the user may edit this specific order"?</summary>
      <p>Because attribute policies run <strong>before the action</strong>, and at that point the order has not been loaded.
      The authorization middleware sees the user and the route values — perhaps <code>id = 42</code> — but not the
      <code>Order</code> entity with its owner, tenant and status. A rule like "only the customer who placed the order, and
      only while it is still pending" depends on data that does not exist yet.</p>
      <p>The answer is <strong>resource-based authorization</strong>: load the resource first, then ask the authorization
      service imperatively, passing the resource:</p>
      <pre>  public async Task&lt;IResult&gt; Edit(int id, EditOrder dto, IAuthorizationService auth,
                                  ClaimsPrincipal user, ShopContext db)
  {
      var order = await db.Orders.FindAsync(id);
      if (order is null) return Results.NotFound();

      var result = await auth.AuthorizeAsync(user, order, "EditOrder");
      if (!result.Succeeded) return Results.NotFound();       // or Forbid()

      order.Apply(dto);
      await db.SaveChangesAsync();
      return Results.NoContent();
  }

  public class EditOrderHandler : AuthorizationHandler&lt;EditOrderRequirement, Order&gt;
  {
      protected override Task HandleRequirementAsync(AuthorizationHandlerContext ctx,
          EditOrderRequirement req, Order order)
      {
          if (order.CustomerId == ctx.User.FindFirstValue("sub") &amp;&amp; order.IsPending)
              ctx.Succeed(req);
          return Task.CompletedTask;
      }
  }</pre>
      <p>The rule still lives in a handler — central and unit-testable — but is invoked at the point where the resource is
      available. The endpoint keeps a coarse attribute policy, such as "authenticated customer", and the resource check
      adds the fine-grained decision.</p>
      <p>Whether a refusal returns 403 or 404 is a deliberate choice: 404 avoids confirming that order 42 exists. And resource
      checks are not the only guard — list queries must also be filtered by owner or tenant.</p></details>''',
}, mistakes='''      <tr><td>A fallback policy without <code>AllowAnonymous</code> on probes and login</td><td>Health checks fail and nobody can sign in</td><td>Mark genuinely public endpoints explicitly</td></tr>
      <tr><td>Setting the default policy and expecting unannotated endpoints to be protected</td><td>The default only applies to a bare <code>[Authorize]</code></td><td>Set the fallback policy</td></tr>
      <tr><td>Singleton handlers that depend on scoped services</td><td>Captive <code>DbContext</code> shared across requests</td><td>Register such handlers as scoped</td></tr>
      <tr><td>Database lookups repeated in several handlers per request</td><td>Authorization multiplies query load</td><td>Load once per request and reuse</td></tr>''',
takeaways='''      <li>Roles are one input to a policy, not an alternative to policies — ASP.NET Core implements roles as a requirement.</li>
      <li>The fallback policy covers endpoints with no authorization metadata at all; the default policy covers a bare <code>[Authorize]</code>.</li>
      <li>Under a fallback policy, health probes and login need an explicit <code>AllowAnonymous</code>.</li>
      <li>Handlers for one requirement combine as OR; <code>Fail()</code> overrides every other handler's success.</li>
      <li>Resource-based checks run after the resource is loaded, through <code>IAuthorizationService.AuthorizeAsync</code>.</li>
      <li>Register authorization handlers with a lifetime that matches their dependencies.</li>''')

apply("tutorials/aspnet/caching-background.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What is the difference between <code>IHostedService</code> and <code>BackgroundService</code>?</summary>
      <p><code>IHostedService</code> is the underlying interface: two methods, <code>StartAsync</code> and
      <code>StopAsync</code>, which the host calls at startup and shutdown. The host <strong>awaits</strong> each service's
      <code>StartAsync</code> before the application starts serving requests, so whatever it does delays startup.</p>
      <p><code>BackgroundService</code> is an abstract base class that implements <code>IHostedService</code> for the most
      common case: a <strong>long-running loop</strong>. You override one method, <code>ExecuteAsync</code>. Its
      <code>StartAsync</code> calls <code>ExecuteAsync</code> and returns as soon as that method yields at its first real
      <code>await</code>, so the loop runs in the background while the app starts. Its <code>StopAsync</code> cancels the
      <code>stoppingToken</code> and waits for the loop to finish.</p>
      <pre>  // short startup/shutdown hook: IHostedService
  public class WarmCache(ICatalog catalog) : IHostedService
  {
      public Task StartAsync(CancellationToken ct) =&gt; catalog.PreloadAsync(ct);  // brief, awaited
      public Task StopAsync(CancellationToken ct) =&gt; Task.CompletedTask;
  }

  // continuous work: BackgroundService
  public class QueueWorker : BackgroundService
  {
      protected override async Task ExecuteAsync(CancellationToken stoppingToken)
      {
          await foreach (var job in _queue.ReadAllAsync(stoppingToken)) await HandleAsync(job);
      }
  }</pre>
      <p>So use <code>IHostedService</code> directly for <strong>short, bounded</strong> work that should happen at startup or
      shutdown — warming a cache, registering with a discovery service, flushing buffers on stop. Use
      <code>BackgroundService</code> for <strong>continuous</strong> work: queue consumers, polling, scheduled jobs.</p>
      <p>One subtlety: code in <code>ExecuteAsync</code> before its first asynchronous <code>await</code> runs synchronously
      during startup, so a slow synchronous preamble still blocks the host. .NET 8 adds
      <code>IHostedLifecycleService</code> for finer hooks such as <code>StartingAsync</code> and
      <code>StoppedAsync</code>.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> Why can't a <code>BackgroundService</code> inject a <code>DbContext</code>?</summary>
      <p>Because of a <strong>lifetime mismatch</strong>. Hosted services, including every <code>BackgroundService</code>, are
      registered as <strong>singletons</strong>: one instance lives for the whole life of the application. A
      <code>DbContext</code> is registered as <strong>scoped</strong>: one instance per request, disposed when the request
      ends.</p>
      <p>Injecting a scoped service into a singleton's constructor is a <strong>captive dependency</strong>. If it were allowed,
      the worker would hold one <code>DbContext</code> forever: its change tracker would grow without limit, it would return
      stale cached entities instead of current data, and one failed save would leave pending changes that the next unit of
      work commits. In Development, where scope validation is on by default, the host refuses to start with "Cannot consume
      scoped service from singleton".</p>
      <p>There is also simply <strong>no scope</strong> to take it from. In a web request, ASP.NET Core creates a scope per
      request. A background loop has no request, so nothing creates one. The worker has to create its own, one per unit of
      work:</p>
      <pre>  public class OutboxPublisher(IServiceScopeFactory scopes) : BackgroundService
  {
      protected override async Task ExecuteAsync(CancellationToken stoppingToken)
      {
          using var timer = new PeriodicTimer(TimeSpan.FromSeconds(5));
          while (await timer.WaitForNextTickAsync(stoppingToken))
          {
              await using var scope = scopes.CreateAsyncScope();
              var db = scope.ServiceProvider.GetRequiredService&lt;ShopContext&gt;();
              await PublishPendingAsync(db, stoppingToken);
          }                                           // scope and context disposed each tick
      }
  }</pre>
      <p>Each iteration gets a fresh context with an empty change tracker and current data, and the scope disposes it. The
      scope must be created <strong>inside</strong> the loop; creating it once outside recreates the captive dependency by
      hand. Singleton dependencies, such as a logger, can still be injected directly.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> Why is <code>PeriodicTimer</code> preferable to <code>await Task.Delay</code> in a loop?</summary>
      <p>A loop of "do the work, then delay" does not run on an interval; it runs on <strong>interval plus work time</strong>,
      and the schedule drifts. A job meant to run every minute that takes 20 seconds actually runs every 80 seconds, and the
      timing wanders further whenever the work is slow.</p>
      <pre>  // drifts: period = work time + 60s
  while (!ct.IsCancellationRequested)
  {
      await DoWorkAsync(ct);
      await Task.Delay(TimeSpan.FromMinutes(1), ct);
  }

  // fixed cadence: ticks every 60s regardless of work time
  using var timer = new PeriodicTimer(TimeSpan.FromMinutes(1));
  while (await timer.WaitForNextTickAsync(ct))
      await DoWorkAsync(ct);</pre>
      <p><code>PeriodicTimer</code> ticks on a <strong>fixed cadence</strong>. <code>WaitForNextTickAsync</code> completes at
      each tick, so the period is independent of how long the work takes.</p>
      <p>Its behaviour when work <strong>overruns</strong> is the other key property: if the work takes longer than the period,
      missed ticks are <strong>coalesced</strong> into one, so the next wait completes immediately once, rather than
      triggering a burst of catch-up runs. Because the loop awaits the work before waiting again, runs <strong>never
      overlap</strong> — unlike <code>System.Threading.Timer</code>, whose callbacks can fire concurrently and which, with an
      async callback, becomes an <code>async void</code> method whose exceptions cannot be caught.</p>
      <p>It also integrates cleanly with cancellation: passing the stopping token ends the wait immediately at shutdown, and
      <code>WaitForNextTickAsync</code> returns false once the timer is disposed.</p>
      <p>Its limit is that it is <strong>interval-based</strong>. "Every day at 02:00" is a wall-clock schedule, and an
      interval restarts from whenever the process started. For those, compute the delay to the next occurrence, or use a
      scheduler such as Quartz.NET or Hangfire.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> What happens to fire-and-forget <code>Task.Run</code> work started from a request?</summary>
      <p>It runs on the thread pool <strong>detached from everything that made the request safe</strong>, and several things go
      wrong.</p>
      <pre>  app.MapPost("/orders", async (Order o, ShopContext db, IEmailSender email) =&gt;
  {
      db.Orders.Add(o);
      await db.SaveChangesAsync();
      _ = Task.Run(() =&gt; email.SendConfirmationAsync(o, db));    // fire and forget
      return Results.Accepted();
  });</pre>
      <p><strong>Its scope is gone.</strong> The <code>DbContext</code> and other scoped services belong to the request scope,
      which is disposed as soon as the response is sent. The background work then touches a disposed context and throws
      <code>ObjectDisposedException</code> — sometimes, depending on timing. <code>HttpContext</code> is likewise invalid after
      the request ends and was never thread-safe.</p>
      <p><strong>Its exceptions vanish.</strong> Nothing awaits the task, so a failure is unobserved: no log, no retry, no
      alert. Customers simply stop receiving emails.</p>
      <p><strong>The host does not know it exists.</strong> On shutdown or deploy, the host drains requests and stops hosted
      services, but it has no idea this task is running, so it is killed mid-flight.</p>
      <p><strong>There is no back-pressure.</strong> A traffic spike starts unbounded background work competing with
      requests for the same thread pool.</p>
      <p>The fix is to <strong>hand the work to something that owns it</strong>. For work that can be lost on a crash, write a
      work item — copying the values it needs, not the context — to a <strong>bounded <code>Channel</code></strong> consumed
      by a <code>BackgroundService</code> that creates a scope per item. For work that must survive restarts, use a durable
      queue or an outbox table written in the same transaction as the order.</p></details>''',
}, mistakes='''      <tr><td>No per-item error handling in a channel consumer</td><td>One bad message stops the consumer for good</td><td>Try/catch per item, with a dead-letter path</td></tr>
      <tr><td>Capturing <code>HttpContext</code> in background work</td><td>Invalid after the request ends, and not thread-safe</td><td>Copy the values the work needs into the work item</td></tr>
      <tr><td><code>PeriodicTimer</code> for wall-clock schedules</td><td>Runs drift from the clock and reset on restart</td><td>Compute the next occurrence, or use a scheduler</td></tr>''',
takeaways='''      <li>Implement <code>IHostedService</code> directly only for short, bounded startup and shutdown hooks.</li>
      <li>Code in <code>ExecuteAsync</code> before its first real await still runs during startup.</li>
      <li>Hosted services are singletons with no request scope — create the scope yourself, inside the loop.</li>
      <li><code>PeriodicTimer</code> keeps a fixed cadence, coalesces missed ticks and never overlaps runs.</li>
      <li>Interval timers are not calendars; wall-clock schedules need a next-occurrence calculation or a scheduler.</li>
      <li>Never capture <code>HttpContext</code> or scoped services in background work — pass plain values.</li>''')
