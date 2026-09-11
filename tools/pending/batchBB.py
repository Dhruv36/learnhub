# -*- coding: utf-8 -*-
"""aspnet batch 2: caching, clean-architecture, configuration, controllers-mvc."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import apply

apply("tutorials/aspnet/caching.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What is the difference between in-memory and distributed caching?</summary>
      <p><strong>In-memory caching</strong> (<code>IMemoryCache</code>) stores objects inside the application process. It is
      the <strong>fastest</strong> option: no network hop and no serialisation — the cache hands back the same object
      reference. But each instance of the app has <strong>its own cache</strong>. With four replicas, the same data is cached
      four times, the copies can disagree, and every deploy or restart starts cold.</p>
      <p><strong>Distributed caching</strong> (<code>IDistributedCache</code>, usually backed by Redis) stores serialised values
      in a <strong>shared</strong> external store. Every replica sees the same data, an eviction takes effect everywhere at
      once, and the cache survives deploys. The costs are a network round trip and serialisation on every read, and a new
      dependency that can fail or slow down.</p>
      <pre>  IMemoryCache       ~nanoseconds   per instance   object references   lost on restart
  IDistributedCache  ~milliseconds   shared         serialised bytes    survives deploys
  HybridCache        L1 in-memory + L2 distributed, with stampede protection (.NET 9)</pre>
      <p>Choose in-memory for small, read-heavy data where brief inconsistency between instances is acceptable: reference data,
      feature configuration, lookup tables. Choose distributed when <strong>consistency across instances</strong> matters —
      invalidation must be seen everywhere — or when the data is expensive enough that losing it on every deploy hurts.</p>
      <p><strong><code>HybridCache</code></strong> combines them: a fast local tier backed by a shared tier, with protection
      against stampedes. One caution for in-memory caching specifically: because it returns shared references,
      <strong>mutating a cached object changes it for every request</strong>. Cache immutable objects, or copies.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> Why must a cache key include the user for personalised responses?</summary>
      <p>Because the cache key must identify <strong>everything that makes the response different</strong>. If a response
      depends on who is asking, and the key does not include the user, the first user's response is stored under a key that
      every other user's request also produces. The second user receives the first user's data.</p>
      <pre>  // wrong: every user's "my orders" page shares one entry
  cache.GetOrCreateAsync("orders:recent", ...);

  // right: the key includes every input that varies the result
  cache.GetOrCreateAsync($"orders:recent:{tenantId}:{userId}:{page}", ...);</pre>
      <p>This is not a performance bug; it is a <strong>data leak</strong>. One customer sees another's orders, addresses or
      account balance. It is a security incident, often a reportable data-protection breach, and it tends to appear only under
      real concurrent traffic, never in a developer's single-user testing.</p>
      <p>The same principle applies at every caching layer. For in-process and distributed caches, build keys from
      <strong>every input</strong> that shapes the result: user, tenant, role, locale, query parameters, feature flags. For
      output caching, configure what the entry varies by. For HTTP caching, personalised responses must be
      <code>Cache-Control: private</code> — or <code>no-store</code> — so that CDNs and shared proxies never store them.</p>
      <p>A better design often avoids the problem: cache the <strong>shared</strong> parts — product details, prices,
      catalogue pages — and compose the small personalised part per request. That keeps hit rates high, since a per-user key
      only helps if the same user repeats the same request, and it removes the risk of cross-user leaks for most of the
      data.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> What is a cache stampede and how do you prevent it?</summary>
      <p>A stampede — or thundering herd — happens when a <strong>hot key expires</strong> and many concurrent requests miss at
      the same moment. Every one of them runs the expensive query or calls the slow service to rebuild the same value. A
      database that comfortably served one query per minute for that data suddenly receives hundreds at once, slows down,
      and the slowdown makes more requests pile up. A cache that normally protects the database becomes the trigger for its
      overload.</p>
      <p>The main defence is <strong>request coalescing</strong>: on a miss, only one caller computes the value, and every
      concurrent caller for the same key awaits that single result.</p>
      <pre>  // HybridCache coalesces concurrent misses for the same key
  var product = await hybridCache.GetOrCreateAsync(
      $"product:{id}",
      async ct =&gt; await db.Products.AsNoTracking().FirstAsync(p =&gt; p.Id == id, ct),
      new HybridCacheEntryOptions { Expiration = TimeSpan.FromMinutes(10) });</pre>
      <p><code>HybridCache</code> does this built in. <code>IMemoryCache.GetOrCreateAsync</code> does <strong>not</strong>:
      its factory can run concurrently for the same key, so hand-rolled code needs a per-key lock or a cached
      <code>Lazy&lt;Task&lt;T&gt;&gt;</code>.</p>
      <p>Further defences address when keys expire. <strong>Jitter</strong> — adding a random few percent to each
      expiration — stops keys populated together from all expiring together. <strong>Refresh-ahead</strong> recomputes a hot
      value in the background shortly before it expires, so readers never see a miss. <strong>Serve stale while
      revalidating</strong> returns the slightly old value during the rebuild instead of blocking.</p>
      <p>Coalescing protects a single instance; with many replicas, each can still rebuild once, which is usually acceptable. If
      not, a distributed lock or a shared L2 tier reduces it further.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> When would you evict a cache entry rather than update it in place?</summary>
      <p>Evicting — deleting the key when the data changes and letting the next read repopulate it from the database — is the
      <strong>default</strong>, because it converges to correct data even when things race.</p>
      <p>Updating in place has a classic race. Two writers change the same record: writer A saves version 1, then writer B saves
      version 2, so the database correctly holds version 2. But their cache writes arrive in the opposite order — B writes
      version 2 to the cache, then A, delayed by a slow network or a garbage-collection pause, writes version 1. The cache now
      holds <strong>stale data</strong> that no future write corrects, and it is served until the TTL expires.</p>
      <pre>  DB:     A saves v1 ─── B saves v2                   database = v2  (correct)
  Cache:           B writes v2 ─── A writes v1        cache    = v1  (stale until TTL)

  Evict instead: A deletes, B deletes → the next read loads v2 from the database</pre>
      <p>Eviction avoids that because deleting is <strong>idempotent</strong>: however the deletes interleave, the result is
      the same empty key, and the next read fetches the current value. It also keeps a single code path that builds the cached
      representation, rather than duplicating it in every write.</p>
      <p>Two timing details matter. Evict <strong>after</strong> the database commit; evicting first lets a concurrent reader
      repopulate the old value before the write lands. And keep a <strong>TTL</strong> as a backstop for any race that remains.</p>
      <p>Updating in place is reasonable when there is a <strong>single writer</strong>, so no race is possible, and a miss is
      costly enough that avoiding it matters — a very hot key whose rebuild is expensive. Even then, versioned writes, which
      reject older versions, make it safer.</p></details>''',
}, mistakes='''      <tr><td>Mutating an object returned by <code>IMemoryCache</code></td><td>The change leaks to every request sharing that instance</td><td>Cache immutable objects, or copies</td></tr>
      <tr><td>The same expiration for every key</td><td>Keys populated together expire together</td><td>Add jitter to expirations</td></tr>
      <tr><td>Evicting before the database commit</td><td>A concurrent reader re-caches the old value</td><td>Evict after the commit</td></tr>
      <tr><td>Caching transient failures as values</td><td>A momentary error is served for the whole TTL</td><td>Cache only successful and deliberate negative results</td></tr>''',
takeaways='''      <li>In-memory caches are per instance and return shared references; distributed caches are shared but cost a network hop.</li>
      <li><code>HybridCache</code> combines a local L1 with a distributed L2 and coalesces concurrent misses.</li>
      <li>Never mutate an object retrieved from an in-memory cache.</li>
      <li>A missing user or tenant in a cache key is a data leak, not a performance bug.</li>
      <li>Jitter expirations so that hot keys do not all expire at the same moment.</li>
      <li>Evict after the database commits; update in place only with a single writer and an expensive miss.</li>''')

apply("tutorials/aspnet/clean-architecture.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What is the dependency rule in Clean Architecture?</summary>
      <p>The dependency rule says that <strong>source-code dependencies point inward</strong>, toward the business rules. Inner
      layers know nothing about outer layers.</p>
      <pre>  Api (endpoints, DI wiring)  ──▶  Application (use cases, interfaces)  ──▶  Domain (entities, rules)
  Infrastructure (EF Core, email, HTTP clients)  ──▶  Application
                         Domain.csproj references nothing</pre>
      <p>The <strong>Domain</strong> holds entities, value objects and invariants, and references no framework: no EF Core, no
      ASP.NET Core. The <strong>Application</strong> layer holds use cases and defines the <strong>interfaces</strong> it
      needs from the outside world — "save this order", "send this email". <strong>Infrastructure</strong> implements those
      interfaces with real technology, and the <strong>Api</strong> layer wires everything together.</p>
      <p>The crucial move is <strong>dependency inversion</strong>. The use case needs to send email, but instead of referencing
      an SMTP library, it declares an <code>IEmailSender</code> interface in the Application layer. Infrastructure
      implements it. At runtime the call goes outward; at compile time the dependency points inward.</p>
      <p>In .NET, <strong>project references enforce it</strong>: if <code>Domain.csproj</code> references nothing, a developer
      cannot accidentally use <code>DbContext</code> in an entity — it does not compile.</p>
      <p>The payoff: business rules can be tested without a database or web server; infrastructure can be replaced or upgraded
      without touching the domain; and framework churn stays at the edges. The cost is more projects, more interfaces and
      more mapping — worthwhile when the domain has real rules, and overkill for a service that is mostly CRUD.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> What does CQRS actually mean?</summary>
      <p>CQRS — Command Query Responsibility Segregation — means using <strong>different models for changing state and for
      reading it</strong>.</p>
      <p><strong>Commands</strong> change state. They go through the domain model: load an aggregate, call a method that
      enforces the invariants, save. They return little or nothing — an identifier or a success result.</p>
      <p><strong>Queries</strong> read state. They <strong>bypass the domain model</strong> entirely and project straight into
      the shape the screen or client needs, with no change tracking and no invariant logic to run.</p>
      <pre>  // command: through the aggregate, enforcing rules
  var order = await db.Orders.Include(o =&gt; o.Lines).FirstAsync(o =&gt; o.Id == id);
  order.AddLine(productId, qty);                   // invariants checked here
  await db.SaveChangesAsync();

  // query: straight to a DTO, no aggregate
  var summary = await db.Orders.AsNoTracking()
      .Where(o =&gt; o.CustomerId == customerId)
      .Select(o =&gt; new OrderSummary(o.Id, o.Total, o.Lines.Count))
      .ToListAsync();</pre>
      <p>The reason is that the two sides have opposite needs. Writes need rich behaviour and consistency; reads need speed,
      joins across aggregates and shapes that match the UI. Forcing both through one model makes the domain bloated with
      display concerns and the reads slow.</p>
      <p>What CQRS does <strong>not</strong> require is just as important: separate databases, event sourcing, eventual
      consistency or a mediator library. Those are later, optional steps. Level one — separate code paths and models over
      <strong>one database</strong> — delivers most of the benefit with none of the operational cost. Separate read stores
      synchronised by events are a response to real scale or query needs, and bring eventual consistency the UI must then
      handle.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> Do you need a repository over EF Core?</summary>
      <p>Usually not a <strong>generic</strong> one. EF Core already implements both patterns a repository is meant to
      provide: <code>DbSet&lt;T&gt;</code> is a repository — a collection-like interface over stored entities — and
      <code>DbContext</code> is a unit of work, tracking changes and committing them in one transaction.</p>
      <p>A generic <code>IRepository&lt;T&gt;</code> with <code>GetById</code>, <code>Add</code> and <code>Update</code> that
      forwards to a <code>DbSet</code> adds a layer without adding value, and it does harm. It <strong>hides EF Core's
      features</strong> — <code>Include</code>, projections, <code>AsNoTracking</code>, compiled queries — so queries get
      worse. Or it exposes <code>IQueryable</code> to avoid that, which leaks EF Core through the abstraction anyway. And it
      encourages mocking data access in unit tests, which proves nothing about the queries themselves.</p>
      <p>A repository <strong>earns its place</strong> in specific situations:</p>
      <p><strong>Aggregate repositories</strong> in a rich domain model: an <code>IOrderRepository</code> with
      <code>GetWithLinesAsync</code> guarantees that an aggregate is always loaded whole and saved as a unit, so no code can load
      half an order and break its invariants.</p>
      <p><strong>Enforcing the dependency rule</strong>: if the Application layer must not reference EF Core, it needs an
      interface to depend on.</p>
      <p><strong>Several data sources</strong> behind one abstraction.</p>
      <pre>  public interface IOrderRepository
  {
      Task&lt;Order?&gt; GetAsync(OrderId id, CancellationToken ct);   // whole aggregate, always
      void Add(Order order);
  }</pre>
      <p>Otherwise, using the <code>DbContext</code> directly in handlers, with integration tests against a real database, is
      simpler and tests more of what can actually go wrong.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> What is an aggregate boundary and why keep aggregates small?</summary>
      <p>An <strong>aggregate</strong> is a cluster of entities that is treated as a single unit for data changes, with one
      entity as its <strong>root</strong>. All changes go through the root, which enforces the invariants that span the
      cluster. The boundary is also a <strong>transaction boundary</strong>: one transaction changes one aggregate.</p>
      <p>An <code>Order</code> with its <code>OrderLine</code>s is a typical aggregate. Lines have no meaning outside their order,
      and invariants such as "no more than 50 lines" or "the total equals the sum of the lines" span them, so they are changed
      only through methods on <code>Order</code>. The <code>Customer</code> and <code>Product</code> are separate aggregates,
      referenced <strong>by identifier</strong>, and the price is copied into the line when the order is placed.</p>
      <pre>  public class Order                        // aggregate root
  {
      private readonly List&lt;OrderLine&gt; _lines = [];
      public CustomerId CustomerId { get; private set; }     // reference by id
      public void AddLine(ProductId product, Money price, int qty)
      {
          if (_lines.Count &gt;= 50) throw new DomainException("Too many lines");
          _lines.Add(new OrderLine(product, price, qty));
      }
  }</pre>
      <p>Aggregates should be small for concrete reasons. <strong>Concurrency</strong>: an aggregate has one version, so every
      change conflicts with every other change to it; a <code>Customer</code> aggregate containing all of its orders makes
      two unrelated orders collide. <strong>Performance</strong>: the whole aggregate is loaded for every change.
      <strong>Clarity</strong>: large aggregates accumulate unrelated rules.</p>
      <p>The design rule is to draw the boundary around invariants that must hold <strong>immediately</strong>. Anything that
      can be consistent a moment later — updating a customer's loyalty points when an order ships — belongs in another
      aggregate, updated through a domain event.</p></details>''',
}, mistakes='''      <tr><td>Anaemic entities with all rules in handlers</td><td>Invariants are duplicated and easily bypassed</td><td>Put behaviour on the entities</td></tr>
      <tr><td>Mapping between identical models at every layer</td><td>Boilerplate with no isolation benefit</td><td>Map only where shapes genuinely differ</td></tr>
      <tr><td>Application layer referencing Infrastructure</td><td>The dependency rule is broken and cycles appear</td><td>Interfaces in Application, implementations in Infrastructure</td></tr>
      <tr><td>Changing several aggregates in one transaction</td><td>Lock contention and hidden coupling</td><td>One aggregate per transaction; events for the rest</td></tr>''',
takeaways='''      <li>Inner layers declare the interfaces they need; outer layers implement them.</li>
      <li>Project references make the dependency rule a compiler error rather than a guideline.</li>
      <li>CQRS means separate models for writes and reads — not separate databases, event sourcing or a mediator.</li>
      <li><code>DbContext</code> is already a unit of work and <code>DbSet</code> already a repository.</li>
      <li>An aggregate is a consistency and transaction boundary with a single root.</li>
      <li>Draw aggregate boundaries around invariants that must hold immediately; everything else can be eventual.</li>''')

apply("tutorials/aspnet/configuration.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What is the precedence order of the default configuration providers?</summary>
      <p><code>WebApplication.CreateBuilder</code> registers configuration providers in a fixed order, and <strong>later
      providers override earlier ones</strong>:</p>
      <pre>  1. appsettings.json                     defaults, committed to source control
  2. appsettings.{Environment}.json       per-environment overrides, committed
  3. User secrets                         Development only, stored outside the repo
  4. Environment variables                set by the deployment platform
  5. Command-line arguments               ad hoc overrides, highest priority</pre>
      <p>The order reflects where values should come from. Safe defaults live in the repository; environment-specific
      differences are committed alongside them; developers' secrets stay on their own machine; the deployment platform
      injects real settings and secrets through environment variables; and a command-line argument can override anything for
      a one-off run. Providers added afterwards — Azure Key Vault, AWS parameter store — override all of these unless you add
      them earlier.</p>
      <p>Two details trip people up. The merge happens <strong>per key</strong>, not per file: an environment variable that sets
      <code>Smtp:Host</code> replaces only that one value, and every other <code>Smtp</code> setting still comes from JSON.
      And <strong>arrays merge by index</strong>, so overriding a three-element list with a two-element one leaves the third
      element in place.</p>
      <p>When a value is not what you expect, <code>((IConfigurationRoot)config).GetDebugView()</code> lists every key and the
      provider that supplied it. It is invaluable for diagnosing precedence problems — and must never be logged in production,
      because it prints secrets too.</p>
      <p>Finally, the <strong>environment name</strong> itself — from <code>ASPNETCORE_ENVIRONMENT</code> or
      <code>DOTNET_ENVIRONMENT</code> — decides which environment file loads, and it defaults to <code>Production</code> when
      unset.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> Why do environment variables use a double underscore?</summary>
      <p>Configuration keys are <strong>hierarchical</strong>, and .NET separates the levels with a colon:
      <code>Smtp:Host</code> is the <code>Host</code> key inside the <code>Smtp</code> section, which binds to a nested options
      class. But a colon is <strong>not a valid character</strong> in environment variable names in most Linux shells, and many
      tools, container platforms and CI systems reject or mangle it.</p>
      <p>So the environment variables provider accepts <strong><code>__</code></strong> — a double underscore — as the section
      separator and translates it into a colon:</p>
      <pre>  Smtp__Host=mail.internal              →  Smtp:Host
  ConnectionStrings__Main=Host=db;...   →  ConnectionStrings:Main
  AllowedOrigins__0=https://a.example   →  AllowedOrigins:0     (array element)
  Smtp_Host=mail.internal               →  "Smtp_Host" — a different key, silently unused</pre>
      <p>A <strong>single</strong> underscore is just a character in the key name. <code>Smtp_Host</code> becomes a top-level key
      called <code>Smtp_Host</code>, which nothing binds to. There is no error: the application quietly keeps using the value
      from <code>appsettings.json</code>, which is why this mistake survives until someone wonders why the production setting
      never took effect.</p>
      <p>Two related details: array elements are addressed by index — <code>__0</code>, <code>__1</code> — and a prefix can be
      stripped with <code>AddEnvironmentVariables("MYAPP_")</code>, so <code>MYAPP_Smtp__Host</code> becomes
      <code>Smtp:Host</code>. Variables prefixed <code>ASPNETCORE_</code> and <code>DOTNET_</code> are read as host
      configuration. Checking <code>GetDebugView()</code> in a staging environment confirms each variable landed on the key
      you intended.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> Explain <code>IOptions</code>, <code>IOptionsSnapshot</code> and <code>IOptionsMonitor</code>.</summary>
      <p>All three give typed access to a bound options class; they differ in <strong>lifetime and reload
      behaviour</strong>.</p>
      <pre>  IOptions&lt;T&gt;          singleton   bound once on first use; never changes
  IOptionsSnapshot&lt;T&gt;  scoped      re-bound per request; sees reloads between requests
  IOptionsMonitor&lt;T&gt;   singleton   CurrentValue always latest; OnChange notifications</pre>
      <p><strong><code>IOptions&lt;T&gt;</code></strong> computes the value once and returns the same instance forever. It is
      the right default for the large majority of settings, which change only with a deployment.</p>
      <p><strong><code>IOptionsSnapshot&lt;T&gt;</code></strong> is scoped: it is re-bound for each request, so a changed
      configuration file takes effect on the next request, and the value stays <strong>consistent within a request</strong>.
      Because it is scoped, it cannot be injected into singletons, and binding on every request has a small cost.</p>
      <p><strong><code>IOptionsMonitor&lt;T&gt;</code></strong> is a singleton whose <code>CurrentValue</code> always reflects the
      latest configuration, with an <code>OnChange</code> callback. It is the choice for singletons and background services
      that must pick up changes — a worker whose polling interval can be tuned at runtime.</p>
      <p>Snapshot and monitor also support <strong>named options</strong> through <code>Get(name)</code> — several configured
      instances of one type, such as two HTTP API clients.</p>
      <p>The essential caveat: reloading only happens if the <strong>provider supports it</strong>. JSON files reload when
      <code>reloadOnChange</code> is on; environment variables and command-line arguments never change after startup. With a
      monitor, read <code>CurrentValue</code> at the point of use rather than caching it in a field, or you have rebuilt
      <code>IOptions</code> by accident.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> What does <code>ValidateOnStart()</code> change, and why is it worth a line of code?</summary>
      <p>Options validation is <strong>lazy</strong> by default. Validators attached with <code>ValidateDataAnnotations()</code>
      or <code>Validate(...)</code> run the first time something reads <code>.Value</code> — which may be the first request to
      one particular endpoint, hours after the deploy.</p>
      <pre>  builder.Services.AddOptions&lt;PaymentOptions&gt;()
      .BindConfiguration("Payments")
      .ValidateDataAnnotations()
      .Validate(o =&gt; o.TimeoutSeconds is &gt; 0 and &lt;= 30, "Timeout must be 1–30s")
      .ValidateOnStart();                   // validate while the host starts</pre>
      <p>Without <code>ValidateOnStart()</code>, a misconfigured deployment <strong>starts successfully</strong>. Health checks
      pass, the rolling deploy replaces every old instance, and the problem surfaces later as a partial outage: the checkout
      endpoint returns 500s while everything else looks healthy. The error appears far from its cause, under incident pressure,
      after the old, working version is gone.</p>
      <p>With it, validation runs while the host starts. A missing or invalid value <strong>stops the application from
      starting</strong>, with an error naming the option. The new instances never become ready, the orchestrator halts the
      rollout, and the old version keeps serving traffic. A configuration mistake becomes a failed deployment — minutes to
      diagnose, zero customer impact — instead of an incident.</p>
      <p>That asymmetry is why it is worth one line on every options registration. Pair it with validation that collects
      <strong>all</strong> failures at once, so a single startup log lists every problem rather than one per redeploy.</p>
      <p>Its limit: validation proves a value is well formed, not that it is right. A valid URL pointing at the staging payment
      provider passes; a readiness check that actually exercises the dependency catches what validation cannot.</p></details>''',
}, mistakes='''      <tr><td>Injecting <code>IOptions&lt;T&gt;</code> and expecting reloads</td><td>The value is fixed at first use</td><td><code>IOptionsMonitor&lt;T&gt;</code> or <code>IOptionsSnapshot&lt;T&gt;</code></td></tr>
      <tr><td>Expecting environment variables to reload</td><td>They are read once at startup</td><td>Restart to apply, or use a reloading provider</td></tr>
      <tr><td>Running with the Development environment in production</td><td>The developer exception page exposes stack traces</td><td>Leave it unset or set <code>Production</code> explicitly</td></tr>
      <tr><td>Misspelled keys that bind to nothing</td><td>The setting silently never applies</td><td><code>ErrorOnUnknownConfiguration = true</code> when binding</td></tr>
      <tr><td>Defaults that mask missing environment-specific values</td><td>Production quietly runs against localhost</td><td>No defaults for such values, plus <code>[Required]</code></td></tr>
      <tr><td>Environment file name casing that differs on Linux</td><td><code>appsettings.production.json</code> is never loaded</td><td>Match the environment name's casing exactly</td></tr>''',
takeaways='''      <li>Providers merge per key: an environment variable replaces one value, not a whole file.</li>
      <li><code>GetDebugView()</code> shows which provider supplied each key — use it to diagnose, never log it in production.</li>
      <li>The environment defaults to <code>Production</code> when <code>ASPNETCORE_ENVIRONMENT</code> is unset.</li>
      <li>Environment variables and command-line arguments never reload; only providers that support reloading do.</li>
      <li>File names are case-sensitive on Linux, so the environment file must match the environment name exactly.</li>
      <li>Options validation is lazy unless <code>ValidateOnStart()</code> moves it to startup.</li>''')

apply("tutorials/aspnet/controllers-mvc.html", iq={
1: '''<details class="solution"><summary><strong>Beginner:</strong> What does the <code>[ApiController]</code> attribute do?</summary>
      <p><code>[ApiController]</code> switches on a set of conventions designed for JSON APIs. Without it, a controller behaves
      like a classic MVC controller, and each of these has to be done by hand.</p>
      <p><strong>Automatic 400 responses.</strong> If model binding or validation fails, the framework returns a
      <code>400 Bad Request</code> with a <code>ValidationProblemDetails</code> body <strong>before the action runs</strong>.
      Without the attribute, invalid input reaches the action, and every action must remember to check
      <code>ModelState.IsValid</code> — forget once and invalid data is processed.</p>
      <p><strong>Binding source inference.</strong> Complex types are bound from the body, parameters matching route template
      names from the route, <code>IFormFile</code> from the form, and everything else from the query string — so
      <code>[FromBody]</code> and <code>[FromRoute]</code> are rarely needed.</p>
      <p><strong>Attribute routing required.</strong> Actions must declare their routes, which keeps the API's URL surface
      explicit instead of being derived from conventions.</p>
      <p><strong>Problem details for errors.</strong> Error status codes such as 404 returned with <code>NotFound()</code> get
      an RFC 9457 problem-details body.</p>
      <pre>  [ApiController]
  [Route("api/orders")]
  public class OrdersController(IOrderService orders) : ControllerBase
  {
      [HttpPost]
      public async Task&lt;ActionResult&lt;OrderDto&gt;&gt; Create(CreateOrder cmd)   // body inferred,
      {                                                                    // invalid → 400
          var dto = await orders.CreateAsync(cmd);
          return CreatedAtAction(nameof(Get), new { id = dto.Id }, dto);
      }
  }</pre>
      <p>It can be applied to a base class or to the whole assembly. The automatic 400 can be customised through
      <code>InvalidModelStateResponseFactory</code> when an API needs a different error shape.</p></details>''',
2: '''<details class="solution"><summary><strong>Beginner:</strong> What is the difference between <code>ControllerBase</code> and <code>Controller</code>?</summary>
      <p><code>ControllerBase</code> provides everything an <strong>API</strong> controller needs: helper methods that produce
      results — <code>Ok</code>, <code>NotFound</code>, <code>CreatedAtAction</code>, <code>Problem</code>,
      <code>ValidationProblem</code> — plus access to <code>HttpContext</code>, <code>User</code>, <code>ModelState</code> and
      <code>Url</code>.</p>
      <p><code>Controller</code> <strong>derives from</strong> <code>ControllerBase</code> and adds <strong>view</strong>
      support for server-rendered MVC: <code>View()</code> and <code>PartialView()</code>, <code>ViewData</code> and
      <code>ViewBag</code>, <code>TempData</code>, and action filters that run around view rendering.</p>
      <pre>  public class OrdersController : ControllerBase   // JSON API
  public class HomeController   : Controller       // returns Razor views</pre>
      <p>For an API, inherit <code>ControllerBase</code>. It signals intent — this controller returns data, not HTML — and keeps
      irrelevant members such as <code>ViewBag</code> and <code>View()</code> out of IntelliSense and out of reach. There is
      no functional benefit to <code>Controller</code> in an API, and its extra members invite mixing concerns.</p>
      <p>The same split appears in registration: <code>AddControllers()</code> registers what APIs need, while
      <code>AddControllersWithViews()</code> also registers Razor view support, which adds startup cost and services an API
      never uses.</p>
      <p>An application can contain both: <code>Controller</code> classes rendering pages and <code>ControllerBase</code>
      classes serving JSON, side by side. For new JSON endpoints, minimal APIs are also an option; they produce the same
      endpoints and coexist with controllers.</p></details>''',
3: '''<details class="solution"><summary><strong>Mid:</strong> When would you use <code>ActionResult&lt;T&gt;</code> over <code>IActionResult</code>?</summary>
      <p>Use <code>ActionResult&lt;T&gt;</code> whenever an action has a <strong>single success type</strong>, which is most
      API actions. It lets you return either the value itself or any other result:</p>
      <pre>  [HttpGet("{id:int}")]
  public async Task&lt;ActionResult&lt;OrderDto&gt;&gt; Get(int id)
  {
      var order = await _orders.FindAsync(id);
      if (order is null) return NotFound();        // an ActionResult
      return order;                                // T converts implicitly to 200 OK
  }</pre>
      <p>The benefits come from the type being visible in the signature. <strong>OpenAPI</strong> tooling knows the 200
      response's schema without a <code>[ProducesResponseType(typeof(OrderDto), 200)]</code> attribute that can drift from
      the code. <strong>The compiler</strong> checks that successful returns really are <code>OrderDto</code>s.
      <strong>Tests</strong> can read <code>result.Value</code> as a typed object instead of casting through
      <code>OkObjectResult</code>.</p>
      <p><code>IActionResult</code> remains right when an action has <strong>no single success type</strong>: it returns
      files, redirects, different payload types depending on the request, or empty results such as
      <code>NoContent()</code> only. It says nothing about the response shape, so documentation needs attributes.</p>
      <p>One wrinkle: C# does not allow implicit conversions from interfaces, so an action returning
      <code>ActionResult&lt;IEnumerable&lt;OrderDto&gt;&gt;</code> cannot simply <code>return list.AsEnumerable();</code> —
      return a concrete type such as a list or array, or wrap the value in <code>Ok(...)</code>.</p>
      <p>Minimal APIs go further with <code>TypedResults</code> and <code>Results&lt;Ok&lt;T&gt;, NotFound&gt;</code>, which put
      <em>every</em> possible response in the signature.</p></details>''',
4: '''<details class="solution"><summary><strong>Mid:</strong> Why is a passing controller unit test not evidence that an endpoint is secure?</summary>
      <p>Because a unit test calls the action <strong>as a plain method</strong>, and almost everything that secures an endpoint
      lives <strong>outside</strong> that method, in the request pipeline:</p>
      <pre>  // unit test: none of the pipeline runs
  var result = await new OrdersController(fakeService).Get(42);

  // what a real request passes through first:
  routing → authentication → authorization ([Authorize], policies, fallback)
          → CORS, rate limiting, antiforgery → filters → model binding + validation
          → the action</pre>
      <p>The test constructs the controller with <code>new</code> and invokes the method. The <code>[Authorize]</code> attribute
      is just metadata that nothing reads; the fallback policy never runs; resource checks performed in filters are skipped.
      The test proves the method's <strong>logic</strong> — given an order, it returns a DTO — and says nothing about whether
      an anonymous caller gets a 401, whether another customer gets that order, or whether someone removed the attribute last
      week.</p>
      <p>Evidence of security needs tests that go <strong>through the pipeline</strong>, with
      <code>WebApplicationFactory</code>:</p>
      <p>An <strong>anonymous</strong> request returns 401. An authenticated user <strong>without the permission</strong> gets
      403. A user requesting <strong>another user's</strong> resource gets 403 or 404. Only then does the happy path return
      200.</p>
      <p>A useful complement is a <strong>metadata test</strong> that enumerates every endpoint through
      <code>EndpointDataSource</code> and fails if any lacks authorization metadata without an explicit
      <code>AllowAnonymous</code> — catching the forgotten attribute across the whole API, not just the endpoints someone
      remembered to test.</p></details>''',
}, mistakes='''      <tr><td>Checking <code>ModelState.IsValid</code> under <code>[ApiController]</code></td><td>Dead code — invalid requests never reach the action</td><td>Rely on the automatic 400, or customise its factory</td></tr>
      <tr><td><code>IActionResult</code> for single-type actions</td><td>OpenAPI loses the response schema and tests need casts</td><td><code>ActionResult&lt;T&gt;</code></td></tr>
      <tr><td>Several <code>[FromBody]</code> parameters</td><td>Only one body can be bound, so the action fails</td><td>One request DTO</td></tr>
      <tr><td><code>CreatedAtAction(nameof(GetAsync))</code></td><td>MVC trims the Async suffix, so no route matches</td><td>Name the action without the suffix</td></tr>
      <tr><td>Binding EF entities as action parameters</td><td>Over-posting lets clients set fields they should not</td><td>Request DTOs</td></tr>''',
takeaways='''      <li><code>[ApiController]</code> returns a 400 problem response before the action runs when the model is invalid.</li>
      <li>Binding sources are inferred: complex types from the body, template parameters from the route, the rest from the query.</li>
      <li><code>ControllerBase</code> is the API surface; <code>Controller</code> only adds view rendering.</li>
      <li><code>ActionResult&lt;T&gt;</code> lets an action return <code>T</code> directly while documenting the success type.</li>
      <li>MVC trims the <code>Async</code> suffix from action names by default, which breaks <code>nameof</code>-based links.</li>
      <li>Only tests that go through the pipeline, plus a metadata sweep of every endpoint, prove authorization.</li>''')
