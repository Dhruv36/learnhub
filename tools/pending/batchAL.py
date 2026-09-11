# -*- coding: utf-8 -*-
"""dotnet batch AL: pattern-matching, performance-aot, records-structs, strings."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import apply

apply("tutorials/dotnet/pattern-matching.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> What is a type pattern, and how does <code>if (x is Circle c)</code> improve on the old approach?</summary>
      <p>A <strong>type pattern</strong> tests a value's runtime type and, if the test succeeds, <strong>casts and binds</strong>
      it to a new variable in the same expression. <code>if (x is Circle c)</code> asks whether <code>x</code> is a
      <code>Circle</code>, and inside the <code>if</code>, <code>c</code> is a strongly typed <code>Circle</code>. A null never
      matches a type pattern, so the null check comes for free.</p>
      <pre>  // old: test then cast, or 'as' plus a null check
  if (x is Circle) { var c = (Circle)x; Draw(c.Radius); }
  var c2 = x as Circle; if (c2 != null) Draw(c2.Radius);

  // pattern: one step, one type name, nothing to drift apart
  if (x is Circle c) Draw(c.Radius);

  if (x is not Circle circle) return;    // guard clause
  Draw(circle.Radius);                   // circle is assigned from here on</pre>
      <p>The old forms had real failure modes. <strong>Test-then-cast</strong> names the type twice, so a refactor can change
      one and not the other, and it performs the type check twice. <strong><code>as</code> plus a null check</strong> checks
      once, but separates the conversion from the test, and it does not work for non-nullable value types:
      <code>x as int</code> is a compile error, while <code>x is int n</code> unboxes directly.</p>
      <p>The binding is governed by <strong>definite assignment</strong>. The compiler knows <code>c</code> is assigned only
      where the pattern matched, so using it in the wrong branch is a compile error instead of a
      <code>NullReferenceException</code> at runtime. The negated form, <code>is not Circle circle</code>, is ideal for guard
      clauses: after the early return, <code>circle</code> is in scope and assigned for the rest of the method.</p>
      <p>A type pattern is also the entry point to the rest of the vocabulary. <code>x is Circle { Radius: &gt; 0 } c</code>
      combines a type test, a property condition and a binding in one readable expression.</p>
      <p>What the interviewer is probing is whether you see the pattern as more than sugar. It removes a class of drift bugs,
      and it lets the compiler track which variables are safe to use on which path.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> Why prefer a switch expression over a switch statement for computing a value, and what safety does it add?</summary>
      <p>A switch <strong>statement</strong> executes code; to compute a value with it, you declare a variable before the switch
      and assign it in every case. A switch <strong>expression</strong> <em>is</em> the value: each arm is
      <code>pattern =&gt; result</code>, and the whole thing can appear anywhere an expression can, such as a return, an
      initialiser, an argument or an expression-bodied member.</p>
      <pre>  decimal Fee(Account? a) =&gt; a switch
  {
      null                          =&gt; throw new ArgumentNullException(nameof(a)),
      { Balance: &lt; 0 }              =&gt; 35m,
      { Type: AccountType.Premium } =&gt; 0m,
      _                             =&gt; 12m,
  };</pre>
      <p>The safety comes in layers. <strong>No unassigned paths</strong>: every arm produces the result, so no case can forget
      to set a variable and there is no mutable temporary to reason about. <strong>No fall-through and no
      <code>break</code></strong> to forget. <strong>Reachability checking</strong>: if an earlier arm already covers a later
      one, such as <code>&gt;= 10</code> before <code>&gt;= 20</code>, the compiler reports error CS8510 instead of silently
      never running it.</p>
      <p>The headline is <strong>exhaustiveness</strong>. The compiler analyses the arms and warns with CS8509 when some input
      is not covered. Add <code>OrderStatus.Refunded</code> and every switch expression without an arm for it lights up,
      provided nobody added a discard, which swallows new members silently. At runtime an unmatched value throws
      <code>SwitchExpressionException</code> rather than leaving a default in place.</p>
      <p>One subtlety: enums are not truly closed, because <code>(OrderStatus)99</code> is legal. When every named member is
      covered, the compiler reports the unnamed values separately as CS8524. Teams that want new members flagged promote CS8509
      to an error and suppress CS8524, rather than adding a discard that hides future cases.</p>
      <p>Keep the statement form when each case performs several side effects rather than producing a value.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> Show how tuple patterns clean up a multi-condition decision, and why it's better than nested ifs.</summary>
      <p>When a decision depends on <strong>several inputs together</strong>, nested <code>if</code>s split it across levels:
      branch on one input, then on the next inside each branch. The combinations exist only implicitly, and a missing one is
      invisible because it is simply the absence of a branch. Grouping the inputs into a tuple and switching over it produces a
      <strong>flat decision table</strong>.</p>
      <pre>  // nested: the matrix is implicit
  if (type == OrderType.Express)
      rate = tier == CustomerTier.Gold ? 5m : 15m;
  else if (tier == CustomerTier.Gold)
      rate = 8m;
  else
      rate = 12m;

  // tuple switch: one row per rule
  decimal rate = (type, tier) switch
  {
      (OrderType.Express, CustomerTier.Gold) =&gt; 5m,
      (OrderType.Express, _)                 =&gt; 15m,
      (_, CustomerTier.Gold)                 =&gt; 8m,
      _                                      =&gt; 12m,
  };</pre>
      <p>The benefits are concrete. Each row reads as one rule, so a <strong>domain expert can check it against their own
      matrix</strong> line by line. A <code>_</code> in a position says "any value here", stating intent that an
      <code>else</code> only implies. Arms run <strong>top to bottom</strong>, so specific rows go before general ones, and the
      compiler rejects a row that can never be reached. Because it is an expression, every path yields a value, and when the
      inputs are enums the compiler checks exhaustiveness across the combinations.</p>
      <p>The canonical case is a state machine: <code>(current, evt) switch</code> literally is the transition table, and a
      final arm that throws <code>InvalidOperationException</code> makes an illegal transition loud instead of a silent no-op.
      Relational patterns fit inside positions too, as in <code>(&gt; 20, true) =&gt; 50m</code> for weight and
      international shipping.</p>
      <p>The tuple costs nothing: it is a <code>ValueTuple</code>, and the compiler usually lowers the switch without
      constructing it at all.</p>
      <p>The limit is width. Tuple switches scale in rows, not columns; beyond three or four inputs, or when rules must change
      without a deploy, the table belongs in data, such as a dictionary keyed by the tuple, rather than in code.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> When is switching on a type a code smell, and when is it legitimately the right design?</summary>
      <p>Switching on type is a smell when <strong>you own the hierarchy and the behaviour is the type's own
      responsibility</strong>. The lesson's <code>Area(Shape)</code> switch is the example: every new shape forces an edit to a
      central method, the shape's intrinsic logic lives outside the shape, and with an open hierarchy the discard arm means a
      forgotten <code>Hexagon</code> fails at runtime rather than at compile time. A <code>virtual Area()</code> puts the logic
      where it belongs and lets new types arrive without touching existing code.</p>
      <p>It is legitimately right in three situations. <strong>A sealed, closed hierarchy</strong>: the compiler proves
      exhaustiveness, and adding a variant lights up every switch that needs a new arm. <strong>Foreign types</strong>: you
      cannot add a virtual method to library exception types, so mapping them to HTTP status codes is naturally a switch.
      <strong>Behaviour that belongs to a consumer</strong>: rendering, serialisation and DTO mapping are concerns of one
      feature, and putting them on the model as virtual methods couples the domain to every consumer.</p>
      <pre>  // foreign types + a consumer's concern: a legitimate type switch
  static int StatusFor(Exception ex) =&gt; ex switch
  {
      ArgumentException           =&gt; 400,
      UnauthorizedAccessException =&gt; 403,
      KeyNotFoundException        =&gt; 404,
      TimeoutException            =&gt; 504,
      _                           =&gt; 500,
  };</pre>
      <p>The deeper framing is the <strong>expression problem</strong>. Polymorphism makes adding <em>types</em> cheap and
      adding <em>operations</em> expensive, because every class changes. Pattern matching over a closed set makes adding
      <em>operations</em> cheap and turns adding a type into a compiler-guided edit. Choose by which axis changes more
      often.</p>
      <p>Two review tells are worth naming. A type switch ending in <code>_ =&gt; throw new NotSupportedException()</code> over
      a hierarchy you own usually means a missing virtual method or a missing <code>sealed</code>. The same type switch
      <strong>duplicated in several places</strong> means the behaviour has no home. The interviewer wants the discriminator,
      ownership plus responsibility, not a dogmatic "always polymorphism".</p></details>''',
}, mistakes='''      <tr><td>Using <code>x is var y</code> as a null check</td><td>A <code>var</code> pattern always matches, null included</td><td><code>x is { } y</code> or <code>is not null</code></td></tr>
      <tr><td>Relational arms over <code>double</code> with no NaN case</td><td>NaN fails every relational pattern and hits the discard or throws</td><td>An explicit <code>double.NaN</code> arm</td></tr>
      <tr><td>Case-sensitive string constants for user input</td><td><code>"get"</code> never matches the <code>"GET"</code> arm</td><td>Normalise first, or a dictionary with <code>OrdinalIgnoreCase</code></td></tr>
      <tr><td>Side effects in <code>when</code> guards or pattern-matched getters</td><td>The compiler may reorder, cache or skip those evaluations</td><td>Keep patterns and guards pure</td></tr>
      <tr><td>A discard arm returning a plausible default</td><td>Unexpected input silently becomes a valid-looking result</td><td><code>_ =&gt; throw</code> with the value in the message</td></tr>
      <tr><td>Slice bindings like <code>.. var rest</code> on arrays in hot paths</td><td>Each match allocates a new array</td><td>Match on a span, or use <code>..</code> without a binding</td></tr>
      <tr><td>Expressing conditions as <code>when</code> guards that a pattern could state</td><td>Guarded arms are opaque to exhaustiveness analysis</td><td>Prefer property and relational patterns</td></tr>
      <tr><td>Positional patterns on types with several same-typed members</td><td>Reordering constructor parameters silently swaps the bindings</td><td>Property patterns with named members</td></tr>''',
takeaways='''      <li><strong>A type pattern tests, casts and binds in one step.</strong></li>
      <li><strong>A type pattern never matches null.</strong></li>
      <li><strong><code>is not T t</code> makes a guard clause with <code>t</code> in scope afterwards.</strong></li>
      <li><strong>The compiler rejects arms that earlier arms already cover.</strong></li>
      <li><strong>A discard arm hides newly added enum members.</strong></li>
      <li><strong>Enums admit unnamed values, so the compiler treats them as open.</strong></li>
      <li><strong>Arms run top to bottom, so put specific cases first.</strong></li>
      <li><strong><code>when</code> guards are invisible to exhaustiveness checking.</strong></li>
      <li><strong>Tuple switches cost no allocation.</strong></li>
      <li><strong>Beyond a few inputs, a decision table belongs in data.</strong></li>
      <li><strong>Polymorphism makes new types cheap; pattern matching makes new operations cheap.</strong></li>
      <li><strong>A type switch duplicated across the codebase means the behaviour has no home.</strong></li>''')

apply("tutorials/dotnet/performance-aot.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> A colleague timed two methods with <code>Stopwatch</code> in a Debug build and picked the winner. What's wrong?</summary>
      <p>Almost every part of that measurement is wrong, and the conclusion can easily be inverted. The first problem is the
      <strong>build</strong>. A Debug build compiles IL without optimisation, and an attached debugger stops the JIT optimising
      even Release code. Neither method ran the code production will run: inlining, bounds-check elimination and register
      allocation were missing, and their absence does not hurt both methods equally.</p>
      <p>The second is <strong>warm-up</strong>. The first calls include JIT compilation, and under tiered compilation a method
      runs as quick, unoptimised tier-0 code until it has been called about 30 times, after which it is recompiled with PGO. A
      short loop measures an unknown blend of compile time, tier-0 code and tier-1 code.</p>
      <p>The third is <strong>noise and dead code</strong>. A GC triggered by earlier allocations can land inside the timing
      window; frequency scaling and other processes skew a single run; and if the result is never used, the optimiser may delete
      the work entirely. One run with no variance gives no way to tell whether a 10% difference is real.</p>
      <pre>  [MemoryDiagnoser]
  public class Candidates
  {
      private readonly Order[] _orders = TestData.Orders(10_000);   // realistic size

      [Benchmark(Baseline = true)] public decimal A() =&gt; Pricing.TotalA(_orders);
      [Benchmark]                  public decimal B() =&gt; Pricing.TotalB(_orders);
  }   // results are returned, so the work cannot be eliminated
  // dotnet run -c Release, with BenchmarkRunner.Run&lt;Candidates&gt;() in Main</pre>
      <p>BenchmarkDotNet fixes each of these. It refuses non-optimised assemblies by default, runs in a separate process, warms
      up to steady state, runs many iterations and reports mean, error and standard deviation, consumes return values, and with
      <code>[MemoryDiagnoser]</code> reports bytes allocated per operation, often the more important number.</p>
      <p>The interviewer is probing scepticism about measurement. A strong answer also asks whether the difference matters at
      all, meaning how hot the method is in production, and whether the inputs were realistic, because a benchmark over ten
      items says little about ten thousand.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What order do you attack a "the API is slow" ticket?</summary>
      <p>The order is <strong>measure, localise, then fix the tier the evidence names</strong>, and never start by editing code.
      First, <strong>scope it</strong>: which endpoints, which percentile, since when, and on every instance or one? A P50 that
      doubled everywhere is systemic; a P99 that grew on one endpoint after a deploy points at a specific change, and "since
      when" gives you a diff to read.</p>
      <p>Second, check <strong>dependencies</strong>, the cheapest suspect to rule out. Distributed tracing or request telemetry
      shows how much of each request is spent in the database, a downstream HTTP call or a cache. If 700 of 800 milliseconds
      are one SQL query, the investigation moves to the query plan and the C# is irrelevant.</p>
      <p>Third, read the process's <strong>vital signs</strong>:</p>
      <pre>  dotnet-counters monitor -p &lt;pid&gt; --counters System.Runtime
  # high CPU                  → dotnet-trace, flame graph: the hot method names itself
  # high % time in GC         → allocation profiling: who allocates per request
  # low CPU, rising latency   → waiting: thread-pool queue, lock contention,
  #                             connection-pool waits, sync-over-async</pre>
      <p>Only then work down the lesson's hierarchy: <strong>architecture</strong> first (N+1 queries, missing caches,
      sequential awaits of independent calls, chatty APIs), then <strong>algorithms</strong> (quadratic scans, the wrong
      collection), then <strong>allocations</strong> in the proven hot path, and <strong>micro-optimisation</strong> last. Fix
      one thing, re-measure, and repeat, so every change carries its own evidence.</p>
      <p>The interviewer is checking discipline. A weak answer lists optimisation tricks. A strong one says that most slow-API
      tickets end at a query or a missing cache, that the 10–1000× wins live in architecture, and that low CPU with high
      latency means the process is <strong>waiting, not working</strong>, so no amount of faster C# will help.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> What is tiered compilation with dynamic PGO, and how does it change how you write and benchmark code?</summary>
      <p><strong>Tiered compilation</strong> resolves the JIT's basic tension: optimising well takes time, but startup wants code
      now. A method is first compiled at <strong>tier 0</strong>, quickly and with minimal optimisation. The runtime counts
      calls, and once a method has been called about 30 times it is queued for recompilation at <strong>tier 1</strong>, fully
      optimised, on a background thread. Long loops in methods called only once, such as <code>Main</code>, are handled by
      <strong>on-stack replacement</strong>, which switches a running loop to optimised code mid-execution.</p>
      <p><strong>Dynamic PGO</strong>, on by default since .NET 8, inserts an instrumented stage for hot methods. While
      instrumented, the method records what actually happens: which branches are taken and which concrete types appear at
      virtual and interface call sites. Tier 1 then compiles with that profile. The biggest win is <strong>guarded
      devirtualisation</strong>: if a call site almost always sees one concrete class, the JIT emits a cheap type check and a
      direct, inlinable call, keeping the virtual call as a fallback.</p>
      <pre>  // what the JIT effectively emits for a mostly-monomorphic interface call
  if (comparer.GetType() == typeof(OrdinalComparer))
      result = /* OrdinalComparer.Compare, inlined */;
  else
      result = comparer.Compare(a, b);      // rare path: normal interface dispatch</pre>
      <p>The consequences are practical. <strong>Benchmarks must reach steady state</strong>, because early iterations measure
      tier-0 code; BenchmarkDotNet's warm-up handles that. Services are <strong>slower just after a deploy</strong>, which
      matters for latency SLOs; warm-up traffic before joining the load balancer, or ReadyToRun to start from precompiled code,
      helps. <strong>Straightforward code optimises best</strong>: small methods inline, <code>sealed</code> classes
      devirtualise without a guard, and simple loops over arrays lose their bounds checks.</p>
      <p>One more: a benchmark with an unrealistic type mix misleads, because PGO specialises for what it observes. The
      interviewer is probing whether you know the runtime keeps optimising after startup, and why a NativeAOT binary, having no
      JIT, cannot.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> Compare JIT, ReadyToRun, and NativeAOT — and pick one for (a) a high-traffic API, (b) a CLI tool, (c) a serverless function.</summary>
      <p>The three sit on one axis: <strong>compile earlier, or optimise with more information</strong>. The
      <strong>JIT</strong> compiles at run time, so startup pays for compilation, but tiered compilation and dynamic PGO optimise
      hot code using real runtime behaviour, which gives the best steady-state throughput. <strong>ReadyToRun</strong>
      precompiles IL to native code at publish time and ships both. The app starts from precompiled code, typically 30–50%
      faster, and because the JIT is still present, hot methods are later recompiled at tier 1 with PGO. The cost is larger
      binaries, with no loss of compatibility.</p>
      <p><strong>NativeAOT</strong> compiles the whole app, trimmed to reachable code, into one native executable with no JIT
      at all. Startup takes milliseconds and memory is a fraction of a JIT app's. The price is that nothing can be generated or
      discovered at run time: <code>Reflection.Emit</code> and dynamic proxies fail, unconstrained reflection can hit trimmed
      members, and steady-state code is good but not PGO-tuned. Dependencies must be trim- and AOT-compatible, which in
      practice means source-generated JSON, DI and logging.</p>
      <pre>  &lt;!-- ReadyToRun: faster start, full compatibility --&gt;
  &lt;PublishReadyToRun&gt;true&lt;/PublishReadyToRun&gt;

  &lt;!-- NativeAOT: also enables the trim and AOT analyzers at build time --&gt;
  &lt;PublishAot&gt;true&lt;/PublishAot&gt;</pre>
      <p>The picks follow from what each workload pays for. <strong>(a) A high-traffic API</strong> runs for days, so startup is
      amortised and throughput dominates: the default JIT, or ReadyToRun if scale-out events and deploys make cold instances
      hurt latency. <strong>(b) A CLI tool</strong> runs for a second, so startup is the user experience: NativeAOT, which also
      gives a single file with no runtime to install. <strong>(c) A serverless function</strong> pays for cold starts in both
      latency and billing: NativeAOT where the dependencies support it, otherwise ReadyToRun.</p>
      <p>The interviewer is probing whether you treat AOT as a trade rather than an upgrade. A strong answer adds the
      verification step: publish AOT in CI from day one and treat trim warnings as errors, because the failures only appear
      in the published binary.</p></details>''',
}, mistakes='''      <tr><td>Benchmark methods that return <code>void</code> and discard the result</td><td>The JIT eliminates the work and the benchmark measures nothing</td><td>Return the result so BenchmarkDotNet consumes it</td></tr>
      <tr><td>Benchmarking one tiny, constant input</td><td>Caches and branch prediction flatter the result</td><td><code>[Params]</code> with realistic sizes and data</td></tr>
      <tr><td>Setup work inside the <code>[Benchmark]</code> method</td><td>You time the data preparation, not the code under test</td><td><code>[GlobalSetup]</code> or <code>[IterationSetup]</code></td></tr>
      <tr><td>Load-testing instances straight after deploy</td><td>Tier-0 code and cold caches distort the numbers</td><td>A warm-up period before measuring</td></tr>
      <tr><td>Suppressing IL2026 or IL3050 warnings to get a clean build</td><td>The trimmed binary fails at run time instead</td><td>Fix or annotate; treat trim warnings as errors</td></tr>
      <tr><td>Running tests only against the JIT build of an AOT app</td><td>Trimming and AOT failures never show up in CI</td><td>Integration-test the published native binary</td></tr>
      <tr><td>An unbounded <code>MemoryCache</code> as a performance fix</td><td>Memory grows without limit and GC pressure rises</td><td><code>SizeLimit</code>, entry sizes and expiry</td></tr>
      <tr><td>Expecting NativeAOT to speed up a long-running API</td><td>Without PGO, steady-state throughput is often lower</td><td>AOT for startup and memory; JIT for throughput</td></tr>''',
takeaways='''      <li><strong>Debug builds and attached debuggers disable JIT optimisation.</strong></li>
      <li><strong>A benchmark must use its result, or the work may be eliminated.</strong></li>
      <li><strong>Benchmark with realistic input sizes and shapes.</strong></li>
      <li><strong>Report variance, not a single number.</strong></li>
      <li><strong>Scope a slowdown by endpoint, percentile and start time before profiling.</strong></li>
      <li><strong>Rule out slow dependencies first; they are the cheapest suspect.</strong></li>
      <li><strong>Low CPU with high latency means the process is waiting, not working.</strong></li>
      <li><strong>Methods start at tier 0 and are recompiled after about 30 calls.</strong></li>
      <li><strong>Dynamic PGO devirtualises call sites based on the types it observes.</strong></li>
      <li><strong>Services run slower just after a deploy until hot code tiers up.</strong></li>
      <li><strong>ReadyToRun speeds startup without giving up the JIT.</strong></li>
      <li><strong>Trim warnings are run-time failures reported early.</strong></li>''')

apply("tutorials/dotnet/records-structs.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> What's the difference between reference equality and value equality, and what's the default for a class?</summary>
      <p><strong>Reference equality</strong> asks whether two variables point to <strong>the same object</strong>.
      <strong>Value equality</strong> asks whether two objects have <strong>the same contents</strong>. For a class, both
      <code>==</code> and <code>Equals</code> default to reference equality: two objects built with identical fields are
      unequal, because they are two separate allocations.</p>
      <pre>  var a = new PointClass { X = 1, Y = 2 };
  var b = new PointClass { X = 1, Y = 2 };
  a == b                                               // false: different objects
  new PointRecord(1, 2) == new PointRecord(1, 2)       // true: generated value equality
  new PointStruct(1, 2).Equals(new PointStruct(1, 2))  // true, via ValueType.Equals
  // new PointStruct(1, 2) == new PointStruct(1, 2)    // compile error: no == defined

  object s1 = "hi", s2 = new string("hi".ToCharArray());
  s1 == s2                                             // false: object ==, reference comparison
  s1.Equals(s2)                                        // true: virtual string.Equals</pre>
      <p>Each default fits a kind of type. Identity is right for <strong>entities</strong>, since two customers with the same
      name are still two customers, and for services and anything with a lifecycle. Contents are right for <strong>values and
      data</strong>: money, coordinates, DTOs, messages. The trap is that the class default is identity, so data modelled as a
      plain class compares wrongly unless you write equality by hand or declare a <code>record</code>.</p>
      <p>The exceptions matter. <code>string</code> is a class that overrides both <code>Equals</code> and <code>==</code> to
      compare contents ordinally. <strong>Structs</strong> default to value equality through <code>ValueType.Equals</code>,
      which compares fields, using reflection unless every field is a tightly packed primitive. And a plain struct has
      <strong>no <code>==</code> operator at all</strong> until you define one or declare a <code>record struct</code>.</p>
      <p>The subtle point is that <code>==</code> is an operator <strong>resolved at compile time from the static
      type</strong>, while <code>Equals</code> is virtual. Put two equal strings in <code>object</code> variables and
      <code>==</code> silently becomes a reference comparison, as the example shows. That is why generic code and collections
      call <code>Equals</code> or an <code>IEqualityComparer&lt;T&gt;</code>, never <code>==</code>.</p>
      <p>The interviewer is probing whether you treat equality as a design decision made per type, rather than a fixed rule of
      the language.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What does a <code>record</code> generate for you, and when should you use one?</summary>
      <p>From a positional declaration such as <code>public record Person(string Name, int Age);</code> the compiler generates a
      primary constructor and <strong>init-only properties</strong>; a value-based <strong><code>Equals</code></strong>,
      including the typed <code>IEquatable&lt;Person&gt;</code> overload, and a matching
      <strong><code>GetHashCode</code></strong> over every field; <strong><code>==</code> and <code>!=</code></strong>; a
      <strong><code>ToString</code></strong> that prints each property; a protected copy constructor and clone method that power
      <strong><code>with</code>-expressions</strong>; and a <strong><code>Deconstruct</code></strong> method. It also emits an
      <code>EqualityContract</code> property, so a base record and a derived record holding the same values are
      <em>not</em> equal.</p>
      <pre>  public record Person(string Name, int Age);

  var ada   = new Person("Ada", 36);
  var older = ada with { Age = 37 };      // copy, then change one property
  var (name, age) = ada;                  // generated Deconstruct
  Console.WriteLine(ada);                 // Person { Name = Ada, Age = 36 }

  public record Basket(List&lt;string&gt; Items);
  new Basket(["a"]) == new Basket(["a"])  // false: the lists compare by reference</pre>
      <p>Use a record for types that are <strong>fundamentally data compared by contents</strong>: DTOs and API contracts,
      domain value objects, messages and events, configuration, query results. The generated equality is correct by
      construction, which removes the most bug-prone boilerplate in C#.</p>
      <p>Know the limits. Equality is <strong>shallow</strong>: a collection property compares by reference, so the two baskets
      above are unequal despite equal contents. Immutability is shallow too, since <code>init</code> stops reassignment but not
      <code>Items.Add</code>, and <code>with</code> makes a <strong>shallow copy</strong> that shares the list with the
      original. The generated <code>ToString</code> prints every property, so it will happily write a password or token into a
      log.</p>
      <p>Avoid records for <strong>entities</strong> with identity and a lifecycle; they are also a poor fit for EF Core
      entities, which are tracked by identity and mutated in place. The interviewer is looking for the data-versus-identity
      split, plus awareness of the shallow-equality trap.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> Explain the <code>Equals</code>/<code>GetHashCode</code> contract and what breaks if you violate it.</summary>
      <p>The contract has three rules. Equality must be an <strong>equivalence relation</strong>: reflexive, symmetric and
      transitive, with <code>Equals(null)</code> returning false rather than throwing. <strong>Equal objects must return equal
      hash codes</strong>; the reverse is not required, because collisions are allowed. And an object's hash must <strong>not
      change while it sits in a hash-based collection</strong>, which in practice means hashing only immutable state.</p>
      <p>The reason is how <code>Dictionary</code> and <code>HashSet</code> work. They use the hash to pick a bucket and only
      then call <code>Equals</code> on the entries in that bucket. Equality is consulted only <em>after</em> the hash agrees,
      so a hash that disagrees with equality means the right entry is never even compared.</p>
      <pre>  public sealed class Sku : IEquatable&lt;Sku&gt;
  {
      public Sku(string code) =&gt; Code = code;
      public string Code { get; }

      public bool Equals(Sku? other) =&gt; other is not null
          &amp;&amp; string.Equals(Code, other.Code, StringComparison.OrdinalIgnoreCase);
      public override bool Equals(object? obj) =&gt; Equals(obj as Sku);

      // must follow the SAME equality: Code.GetHashCode() would be case-sensitive
      public override int GetHashCode() =&gt; StringComparer.OrdinalIgnoreCase.GetHashCode(Code);
  }</pre>
      <p>Violations fail silently. Override <code>Equals</code> without <code>GetHashCode</code> and equal keys hash by identity
      into different buckets: <code>ContainsKey</code> returns false, <code>HashSet.Add</code> accepts a duplicate, and LINQ's
      <code>Distinct</code> and <code>GroupBy</code> give wrong answers. Hash over a field that later changes and the entry
      sits in a bucket its new hash no longer points to. The <code>Sku</code> comment shows a subtler case: case-insensitive
      equality with a case-sensitive hash makes "abc" and "ABC" equal but usually in different buckets.</p>
      <p>Symmetry breaks with inheritance: a base class comparing its fields and a derived class also comparing its own give
      different answers depending on which object is the receiver. Sealing the class, or checking <code>GetType()</code>,
      avoids it; records use <code>EqualityContract</code>.</p>
      <p>The interviewer is probing whether you can explain <em>why</em> the contract exists, buckets first and equality
      second, because that is what makes the "dictionary lost my entry" bug quick to diagnose.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> When is a struct the right choice over a class, and what are the constraints?</summary>
      <p>A struct is a <strong>value type</strong>: it is stored inline, in a local, inside its containing object or as an
      array element, and it is copied on assignment. An array of a million structs is one allocation, and a struct local
      creates no garbage. That is the benefit: <strong>less GC pressure and better memory locality</strong>. Every constraint
      follows from the copying.</p>
      <p>A struct is the right choice when the type is <strong>small</strong>, roughly 16–24 bytes, so a copy costs about as
      much as passing a reference; <strong>logically a single value</strong>, such as a coordinate, an amount or an id;
      <strong>immutable</strong>; and used <strong>in volume or on hot paths</strong>, where the saved allocation shows up in a
      profile. <code>DateTime</code>, <code>Guid</code>, <code>TimeSpan</code> and <code>decimal</code> are the models.</p>
      <pre>  public readonly record struct Money(decimal Amount, string Currency);   // 16 + 8 bytes

  var prices = new Money[1_000_000];     // one allocation, contiguous memory
  Money none = default;                  // Amount 0, Currency null: no constructor ran
  object boxed = prices[0];              // boxing: a heap copy is allocated here</pre>
      <p>The constraints are the cost of being a value. <strong>Copies are silent</strong>: a large struct is copied on every
      assignment, argument and return, and mutation through a <code>List&lt;T&gt;</code> indexer, a property or a
      <code>readonly</code> field acts on a copy, the mutable-struct trap. <strong>Boxing</strong>: converting to
      <code>object</code> or a non-generic interface allocates a copy, which defeats the purpose; generic constraints avoid it.
      <strong>No inheritance</strong>. And every struct has a <strong>zeroed default</strong> that bypasses the constructor, so
      arrays and <code>default</code> produce values your validation never saw.</p>
      <p>Equality needs care as well: the inherited <code>Equals</code> can fall back to reflection, so use
      <code>record struct</code> or implement <code>IEquatable&lt;T&gt;</code>.</p>
      <p>The interviewer wants the narrow profile and a measured reason. "Structs are faster" is the wrong answer; "a small
      immutable value that removes an allocation from a measured hot path" is the right one.</p></details>''',
}, mistakes='''      <tr><td>A record with a collection property, expecting value equality</td><td>The collection compares by reference, so equal contents are unequal</td><td>Custom <code>Equals</code> with <code>SequenceEqual</code>, or a value-equal wrapper</td></tr>
      <tr><td>Assuming <code>with</code> makes a deep copy</td><td>The copy and the original share mutable members</td><td>Immutable collections, or copy those members explicitly</td></tr>
      <tr><td>Records as EF Core entities</td><td>Value equality conflicts with identity-based tracking</td><td>Classes for entities; records for DTOs</td></tr>
      <tr><td>Trusting a struct's constructor validation</td><td><code>default</code> and new arrays produce zeroed values that skipped it</td><td>Make the zero value valid, or validate on use</td></tr>
      <tr><td>Passing structs as <code>object</code> or non-generic interfaces</td><td>Every conversion boxes: an allocation and a detached copy</td><td>Generic methods with interface constraints</td></tr>
      <tr><td>Custom <code>Equals</code> in a record without <code>GetHashCode</code></td><td>Hash disagrees with equality; the compiler warns with CS8851</td><td>Define both together</td></tr>
      <tr><td><code>in</code> parameters of a non-readonly struct</td><td>Each member call makes a hidden defensive copy</td><td>Mark the struct <code>readonly</code></td></tr>
      <tr><td>Secrets in records that get logged</td><td>The generated <code>ToString</code> prints every property</td><td>Override <code>PrintMembers</code>, or keep secrets out of records</td></tr>''',
takeaways='''      <li><strong>Classes compare by identity unless you say otherwise.</strong></li>
      <li><strong>A plain struct has no <code>==</code> operator until you define one.</strong></li>
      <li><strong><code>==</code> binds to the static type; <code>Equals</code> is virtual.</strong></li>
      <li><strong>Record equality and <code>with</code> copies are shallow.</strong></li>
      <li><strong><code>EqualityContract</code> keeps a base record unequal to a derived one.</strong></li>
      <li><strong>A record's <code>ToString</code> prints every property, secrets included.</strong></li>
      <li><strong>Hash collections check the hash first and <code>Equals</code> second.</strong></li>
      <li><strong>Equal objects must share a hash; unequal objects may.</strong></li>
      <li><strong>The hash must follow the same notion of equality as <code>Equals</code>.</strong></li>
      <li><strong>A struct saves an allocation and costs a copy.</strong></li>
      <li><strong>Every struct has a zeroed default that skips its constructor.</strong></li>
      <li><strong>Boxing a struct allocates and detaches a copy.</strong></li>''')

apply("tutorials/dotnet/strings.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> Why are .NET strings immutable, and what are two consequences a developer must know?</summary>
      <p>A .NET string's contents <strong>never change after construction</strong>. Every method that seems to modify one, such
      as <code>Trim</code>, <code>Replace</code> or <code>ToUpper</code>, returns a new string. The platform made that choice
      because strings are shared everywhere, and immutability makes the sharing safe and cheap.</p>
      <p>The benefits are specific. <strong>Safe sharing</strong>: a method can store a string it was given without a defensive
      copy, because the caller cannot change it later. <strong>Security</strong>: a path or connection string validated once
      cannot be swapped between the check and the use. <strong>Stable hashing</strong>: a string's hash cannot drift, so
      strings are reliable dictionary keys. <strong>Thread safety</strong>: concurrent readers need no locks. And
      <strong>interning</strong>: identical literals share one object, since nobody can modify it.</p>
      <pre>  string name = "  Ada  ";
  name.Trim();                  // result discarded: name is unchanged
  name = name.Trim();           // correct: capture the new string

  var report = "";
  foreach (var line in lines)
      report += line;           // allocates and copies everything so far, every pass</pre>
      <p>The first consequence: <strong>ignoring the return value is a silent no-op</strong>. <code>s.Trim();</code> compiles,
      runs and changes nothing, and the bug often survives testing because the test data had no padding. Analyzer rule CA1806
      flags ignored results; turn it on.</p>
      <p>The second: <strong>accumulating in a loop is quadratic</strong>. Each <code>+=</code> allocates a new string and
      copies all the text so far, so total copying grows with the square of the output, and every intermediate string is
      garbage. Once the text passes about 42,500 characters, or 85,000 bytes, each intermediate lands on the Large Object Heap,
      which is collected only with gen 2. <code>StringBuilder</code> or <code>string.Join</code> make it linear.</p>
      <p>The interviewer is probing whether you connect the design decision to its costs. Immutability is why
      <code>StringBuilder</code>, <code>string.Create</code> and <code>ReadOnlySpan&lt;char&gt;</code> exist: each gives a
      mutable or allocation-free path where immutability would be too expensive.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> When do you use StringBuilder vs interpolation vs string.Join?</summary>
      <p>Choose by the <strong>shape</strong> of the assembly rather than by a blanket rule.</p>
      <p><strong>A fixed handful of pieces</strong> → interpolation. <code>$"{dir}/{name}.{ext}"</code> is the clearest form,
      and since C# 10 the compiler lowers it to a <code>DefaultInterpolatedStringHandler</code> that formats into a pooled
      buffer and produces one string, without boxing value-type holes. The old advice that interpolation is
      <code>string.Format</code> with boxing no longer applies. Plain <code>a + b + c</code> compiles to one
      <code>string.Concat</code> and is fine too.</p>
      <p><strong>A collection with a separator</strong> → <code>string.Join</code>. It handles separators and the empty case
      correctly, and a hand-written builder loop with a trailing-separator check is more code for no gain.</p>
      <p><strong>A loop that grows text, or conditional assembly</strong> → <code>StringBuilder</code>. It appends into internal
      chunks at amortised constant cost and materialises one string at the end, turning quadratic concatenation into linear.
      Pre-size it when you can estimate the output, prefer typed overloads such as <code>Append(int)</code>, and interpolate
      straight into it: since .NET 6, <code>Append</code> has an interpolated-string handler that writes each hole directly
      into the builder with no intermediate string.</p>
      <pre>  var sb = new StringBuilder(capacity: rows.Count * 48);
  foreach (var r in rows)
      sb.Append(CultureInfo.InvariantCulture, $"{r.Id},{r.Sku},{r.Total}").AppendLine();
  return sb.ToString();         // one final string; invariant culture for a machine format</pre>
      <p>Two more tools sit at the extremes. <code>string.Create</code> writes directly into a new string's buffer when you
      know the exact length, which pays off on proven hot paths. Spans avoid producing strings at all when you are parsing
      rather than building.</p>
      <p>The judgement the interviewer is probing: <code>StringBuilder</code> for three fragments is ceremony, <code>+=</code>
      in a loop is quadratic, and for logs and wire formats the culture used to format numbers matters as much as the
      mechanism.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> Explain the Turkish-i bug and the discipline that prevents the whole class.</summary>
      <p>Culture-aware casing follows the <strong>current culture's linguistic rules</strong>, and in Turkish and Azerbaijani the
      letter i comes in two forms: dotted <em>i/İ</em> and dotless <em>ı/I</em>. Under tr-TR, <code>"FILE".ToLower()</code>
      produces "fıle" with a dotless ı, and <code>"file".ToUpper()</code> produces "FİLE". A check like
      <code>input.ToLower() == "file"</code> passes on every developer machine and fails for Turkish users, or on any server
      whose culture is tr-TR.</p>
      <pre>  CultureInfo.CurrentCulture = new CultureInfo("tr-TR");
  "FILE".ToLower() == "file"                                          // false
  string.Equals("FILE", "file", StringComparison.OrdinalIgnoreCase)   // true in any culture
  "FILE".Equals("file", StringComparison.CurrentCultureIgnoreCase)    // false under tr-TR</pre>
      <p>Turkish-i is one member of a wider class: <strong>machine logic that silently depends on the user's or server's
      locale</strong>. The class includes culture-aware sorting that changes which item comes first, and defaults that are easy
      to forget: <code>StartsWith(string)</code>, <code>EndsWith(string)</code>, <code>IndexOf(string)</code> and
      <code>CompareTo</code> are culture-sensitive, while <code>Equals</code>, <code>==</code> and <code>Contains(string)</code>
      are ordinal. It also includes platform drift: when .NET 5 moved globalisation to ICU, a culture-sensitive
      <code>IndexOf</code> searching for a line feed inside a CRLF pair started returning -1 on some systems.</p>
      <p>The discipline is that <strong>every comparison states its mode</strong>. Anything machine-meaningful, such as keys,
      identifiers, file paths, HTTP headers and protocol tokens, uses <code>Ordinal</code> or <code>OrdinalIgnoreCase</code>.
      Casing for logic uses <code>ToUpperInvariant</code>, though comparing with <code>OrdinalIgnoreCase</code> is better
      still because it allocates nothing. Culture-aware comparison is reserved for text a human reads and sorts, with the
      culture chosen deliberately.</p>
      <p>Then make it structural rather than a matter of memory. Pass a <code>StringComparer</code> to dictionaries, sets and
      sorts; enable analyzers CA1307, CA1309 and CA1310 as build errors; and run one test pass under tr-TR, which flushes out
      the whole class at once. The interviewer is checking whether you fix the class of bug, not just the instance.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> <code>"🎸".Length</code> returns 2. Explain, and state what this means for substring/truncate logic.</summary>
      <p>A .NET string is a sequence of <strong>UTF-16 code units</strong>, and <code>Length</code> counts those units, not
      characters. Code points above U+FFFF, which include most emoji such as 🎸 (U+1F3B8), do not fit in 16 bits, so UTF-16
      encodes each as a <strong>surrogate pair</strong>: two <code>char</code> values that mean nothing on their own. So
      <code>"🎸".Length</code> is 2, and <code>"🎸"[0]</code> is half a character.</p>
      <p>It goes further than surrogates. What a user sees as one character is a <strong>grapheme cluster</strong>, which may be
      several code points: "é" can be one code point or an <em>e</em> plus a combining accent, a flag is two regional-indicator
      code points, and the family emoji 👨‍👩‍👧 is three people joined by zero-width joiners, five code points in eight
      <code>char</code>s.</p>
      <pre>  var family = "👨‍👩‍👧";
  family.Length                                 // 8  UTF-16 code units
  family.EnumerateRunes().Count()               // 5  code points
  new StringInfo(family).LengthInTextElements   // 1  grapheme cluster (.NET 5+)
  "🎸"[..1]                                     // a lone surrogate: invalid text</pre>
      <p>For truncation this matters. Cutting by <code>char</code> index can <strong>split a surrogate pair</strong>, leaving a
      lone surrogate that renders as a box and that UTF-8 encoding replaces with U+FFFD. It can strip the accent from a letter
      or break a joined emoji into separate people. And a "maximum 20 characters" rule checked with <code>Length</code>
      rejects names a user sees as twelve characters long.</p>
      <p>The fix is to <strong>decide which unit you are counting</strong>. For display limits, count and cut by text elements
      with <code>StringInfo</code>, as the lesson's <code>TruncateForDisplay</code> does. For byte limits, such as a message
      size cap, count <strong>bytes in the target encoding</strong> with <code>Encoding.UTF8.GetByteCount</code> and cut on a
      boundary. An <code>nvarchar(50)</code> column, by contrast, counts UTF-16 code units, so <code>Length</code> is exactly
      right there, as it is for ASCII protocol text you control.</p>
      <p>The interviewer is probing whether you know "character" is ambiguous and can say which meaning each piece of code
      needs.</p></details>''',
}, mistakes='''      <tr><td><code>StartsWith</code> or <code>IndexOf</code> with a string and no comparison</td><td>Culture-sensitive by default, and results vary between ICU and NLS</td><td>Pass <code>StringComparison.Ordinal</code></td></tr>
      <tr><td>Interpolated strings in log calls</td><td>Formatted even when the level is off, and structured properties are lost</td><td>Message templates: <code>LogInformation("Order {OrderId}", id)</code></td></tr>
      <tr><td>User text used as a composite format string</td><td>A stray brace throws <code>FormatException</code></td><td>Pass user text as an argument, never as the format</td></tr>
      <tr><td>Indexing <code>Split</code> results from untrusted input</td><td><code>IndexOutOfRangeException</code> when a separator is missing</td><td>Check the count, or parse with <code>IndexOf</code> on a span</td></tr>
      <tr><td><code>IsNullOrEmpty</code> to validate required input</td><td>Whitespace-only values pass validation</td><td><code>IsNullOrWhiteSpace</code></td></tr>
      <tr><td>Ordinal comparison of unnormalised Unicode</td><td>Composed and decomposed "é" compare unequal</td><td><code>Normalize()</code> to Form C at the input boundary</td></tr>
      <tr><td><code>Encoding.ASCII</code> for general text</td><td>Every non-ASCII character becomes <code>?</code>, permanently</td><td><code>Encoding.UTF8</code></td></tr>
      <tr><td>Regexes on user input without a timeout</td><td>Catastrophic backtracking pins a CPU core</td><td><code>[GeneratedRegex]</code> with a timeout, or <code>RegexOptions.NonBacktracking</code></td></tr>''',
takeaways='''      <li><strong>Ignoring a string method's return value is a silent no-op.</strong></li>
      <li><strong>Strings over 85,000 bytes land on the Large Object Heap.</strong></li>
      <li><strong>Modern interpolation compiles to a handler that avoids boxing.</strong></li>
      <li><strong><code>StringBuilder.Append</code> takes interpolated strings without an intermediate copy.</strong></li>
      <li><strong>Pre-size a <code>StringBuilder</code> when the output size is predictable.</strong></li>
      <li><strong><code>StartsWith(string)</code> and <code>IndexOf(string)</code> are culture-sensitive by default.</strong></li>
      <li><strong>Culture-aware results can change with the globalisation library.</strong></li>
      <li><strong>One test pass under tr-TR flushes out culture bugs.</strong></li>
      <li><strong>A user-perceived character can span several code points.</strong></li>
      <li><strong>Count graphemes for display limits and bytes for byte limits.</strong></li>
      <li><strong>Normalise text before comparing it ordinally.</strong></li>
      <li><strong>Log with message templates, not interpolated strings.</strong></li>''')
