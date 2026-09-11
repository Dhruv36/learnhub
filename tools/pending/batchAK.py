# -*- coding: utf-8 -*-
"""dotnet batch AK: memory, methods, modern-csharp, oop."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import apply

apply("tutorials/dotnet/memory.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> What does the garbage collector do, and what does "reachable" mean?</summary>
      <p>The GC reclaims managed heap memory automatically. Allocation itself is almost free — the runtime bumps a pointer in
      a per-thread allocation region — so the real cost is paid at <strong>collection</strong>, and the GC's design is about
      making collections cheap and rare.</p>
      <p>A collection suspends managed threads at safe points and <strong>marks</strong> every object it can reach from the
      <strong>roots</strong>: live locals and registers in each thread's stack frames, static fields, GC handles (including
      pinned and strong handles held by the runtime), and the finalization queue. Everything unmarked is garbage. Survivors
      are usually compacted, and every reference to a moved object is updated.</p>
      <p><strong>Reachable</strong> means there is a chain of references from some root to the object. It is a property of the
      whole graph, not a count of references, and that has two consequences:</p>
      <pre>  var a = new Node();
  var b = new Node();
  a.Next = b;  b.Next = a;       // a cycle
  a = null;    b = null;         // no root reaches either: both collected, cycle and all

  static readonly List&lt;Node&gt; Recent = new();
  Recent.Add(new Node());        // reachable from a static root: lives until removed</pre>
      <p>Cycles are not a problem, unlike reference-counted systems such as COM. And a "leak" is always a reachability bug:
      something rooted still points at objects you no longer need. A <code>WeakReference</code> is the deliberate exception —
      it lets you observe an object without keeping it alive.</p>
      <p>One subtlety interviewers like: in an optimised Release build, the JIT tells the GC exactly where each local is still
      live, so an object can be collected <strong>before the method that created it returns</strong>, right after its last
      use. Debug builds extend locals to the end of the method, which is why memory behaves differently under a debugger, and
      why interop code sometimes needs <code>GC.KeepAlive</code>. The probe is whether you define "alive" precisely —
      reachable from a root — and reason from there.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What is <code>IDisposable</code>, and what does a <code>using</code> statement guarantee?</summary>
      <p><code>IDisposable</code> is a single method, <code>Dispose()</code>, and a contract: "I own something that must be
      released <strong>now</strong>, not whenever the GC gets round to it." That something is usually outside the managed
      heap — a file handle, a socket, a pooled database connection, a lock, native memory — or a registration such as an
      event subscription or a timer.</p>
      <p><code>using</code> guarantees that <code>Dispose</code> runs when the scope is left, <strong>however it is
      left</strong>: normal completion, <code>return</code>, <code>break</code> or an exception. It does that by compiling to
      <code>try</code>/<code>finally</code>:</p>
      <pre>  using var conn = new SqlConnection(cs);
  Work(conn);

  // lowered by the compiler to roughly:
  var conn = new SqlConnection(cs);
  try
  {
      Work(conn);
  }
  finally
  {
      if (conn != null) ((IDisposable)conn).Dispose();
  }</pre>
      <p>It is just as important to know what it does <strong>not</strong> guarantee. It does not free the object's memory;
      the object is collected later like any other. It does not run if the process is killed or
      <code>Environment.FailFast</code> is called, and a stack overflow ends the process without running <code>finally</code>
      blocks. And it cannot stop other references from outliving the resource; using a disposed object typically throws
      <code>ObjectDisposedException</code>.</p>
      <p>Two scoping details cause real bugs. A <strong>using declaration</strong> holds its resource until the end of the
      enclosing block, so a connection declared at the top of a long method stays checked out of the pool during all the slow
      work after it; a block or a smaller method releases it sooner. And returning a disposable from inside a
      <code>using</code> hands the caller an object that is already disposed. When cleanup itself does I/O, such as flushing a
      stream, use <code>await using</code> with <code>IAsyncDisposable</code>.</p>
      <p>The interviewer is probing whether you separate <strong>resource lifetime</strong> from <strong>memory
      lifetime</strong>, and understand ownership: whoever creates it disposes it.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> Explain the generational hypothesis and why gen2 collections are the ones you tune against.</summary>
      <p>The generational hypothesis says <strong>most objects die young</strong> — request DTOs, temporary strings, LINQ
      iterators — while objects that survive a while tend to live a long time: caches, singletons, configuration. The GC
      exploits it because a collection's cost scales with the objects that <strong>survive</strong>, not with the garbage;
      dead objects are never visited.</p>
      <p>So gen0 is collected often. If nearly everything in it is dead, the collection marks a handful of survivors, moves
      them to gen1, and resets the allocation region. The obvious question is how it can do that without scanning gen2 for
      references into gen0. The answer is the <strong>write barrier</strong>: when a reference is stored into an older object,
      the runtime marks a "card" for that region, and a gen0 collection scans only the dirty cards as extra roots. That is
      also why storing short-lived objects into long-lived structures has a cost: it promotes them and adds card
      scanning.</p>
      <p>Gen2 collections are expensive because they mark the <strong>entire heap</strong>, including the Large Object Heap.
      Background GC runs most of that marking concurrently, but it still burns CPU, and compacting a large gen2 moves a lot of
      memory. The healthy shape in the counters looks like this:</p>
      <pre>  Gen 0 collections   1,240     // many, cheap
  Gen 1 collections     310
  Gen 2 collections       4     // few, expensive
  % time in GC            2</pre>
      <p>That is why you tune against gen2, and the levers are about <strong>promotion</strong>, not allocation count. Avoid
      mid-lived objects: per-request data parked in a cache for a few seconds under load, or objects kept alive an extra cycle
      by a finalizer. Rent large buffers instead of allocating them, so the LOH does not churn. And keep the long-lived set
      small, because every full collection has to walk it.</p>
      <p>The interviewer is probing whether you know <em>why</em> gen0 is cheap, and whether you would look at promotion rates
      and gen2 counts before touching GC settings.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> What is <code>Span&lt;T&gt;</code>, why is it a <code>ref struct</code>, and when do you need <code>Memory&lt;T&gt;</code> instead?</summary>
      <p><code>Span&lt;T&gt;</code> is a <code>ref struct</code> holding two things: a managed reference to the first element
      and a length. That lets one type describe <strong>any contiguous memory</strong> — part of an array, the characters of
      a string as <code>ReadOnlySpan&lt;char&gt;</code>, a <code>stackalloc</code> buffer or native memory — with
      bounds-checked indexing and slicing that allocates nothing.</p>
      <p>It must be a <code>ref struct</code> for two reasons. A span can point at <strong>stack memory</strong>, and if it
      could be stored on the heap it could outlive the frame it points into. And it can point into the <strong>middle of an
      object</strong>, and the GC tracks such interior references only when they live on the stack. There is a quieter third
      reason: a two-field struct on the heap could be <strong>torn</strong> by concurrent writes, pairing one span's pointer
      with another's length and defeating bounds checks. So the compiler forbids span fields in classes, boxing, capture by
      lambdas, and any span local that is live across an <code>await</code> or <code>yield</code>.</p>
      <p><code>Memory&lt;T&gt;</code> is the answer when data must be stored or cross an asynchronous boundary. It is an
      ordinary struct — an object reference, an offset and a length — so it can live in fields and flow through async methods.
      You call <code>.Span</code> when synchronous work begins:</p>
      <pre>  async Task&lt;int&gt; ReadHeaderAsync(Stream s, Memory&lt;byte&gt; buffer, CancellationToken ct)
  {
      int n = await s.ReadAsync(buffer, ct);     // Memory crosses the await
      return ParseHeader(buffer.Span[..n]);      // Span for the synchronous work
  }

  static int ParseHeader(ReadOnlySpan&lt;byte&gt; data) { ... }</pre>
      <p>That gives the API guideline: <strong>synchronous methods take spans</strong>, since arrays, strings and slices all
      convert to them, and <strong>async methods take <code>Memory&lt;T&gt;</code></strong>, using the <code>ReadOnly</code>
      forms when they do not write. Neither type owns memory: a span into a pooled array that has already been returned is a
      use-after-free bug that corrupts data rather than crashing. The interviewer wants the reasoning behind the restrictions,
      not just the rules.</p></details>''',
}, mistakes='''      <tr><td>Returning a disposable created inside a <code>using</code></td><td>The caller receives an already disposed object</td><td>Transfer ownership: do not dispose it; the caller uses <code>using</code></td></tr>
      <tr><td>A using declaration at the top of a long method</td><td>The connection or lock is held through all the slow work</td><td>A block scope, or a smaller method</td></tr>
      <tr><td>Using a pooled array after returning it</td><td>Another renter overwrites the data under you</td><td>Return only when finished; keep no spans into it</td></tr>
      <tr><td>Assuming <code>ArrayPool.Rent</code> returns the exact length</td><td>Processing stale bytes past the requested size</td><td>Slice to the length you asked for</td></tr>
      <tr><td>Plain <code>Dispose</code> on a type that needs async cleanup</td><td>Blocking, or unflushed data</td><td><code>await using</code> with <code>IAsyncDisposable</code></td></tr>
      <tr><td>Investigating object lifetimes in a Debug build</td><td>Locals live to the end of the method, so objects linger</td><td>Analyse Release builds</td></tr>
      <tr><td>Keeping no reference to a <code>System.Threading.Timer</code></td><td>It can be collected and silently stop firing</td><td>Store it in a field and dispose it deliberately</td></tr>
      <tr><td>A <code>stackalloc</code> sized by input</td><td>Large inputs overflow the stack and kill the process</td><td>Cap the size and fall back to <code>ArrayPool</code></td></tr>''',
takeaways='''      <li><strong>Reachability from roots, not reference counting, decides what stays alive.</strong></li>
      <li><strong>Reference cycles are collected when nothing roots them.</strong></li>
      <li><strong>In Release builds a local stops being a root after its last use.</strong></li>
      <li><strong><code>using</code> compiles to <code>try</code>/<code>finally</code> and disposes even on exceptions.</strong></li>
      <li><strong><code>Dispose</code> releases resources; it does not free the object's memory.</strong></li>
      <li><strong>A using declaration holds its resource until the enclosing scope ends.</strong></li>
      <li><strong>Collection cost scales with survivors, not with garbage.</strong></li>
      <li><strong>The write barrier lets gen0 be collected without scanning gen2.</strong></li>
      <li><strong>Promotions, not allocations, feed expensive gen2 collections.</strong></li>
      <li><strong>A span is stack-only so it can safely point at stack memory and object interiors.</strong></li>
      <li><strong>Synchronous APIs take spans; async APIs take <code>Memory&lt;T&gt;</code>.</strong></li>
      <li><strong>Never touch a pooled buffer after returning it.</strong></li>''')
