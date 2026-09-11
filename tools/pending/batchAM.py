# -*- coding: utf-8 -*-
"""dotnet batch AM: testing, threading, types."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import apply

apply("tutorials/dotnet/testing.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> Difference between <code>[Fact]</code> and <code>[Theory]</code>? How does xUnit isolate tests?</summary>
      <p>A <strong><code>[Fact]</code></strong> is a single test case with no parameters: one scenario, one expected outcome.
      A <strong><code>[Theory]</code></strong> is a parameterised test that runs once per data row, and each row is reported as
      its own test. Rows come from <code>[InlineData]</code> for compile-time constants, <code>[MemberData]</code> for a static
      property or method, or <code>[ClassData]</code> for a reusable data class; the last two can supply objects that
      attributes cannot.</p>
      <pre>  [Theory]
  [InlineData(9,  90)]      // just below the discount threshold
  [InlineData(10, 90)]      // exactly at it
  [InlineData(11, 99)]      // just above
  public void Total_applies_bulk_discount_at_ten(int qty, decimal expected)
      =&gt; Assert.Equal(expected, new PriceCalculator().Total(10m, qty));</pre>
      <p>Theories make boundary testing cheap. The rows that earn their place hug the thresholds, because off-by-one
      comparisons such as <code>&gt;</code> versus <code>&gt;=</code> are where the bugs are. A failing row names its inputs in
      the report, so you see at once which boundary broke.</p>
      <p>Isolation is xUnit's sharpest design choice: it creates a <strong>new instance of the test class for every test
      method</strong>. The constructor is the setup, and <code>Dispose</code>, or <code>DisposeAsync</code> through
      <code>IAsyncLifetime</code>, is the teardown. There are no setup attributes, and instance fields cannot carry state from
      one test into the next. Static fields still can, which is one more reason to avoid them.</p>
      <p>Sharing is <strong>explicit</strong>. <code>IClassFixture&lt;T&gt;</code> creates one fixture per test class and injects
      it into every instance, for expensive resources such as a database container; a collection fixture shares one across
      several classes. That has a scheduling consequence: tests within a class or collection run sequentially, while separate
      collections run in parallel.</p>
      <p>The interviewer is probing whether you understand why the per-test instance matters, which is order-independent tests
      by construction, and whether you know that a fixture is shared mutable state you opted into, so each test must still
      leave it clean.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What's the difference between a unit test and an integration test, and why do you need both?</summary>
      <p>A <strong>unit test</strong> exercises a small piece of logic in isolation, with its external dependencies replaced by
      test doubles. It runs in milliseconds, needs no infrastructure, and when it fails it points at one method. It is the right
      tool for business rules, calculations, validation and state machines, where many boundary cases need covering
      cheaply.</p>
      <p>An <strong>integration test</strong> exercises real collaboration: a request going through the actual routing,
      middleware, model binding, DI container, EF Core mappings, a real SQL database and JSON serialisation. It is slower, from
      tens of milliseconds to seconds, and a failure points at a region rather than a line. What it proves is that the parts
      <strong>fit together</strong>.</p>
      <pre>  // green in a mocked unit suite, broken for real:
  //   a Singleton service that depends on the Scoped DbContext
  //   [JsonPropertyName("qty")] on the DTO while clients send "quantity"
  //   a unique index on Sku that the test double never enforces
  //   route template "/order/{id}" while clients call "/orders/{id}"</pre>
      <p>You need both because they <strong>fail in different places</strong>. Every failure in that list lives in the wiring
      between units, so a suite of mocked unit tests can be entirely green while every request returns a 500; integration tests
      catch exactly that class. The reverse also holds: covering every pricing boundary through HTTP would make the suite slow
      and its failures vague, so integration tests alone cannot cover the rules.</p>
      <p>The practical shape is the lesson's pyramid: many fast unit tests for logic, a solid middle layer of
      <code>WebApplicationFactory</code> tests per endpoint against a Testcontainers database, and a few end-to-end smoke tests
      after deploy. The common failure is a missing middle, with thousands of mocks and no integration layer, which is how a
      team gets a green build and a broken release.</p>
      <p>The interviewer wants the <em>why</em>: different tests find different bug classes, and a good strategy gives each
      class to the <strong>cheapest test that can catch it</strong>.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> Fake vs stub vs mock — and when is a mocking library the wrong choice?</summary>
      <p>The terms describe what a test double does. A <strong>fake</strong> is a working, simplified implementation with real
      behaviour, such as an in-memory repository where saving and then finding an order works. A <strong>stub</strong> returns
      canned answers so a code path can run, such as a payment gateway that always declines. A <strong>mock</strong> also
      records calls so the test can assert on them: the gateway was charged exactly once with the cart total. Libraries such as
      NSubstitute and Moq produce stubs and mocks; fakes are usually hand-written.</p>
      <pre>  // stub + requirement-level verification: the right use of a library
  gateway.ChargeAsync(Arg.Any&lt;Payment&gt;()).Returns(PaymentResult.Declined("insufficient"));
  var result = await svc.CheckoutAsync(cart);
  Assert.Equal(CheckoutStatus.PaymentFailed, result.Status);
  await gateway.Received(1).ChargeAsync(Arg.Is&lt;Payment&gt;(p =&gt; p.Amount == cart.Total));</pre>
      <p>A library is the <strong>wrong choice</strong> in recognisable cases. When the double needs <strong>coherent
      behaviour</strong>, like save then find or add then count, stubbing each call separately is brittle and hides bugs; a
      twenty-line fake is clearer and survives refactoring. When the test asserts <strong>internal choreography</strong>, such
      as which repository methods ran in what order, it breaks on every refactor while catching nothing. Verify only
      interactions that are requirements, like money moving or an email being sent.</p>
      <p>It is also wrong for <strong>types you do not own</strong>. Mocking <code>DbContext</code> or <code>DbSet</code> means
      re-implementing LINQ translation badly, so use a real database in a container. <code>HttpClient</code> is better tested
      with a stub <code>HttpMessageHandler</code> than through mocked wrappers. And mocking <code>ILogger</code> to verify log
      calls is fragile, because most logging methods are extension methods, and logging is rarely the requirement.</p>
      <p>The final tell is <strong>setup volume</strong>. If a test needs five mocks to construct the subject, the class has too
      many responsibilities, and the fix is in the production design rather than a more powerful mocking tool. The interviewer
      is probing for that judgement: fakes first, mocks deliberately.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> How do you test time-dependent logic like "orders older than 30 days are archived" without flaky tests?</summary>
      <p>Flaky time tests come from logic that reads <strong>ambient time</strong>, <code>DateTime.UtcNow</code> inside the
      method. The test cannot control it, so assertions depend on when the suite runs, and a boundary like "exactly 30 days" can
      pass or fail by milliseconds. The fix is to <strong>inject the clock</strong>. Since .NET 8 the platform ships
      <code>TimeProvider</code> for this: production registers <code>TimeProvider.System</code>, and tests pass a
      <code>FakeTimeProvider</code> from Microsoft.Extensions.TimeProvider.Testing.</p>
      <pre>  public class ArchivePolicy(TimeProvider clock)
  {
      public bool ShouldArchive(Order o) =&gt; clock.GetUtcNow() - o.PlacedAt &gt; TimeSpan.FromDays(30);
  }

  [Fact]
  public void Archives_only_after_thirty_days()
  {
      var clock  = new FakeTimeProvider(new DateTimeOffset(2026, 3, 1, 0, 0, 0, TimeSpan.Zero));
      var policy = new ArchivePolicy(clock);
      var order  = new Order { PlacedAt = clock.GetUtcNow() };

      clock.Advance(TimeSpan.FromDays(30));
      Assert.False(policy.ShouldArchive(order));    // exactly 30 days: kept
      clock.Advance(TimeSpan.FromTicks(1));
      Assert.True(policy.ShouldArchive(order));     // one tick later: archived
  }</pre>
      <p>The test now states the rule precisely, including the <strong>boundary decision</strong>: is an order of exactly 30
      days archived or kept? That choice, <code>&gt;</code> versus <code>&gt;=</code>, is usually unspecified until a test pins
      it down.</p>
      <p><code>FakeTimeProvider</code> also drives <strong>timers and delays</strong> created through the provider, such as
      <code>Task.Delay(span, provider)</code> or a <code>PeriodicTimer</code> constructed with it, so <code>Advance</code> fires
      them at once and a 15-minute schedule is tested in microseconds. Structure helps too: split the schedule loop from the
      logic, as the lesson does with the archiver, so the logic is a plain class and the loop is thin.</p>
      <p>Two more details. Store and compare <code>DateTimeOffset</code> or UTC values, never local time, so daylight-saving
      changes cannot move a boundary. And SQL that calls <code>GETDATE()</code> or <code>now()</code> reads the database
      server's clock and bypasses your injection, so pass the cutoff as a parameter. The interviewer is checking whether you
      treat time as a <strong>dependency</strong>.</p></details>''',
}, mistakes='''      <tr><td><code>async void</code> test methods</td><td>Failures can be missed or misattributed; xUnit v3 rejects them</td><td><code>async Task</code></td></tr>
      <tr><td>Swapping arguments in <code>Assert.Equal(actual, expected)</code></td><td>Failure messages report the values backwards</td><td>Expected first, actual second</td></tr>
      <tr><td>Asserting exact exception messages</td><td>Tests break on rewording and on localised messages</td><td>Assert the type and the relevant properties</td></tr>
      <tr><td><code>Assert.Throws</code> around an async call</td><td>The task is not awaited, so the wrong thing is checked</td><td><code>await Assert.ThrowsAsync</code></td></tr>
      <tr><td>A <code>WebApplicationFactory</code> that keeps real external services</td><td>Tests charge real cards or send real email</td><td><code>RemoveAll</code> and register a fake at the seam</td></tr>
      <tr><td><code>Thread.Sleep</code> waiting for background work</td><td>Slow when it passes, flaky when the machine is busy</td><td>Poll with a deadline, or drive time with <code>FakeTimeProvider</code></td></tr>
      <tr><td>Treating code coverage as the goal</td><td>Assertion-free tests inflate the number and catch nothing</td><td>Assert outcomes; use mutation testing to measure strength</td></tr>
      <tr><td>Tests that format numbers or dates under the ambient culture</td><td>They fail on a CI agent with a different locale</td><td>Set the culture explicitly in the test</td></tr>''',
takeaways='''      <li><strong>Each theory row is reported as its own test.</strong></li>
      <li><strong>Boundary rows sit on, just below and just above each threshold.</strong></li>
      <li><strong>The test class constructor is setup; <code>Dispose</code> is teardown.</strong></li>
      <li><strong>Tests in one collection run sequentially; collections run in parallel.</strong></li>
      <li><strong>Unit tests find logic bugs; integration tests find wiring bugs.</strong></li>
      <li><strong>Give each bug class to the cheapest test that can catch it.</strong></li>
      <li><strong>Fakes have behaviour, stubs return canned answers, mocks record calls.</strong></li>
      <li><strong>Do not mock types you do not own.</strong></li>
      <li><strong>Needing five mocks to build a subject is a design problem.</strong></li>
      <li><strong>Time is a dependency: inject <code>TimeProvider</code>.</strong></li>
      <li><strong>Pin the exact boundary of every time rule with a test.</strong></li>
      <li><strong>Pass time cutoffs to SQL instead of reading the database clock.</strong></li>''')

apply("tutorials/dotnet/threading.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> When do you use <code>Task.Run</code> vs plain <code>await</code>? </summary>
      <p>The question is <strong>what the work is waiting on</strong>. Plain <code>await</code> on an asynchronous API is for
      <strong>I/O-bound</strong> work: an HTTP call, a query, a file read. The operation is asynchronous at the OS level, so no
      thread is held while it waits. <code>Task.Run</code> is for <strong>CPU-bound</strong> work you want off the current
      thread: it queues a delegate to the thread pool, where a worker executes it and stays busy the whole time.</p>
      <pre>  // desktop: keep the UI thread free during a CPU-heavy computation
  var report = await Task.Run(() =&gt; BuildReport(rows), ct);

  // anywhere: the I/O is already asynchronous, so just await it
  var open = await db.Orders.Where(o =&gt; o.IsOpen).ToListAsync(ct);

  // anti-pattern: parks async I/O on a second pool thread for nothing
  var all = await Task.Run(() =&gt; db.Orders.ToListAsync(ct));</pre>
      <p>In a <strong>client application</strong>, <code>Task.Run</code> is the standard way to keep the UI responsive: the UI
      thread hands the computation to the pool, awaits the result, and resumes on the UI thread to display it. Put the
      <code>Task.Run</code> at the call site in the UI layer, not inside library methods; a method that looks asynchronous but
      secretly occupies a pool thread misleads every caller.</p>
      <p>In <strong>ASP.NET Core</strong>, the request already runs on a pool thread, so <code>Task.Run</code> buys nothing: you
      release one pool thread and occupy another, adding a context switch. Wrapping async I/O in it is pure waste, and wrapping
      synchronous blocking I/O only moves the blocked thread somewhere less visible; the fix there is the async API. Heavy CPU
      work in a request usually belongs in a background queue or a separate worker service.</p>
      <p><code>Task.Run</code> is also the modern replacement for <code>new Thread</code> and
      <code>Task.Factory.StartNew</code>: it always targets the default scheduler and unwraps async lambdas correctly, where
      <code>StartNew</code> would hand back a <code>Task&lt;Task&gt;</code>. A dedicated thread is justified only for a loop
      that runs for the life of the process. The interviewer is probing whether you separate <strong>waiting from
      working</strong>: async for one, threads for the other.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What is a race condition? Why does <code>counter++</code> from two threads lose increments?</summary>
      <p>A <strong>race condition</strong> is a bug where correctness depends on the timing of threads: the code works under
      one interleaving and fails under another. Because the scheduler chooses the interleaving, the failure is intermittent,
      load-dependent and often invisible on a developer machine with few cores.</p>
      <p><code>counter++</code> looks like one operation but is three: <strong>load</strong> the value into a register,
      <strong>add</strong> one, <strong>store</strong> it back. Two threads can interleave those steps:</p>
      <pre>  // counter == 5
  // T1: load 5
  // T2: load 5
  // T1: add, store 6
  // T2: add, store 6        → two increments ran, counter grew by one

  int counter = 0;
  Parallel.For(0, 100_000, _ =&gt; counter++);
  Console.WriteLine(counter);                                        // a different wrong number each run

  Parallel.For(0, 100_000, _ =&gt; Interlocked.Increment(ref counter)); // always 100,000</pre>
      <p>That is a <strong>lost update</strong>, and the more cores and the tighter the loop, the more often the windows overlap.
      There is a second, subtler problem: without synchronisation, one thread's write may not become <strong>visible</strong> to
      another promptly, because values can sit in registers or be reordered by the JIT and the CPU. So even one writer and one
      reader polling a plain field can misbehave; the classic case is a loop on a <code>bool</code> flag that never sees the
      change once the JIT hoists the read out of the loop.</p>
      <p>There are three fixes, in order of preference. <strong>Don't share</strong>: give each thread its own subtotal and merge
      once, using the <code>Parallel.ForEach</code> overload with local state, which has no contention at all. <strong>Make it
      atomic</strong>: <code>Interlocked.Increment</code> uses a hardware atomic instruction. <strong>Serialise</strong>: a
      <code>lock</code> when the update spans several steps, such as check-then-act.</p>
      <p>The interviewer is checking whether you can walk through the interleaving concretely, and whether you reach for "don't
      share" before reaching for locks.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> <code>lock</code> vs <code>Interlocked</code> vs <code>SemaphoreSlim</code> — when is each the right tool?</summary>
      <p>They solve different problems, and the choice follows the shape of what you are protecting.</p>
      <p><strong><code>Interlocked</code></strong> performs a <strong>single atomic operation</strong> on one field, such as
      <code>Increment</code>, <code>Add</code>, <code>Exchange</code> or <code>CompareExchange</code>, using a CPU instruction
      with no lock and no blocking. It is the cheapest tool and the right one for counters, flags and publishing a reference.
      Its limit is that it cannot make <em>two</em> steps atomic; compare-and-swap loops can build more, but that is lock-free
      programming, and it is easy to get wrong.</p>
      <p><strong><code>lock</code></strong> gives <strong>mutual exclusion</strong> for a multi-step invariant: check the balance
      then subtract, or update two fields together. Uncontended it costs a few tens of nanoseconds; under contention threads
      queue, and parallel code becomes sequential at that point. It is thread-affine and <strong>cannot contain an
      <code>await</code></strong>, which the compiler rejects. Lock on a private readonly object and hold it briefly. On .NET 9
      with C# 13, declaring that object as <code>System.Threading.Lock</code> gives the statement a faster, purpose-built
      type.</p>
      <p><strong><code>SemaphoreSlim</code></strong> has two roles. As <code>SemaphoreSlim(1, 1)</code> it is the
      <strong>async-compatible mutex</strong>: <code>WaitAsync</code> waits without blocking a thread, and release is not tied to
      the acquiring thread, so the critical section can contain <code>await</code>. As <code>SemaphoreSlim(n)</code> it is a
      <strong>throttle</strong> admitting at most n callers, for example to cap calls to a rate-limited API. It is not
      reentrant, and release belongs in <code>finally</code>.</p>
      <pre>  Interlocked.Increment(ref _requests);           // one field, one step

  lock (_sync)                                     // several steps, no await
  {
      if (_balance &lt; amount) return false;
      _balance -= amount;
  }

  await _gate.WaitAsync(ct);                       // the critical section awaits
  try { _token = await _auth.RefreshAsync(ct); }
  finally { _gate.Release(); }</pre>
      <p>The rule of thumb: one field, <code>Interlocked</code>; a synchronous invariant, <code>lock</code>; anything with an
      <code>await</code>, or a concurrency limit, <code>SemaphoreSlim</code>. The interviewer is probing whether you know
      <em>why</em> <code>lock</code> cannot span an await, and whether you choose the least powerful tool that works.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> Does <code>ConcurrentDictionary.GetOrAdd</code> guarantee the value factory runs only once per key? Consequences and fix?</summary>
      <p><strong>No.</strong> <code>GetOrAdd(key, factory)</code> guarantees that exactly <strong>one value is stored</strong>
      for the key and that every caller receives that stored value. It does not guarantee the factory runs once. To avoid
      calling arbitrary code while holding its internal lock, <code>ConcurrentDictionary</code> runs the factory
      <strong>outside the lock</strong>, so two threads that miss on the same key at the same moment can both run it; one
      result is stored and the other is discarded.</p>
      <p>Whether that matters depends on the factory. If it is cheap and pure, a discarded duplicate is harmless. If it is
      <strong>expensive</strong>, such as a database query or a remote call, you pay twice under exactly the load where you can
      least afford it, and a cold cache after a deploy can send a burst of duplicate queries. If it has <strong>side
      effects</strong>, such as opening a connection or starting a timer, the discarded value leaks, since nothing disposes
      it.</p>
      <pre>  private readonly ConcurrentDictionary&lt;string, Lazy&lt;Task&lt;Config&gt;&gt;&gt; _cache = new();

  public Task&lt;Config&gt; GetAsync(string tenant) =&gt;
      _cache.GetOrAdd(tenant, t =&gt; new Lazy&lt;Task&lt;Config&gt;&gt;(
          () =&gt; LoadConfigAsync(t),
          LazyThreadSafetyMode.ExecutionAndPublication)).Value;</pre>
      <p>The fix is to store <strong><code>Lazy&lt;V&gt;</code></strong> instead of <code>V</code>. Racing threads may each
      build a <code>Lazy</code> wrapper, which is cheap and runs nothing, but only one wrapper is stored and every caller reads
      <code>.Value</code> from that same instance. <code>ExecutionAndPublication</code> guarantees the load runs once. For async
      loads, store <code>Lazy&lt;Task&lt;V&gt;&gt;</code>, as above, so concurrent callers await one in-flight task.</p>
      <p>Two follow-ups show seniority. A <strong>failed</strong> load is cached too, because the <code>Lazy</code> rethrows or
      the faulted task stays stored, so remove the entry on failure if the next call should retry. And the update delegate of
      <code>AddOrUpdate</code> can also run more than once under contention, so it must be pure. The interviewer is checking
      whether you know that "thread-safe" describes the collection's own state, not your callbacks.</p></details>''',
}, mistakes='''      <tr><td>Polling a plain <code>bool</code> field set by another thread</td><td>The JIT may hoist the read, so the loop never sees the change</td><td><code>CancellationToken</code>, or <code>Volatile.Read</code></td></tr>
      <tr><td><code>Task.Run</code> inside library methods</td><td>Hides thread use; ASP.NET callers pay a pointless extra hop</td><td>Expose the synchronous API and let callers offload</td></tr>
      <tr><td>Reading <code>Count</code> or <code>Keys</code> of a <code>ConcurrentDictionary</code> on hot paths</td><td>Each call takes every internal lock</td><td>Track counts separately, or avoid the call</td></tr>
      <tr><td><code>ContainsKey</code> then <code>TryAdd</code> on a concurrent dictionary</td><td>Another thread acts between the two calls</td><td><code>GetOrAdd</code>, <code>AddOrUpdate</code> or <code>TryUpdate</code></td></tr>
      <tr><td>A single <code>CompareExchange</code> without a retry loop</td><td>The update is silently dropped when another thread wins</td><td>Loop until the swap succeeds</td></tr>
      <tr><td>Catching one exception type around <code>Parallel.ForEach</code></td><td>Failures arrive wrapped in <code>AggregateException</code></td><td>Inspect <code>InnerExceptions</code></td></tr>
      <tr><td>Raising <code>ThreadPool.SetMinThreads</code> to cure starvation</td><td>Masks the blocking code and spends memory on threads</td><td>Remove sync-over-async at the source</td></tr>
      <tr><td><code>[ThreadStatic]</code> or <code>ThreadLocal&lt;T&gt;</code> in async code</td><td>The value is gone when the continuation resumes on another thread</td><td><code>AsyncLocal&lt;T&gt;</code></td></tr>''',
takeaways='''      <li><strong>Await I/O; offload CPU work with <code>Task.Run</code>.</strong></li>
      <li><strong>Offload at the call site, not inside library methods.</strong></li>
      <li><strong><code>Task.Run</code> in ASP.NET Core only swaps one pool thread for another.</strong></li>
      <li><strong>A race condition is a bug that depends on thread timing.</strong></li>
      <li><strong><code>count++</code> is a load, an add and a store.</strong></li>
      <li><strong>Unsynchronised writes may not be visible to other threads.</strong></li>
      <li><strong>Prefer not sharing, then atomics, then locks.</strong></li>
      <li><strong>A <code>lock</code> is thread-affine and cannot span an await.</strong></li>
      <li><strong><code>SemaphoreSlim</code> is both an async mutex and a throttle.</strong></li>
      <li><strong>.NET 9 adds <code>System.Threading.Lock</code> as a dedicated lock type.</strong></li>
      <li><strong><code>GetOrAdd</code> stores one value but may run the factory several times.</strong></li>
      <li><strong>A failed <code>Lazy</code> load stays cached until you remove it.</strong></li>''')

apply("tutorials/dotnet/types.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> Value types vs reference types — what's the difference, and what does assignment do in each case?</summary>
      <p>The difference is <strong>what a variable holds</strong>. A value-type variable, such as an <code>int</code>,
      <code>double</code>, <code>DateTime</code>, <code>struct</code> or <code>enum</code>, contains <strong>the data
      itself</strong>. A reference-type variable, such as any <code>class</code>, <code>string</code>, array, delegate or record
      class, contains <strong>a reference</strong> to an object on the managed heap, or null.</p>
      <p>Assignment follows one rule: <strong>it always copies the variable's contents</strong>. For a value type the contents
      are the data, so you get an independent copy. For a reference type the contents are the reference, so you get a second
      name for the same object.</p>
      <pre>  var p1 = new PointStruct { X = 1 };
  var p2 = p1;          // copies the data
  p2.X = 99;            // p1.X is still 1

  var c1 = new PointClass { X = 1 };
  var c2 = c1;          // copies the reference
  c2.X = 99;            // c1.X is now 99: one object, two names

  void Reset(PointClass p)        { p = new PointClass(); }  // caller's variable unchanged
  void ResetRef(ref PointClass p) { p = new PointClass(); }  // caller's variable replaced</pre>
      <p>Parameter passing is assignment too, which explains both bug families. <strong>"My change didn't stick"</strong>: a
      method mutates a struct parameter, or a struct obtained through a property or list indexer, and changes a copy.
      <strong>"My change leaked"</strong>: a method mutates a list it was given, and the caller's list changes because both
      names refer to it.</p>
      <p>Keep two ideas apart. <strong>Value versus reference types</strong> is about what a variable holds; <strong>by value
      versus by <code>ref</code></strong> is about how a parameter is passed. Everything in C# is passed by value unless marked
      <code>ref</code>, <code>out</code> or <code>in</code>. Passing a reference type by value copies the reference, so the
      method can mutate the object but cannot make the caller's variable point elsewhere; with <code>ref</code> it can.</p>
      <p>The design consequence is why interviewers ask: every type you write picks a side, and immutability defuses both bug
      families. <code>string</code> is the illustration, a reference type that behaves like a value because it cannot
      change.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> Why is <code>decimal</code> the money type, and what do the literal suffixes mean?</summary>
      <p><code>double</code> and <code>float</code> are <strong>binary floating point</strong>: a binary fraction times a power
      of two. Most decimal fractions, including 0.1, have no finite binary representation, just as 1/3 has none in decimal. So
      <code>0.1 + 0.2</code> is 0.30000000000000004, and adding ten cents a thousand times gives 99.99999999999986. For
      measurements that is fine; for money it means totals that do not reconcile.</p>
      <p><code>decimal</code> is a 128-bit <strong>base-10</strong> type: a 96-bit integer plus a scale from 0 to 28, the power of
      ten to divide by. Any value with up to 28 significant digits is stored exactly, so <code>0.1m + 0.2m</code> is exactly
      0.3. It preserves scale too, so 1.50m prints as 1.50. The costs are speed, since it is implemented in software and is
      roughly ten times slower than <code>double</code>, and a smaller range; neither matters for business arithmetic.</p>
      <pre>  decimal price = 19.99m;           // m: decimal
  float   ratio = 0.5f;             // f: float
  double  rate  = 0.07;             // no suffix, or d: double
  long    big   = 5_000_000_000L;   // L: long (U and UL for unsigned)

  decimal wrong = 19.99;            // compile error CS0664: add the m suffix
  decimal third = 100m / 3;         // 33.33...: division still rounds</pre>
      <p>The suffixes choose a literal's type: <strong><code>m</code></strong> decimal, <strong><code>f</code></strong> float,
      <strong><code>d</code></strong> or none double, <strong><code>L</code></strong> long. The compiler rejects
      <code>decimal x = 19.99;</code> for good reason: the literal is already an inexact double before any conversion, so the rule
      forces the <code>m</code> and keeps binary rounding out of money.</p>
      <p>Decimal is exact for representation, not for every operation. Division still rounds, so money code needs an explicit
      <strong>rounding policy</strong>, <code>Math.Round(x, 2, MidpointRounding.ToEven)</code> or <code>AwayFromZero</code>,
      applied at defined points, plus allocation logic that places the leftover cent deliberately. The type must also flow
      <strong>end to end</strong>: one <code>double</code> in a DTO or a <code>float</code> column reintroduces drift. The
      interviewer is probing whether you know both halves.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> What is boxing, where does it hide, and why do .NET's reified generics matter here?</summary>
      <p><strong>Boxing</strong> happens when a value type is converted to <code>object</code>, or to an interface it
      implements. The runtime allocates a heap object with an object header, copies the value into it, and hands back a
      reference. <strong>Unboxing</strong> checks that the object holds exactly the target type and copies the value back out.
      Each box is an allocation, a copy and future GC work, and the box is a <strong>separate copy</strong>: changing it does
      not change the original.</p>
      <pre>  int n = 42;
  object o = n;                            // box: allocation + copy
  int back = (int)o;                       // unbox: type check + copy
  long wrong = (long)o;                    // InvalidCastException: the box holds an int

  IComparable c = n;                       // struct in an interface variable: box
  var legacy = new ArrayList { 1, 2, 3 };  // non-generic collection: a box per element
  string s = string.Format("{0}", n);      // object parameter: box
  string t = $"{n}";                       // interpolation handler: no box</pre>
      <p>It hides in predictable places: <strong>non-generic APIs</strong> such as <code>ArrayList</code> and
      <code>Hashtable</code>; <strong>structs stored in interface-typed variables</strong> or collections of interfaces;
      <strong>enums</strong> passed as <code>object</code>; calling <code>Equals</code> or <code>GetHashCode</code> on a struct
      that does not override them; and <code>params object[]</code> methods. In a loop over millions of items, these show up in
      an allocation profile as millions of <code>System.Int32</code> objects.</p>
      <p><strong>Reified generics</strong> are the systemic fix. In .NET, <code>List&lt;int&gt;</code> is a real runtime type:
      the JIT compiles a specialised version for each value-type argument, while reference-type arguments share one version, so
      the list stores raw 4-byte ints contiguously and <code>Add</code> never boxes. Java's generics use erasure, so
      <code>List&lt;Integer&gt;</code> holds a reference to a boxed object per element. <strong>Constraints</strong> extend this
      to methods: with <code>where T : IComparable&lt;T&gt;</code> the JIT calls a struct's <code>CompareTo</code> directly,
      where a parameter typed as the interface would box.</p>
      <p>The interviewer is probing two things: whether you can spot the hidden sites in review, and whether you can say
      precisely why .NET generics avoid the cost Java pays, namely specialisation per value type rather than erasure.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> "Value types live on the stack" — critique this common claim.</summary>
      <p>The claim is a <strong>half-truth</strong>. Its flaw is that it ties the storage location to the <em>type</em>, when it
      actually belongs to the <em>variable</em>. A value type lives <strong>wherever its container lives</strong>, stored inline
      without an object header.</p>
      <pre>  class Order { public decimal Total; }  // on the heap, inline inside each Order

  int[] counts = new int[1000];          // 1,000 ints on the heap, inside the array
  int local = 5;                         // a stack slot, or only a register

  Func&lt;int&gt; MakeCounter()
  {
      int n = 0;                         // captured: moved into a heap closure object
      return () =&gt; ++n;
  }

  async Task WorkAsync()
  {
      int x = 1;                         // lives across the await: hoisted into the state
      await Task.Delay(10);              // machine, which moves to the heap on suspension
      Use(x);
  }</pre>
      <p>Every case above except the plain local is a value type on the heap. A <strong>field</strong> of a class is part of the
      object. <strong>Array elements</strong> are stored inline in the array's heap memory, which is exactly why an array of
      structs is dense and cache-friendly. A <strong>captured local</strong> moves into a compiler-generated closure class. A
      local that lives across an <code>await</code> or <code>yield</code> is hoisted into the state machine. And a boxed value
      is on the heap by definition.</p>
      <p>Even the "local on the stack" half is an implementation detail: the JIT may keep a local only in a register, or remove
      it. The C# specification talks about <strong>lifetimes and copy semantics</strong>, not stacks.</p>
      <p>The accurate statement is that value types have <strong>copy semantics and inline storage</strong>: no separate
      allocation, no header, no indirection. That is the real performance point, density and zero per-item allocations. The
      genuinely stack-only types are <code>ref struct</code>s such as <code>Span&lt;T&gt;</code>, and the compiler enforces it:
      no boxing, no class fields, no lambda capture, and, since C# 13 relaxed the rule, no living across an
      <code>await</code>. The interviewer is probing whether you reason from the model rather than repeat the slogan.</p></details>''',
}, mistakes='''      <tr><td>Comparing <code>double</code> results with <code>==</code></td><td><code>0.1 + 0.2 == 0.3</code> is false</td><td>Compare within a tolerance, or use <code>decimal</code></td></tr>
      <tr><td>Treating a <code>default(DateTime)</code> field as a real date</td><td>Year 0001 values reach reports and databases</td><td><code>DateTime?</code> or a required member</td></tr>
      <tr><td><code>DateTime</code> values with an unspecified <code>Kind</code> across boundaries</td><td>Times shift by the server's UTC offset</td><td><code>DateTimeOffset</code> for instants</td></tr>
      <tr><td>Casting unvalidated integers to enums</td><td>Undefined values such as <code>(OrderStatus)42</code> flow through silently</td><td><code>Enum.IsDefined</code> at the boundary</td></tr>
      <tr><td>Renumbering or reordering persisted enum members</td><td>Stored rows change meaning without any migration</td><td>Explicit numbers that never change</td></tr>
      <tr><td>Integer division where a fraction was meant</td><td><code>1 / 3</code> is 0 before any conversion happens</td><td>Make one operand <code>decimal</code> or <code>double</code></td></tr>
      <tr><td>Unboxing to a different numeric type</td><td><code>(long)obj</code> on a boxed <code>int</code> throws <code>InvalidCastException</code></td><td>Unbox to the exact type, then convert</td></tr>
      <tr><td>Relying on the default <code>Math.Round</code> for money</td><td>Banker's rounding turns 2.5 into 2</td><td>Pass <code>MidpointRounding</code> explicitly</td></tr>''',
takeaways='''      <li><strong>Value versus reference is about what a variable holds.</strong></li>
      <li><strong>By value versus by <code>ref</code> is about how a parameter is passed.</strong></li>
      <li><strong>A reference passed by value lets a method mutate the object, not replace it.</strong></li>
      <li><strong>Immutability defuses both aliasing and lost-copy bugs.</strong></li>
      <li><strong>0.1 has no exact binary representation.</strong></li>
      <li><strong><code>decimal</code> stores a 96-bit integer and a base-10 scale.</strong></li>
      <li><strong>Decimal division still rounds, so money needs a rounding policy.</strong></li>
      <li><strong><code>Math.Round</code> uses banker's rounding by default.</strong></li>
      <li><strong>A box is a separate copy on the heap.</strong></li>
      <li><strong>Unboxing requires the exact original type.</strong></li>
      <li><strong>Generic constraints let the JIT call struct methods without boxing.</strong></li>
      <li><strong>A value type lives wherever its container lives.</strong></li>''')
