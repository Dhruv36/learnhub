# -*- coding: utf-8 -*-
"""dotnet batch AJ: generics, index, inheritance, linq."""
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from lib import apply

apply("tutorials/dotnet/generics.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> What problem do generics solve, and what were the alternatives before them?</summary>
      <p>Generics resolve the tension between <strong>reuse and type safety</strong>. A stack, a cache or a sorting routine is
      logically identical whether it holds integers or orders, and before C# 2.0 there was no way to write it once without
      giving something up.</p>
      <p>The first alternative was <strong>duplication</strong>: an <code>IntStack</code>, a <code>StringStack</code>, one per
      element type. Each copy is type-safe and fast, but every bug fix has to be applied N times, and the copies drift apart.
      Teams used code generators to make this bearable, which only moved the duplication into the build.</p>
      <p>The second was <strong>object-based containers</strong> such as <code>ArrayList</code> and <code>Hashtable</code>.
      There is one implementation, but it carries three concrete costs: every value type is <strong>boxed</strong> on the way
      in, which means a heap allocation and later GC work; every read needs a <strong>cast</strong>; and a wrong-type insertion
      fails <strong>late</strong>, as an <code>InvalidCastException</code> at the read site, often far from the code that
      inserted the bad item.</p>
      <pre>  var old = new ArrayList();
  old.Add(42);                 // boxes: allocates an object on the heap
  old.Add("42");               // compiles — nothing stops it
  int n = (int)old[1];         // InvalidCastException, at runtime, at the READ

  var list = new List&lt;int&gt;();
  list.Add(42);                // stored raw in an int[]; no allocation per item
  // list.Add("42");           // compile error, at the WRITE
  int m = list[0];             // no cast</pre>
      <p><code>List&lt;T&gt;</code> gives <strong>one definition</strong> that the compiler checks at every call site, stores
      value types unboxed, and returns the real type. Because .NET generics are reified, the runtime also generates
      specialised code for each value-type instantiation, so the reuse costs nothing at runtime.</p>
      <p>What the interviewer is probing is whether you can name those costs — boxing, casts and late failure — rather than
      just saying "type safety". It is also worth showing how far generics reach beyond collections: <code>Task&lt;T&gt;</code>,
      <code>Func&lt;T&gt;</code>, <code>Span&lt;T&gt;</code>, and even <code>int?</code>, which is
      <code>Nullable&lt;int&gt;</code>, a generic struct.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What are generic constraints, and why can't you do much with an unconstrained <code>T</code>?</summary>
      <p>An unconstrained <code>T</code> means the compiler must produce code that is valid for <strong>every possible type
      argument</strong>: value or reference type, sealed or abstract, with or without a constructor. So it allows only what
      every type supports — the members of <code>object</code>, assignment, <code>default(T)</code>, and comparison against
      <code>null</code>. It will not let you call <code>CompareTo</code>, use <code>==</code> between two <code>T</code>
      values, or write <code>new T()</code>, because it cannot prove those exist.</p>
      <p>A constraint is a <strong>two-sided contract</strong>. Inside the method, it unlocks exactly the declared
      capabilities. At every call site, the compiler checks that the type argument actually has them, so the error appears
      where the wrong type is supplied, not deep inside the generic code.</p>
      <pre>  where T : IComparable&lt;T&gt;   // can call CompareTo
  where T : class            // reference type: null checks, 'as'
  where T : struct           // non-nullable value type: T? means Nullable&lt;T&gt;
  where T : unmanaged        // no references inside: sizeof, stackalloc, pointers
  where T : new()            // public parameterless constructor
  where T : notnull          // non-nullable, e.g. dictionary keys
  where T : INumber&lt;T&gt;       // generic math: T.Zero, +, * (C# 11)</pre>
      <p>Constraints also affect <strong>performance</strong>. Compare <code>void Log(IFormattable x)</code> with
      <code>void Log&lt;T&gt;(T x) where T : IFormattable</code>. Passing an <code>int</code> to the first boxes it on every
      call. The generic version does not: the JIT compiles a specialised body for <code>int</code> and calls the method
      directly, often inlining it. That is why the BCL uses constrained generics on hot paths.</p>
      <p>Two practical rules follow. Add <strong>only the constraints the code uses</strong>, because each one narrows who can
      call you. And prefer a <code>Func&lt;T&gt;</code> factory to <code>new()</code> when construction needs arguments or
      dependencies, since <code>new()</code> only permits a parameterless constructor.</p>
      <p>The interviewer is checking that you see constraints as the vocabulary of generic code — without them, <code>T</code>
      is only a placeholder — and that you know the boxing difference, which separates people who use generic APIs from
      people who design them.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> Explain reified generics and give three concrete consequences of .NET having them.</summary>
      <p><strong>Reified</strong> means the type argument is part of the object's runtime identity. Assembly metadata holds the
      open definition, <code>List`1</code>, and at runtime the CLR creates a distinct closed type for each instantiation —
      <code>List&lt;int&gt;</code> and <code>List&lt;string&gt;</code> each have their own type handle. Java, by contrast,
      <strong>erases</strong> type arguments at compile time, so the JVM only ever sees a raw <code>List</code>.</p>
      <p><strong>1. Value types are stored and processed unboxed.</strong> <code>List&lt;int&gt;</code> is backed by an
      <code>int[]</code>, and the JIT compiles a separate native body for each value-type instantiation, with correctly sized
      storage and direct, inlinable calls; <code>EqualityComparer&lt;T&gt;.Default</code>, for example, is devirtualised for
      <code>int</code>. Reference-type instantiations share one canonical body, because every reference is pointer-sized; the
      shared code looks up the exact type through a small runtime dictionary when it needs it.</p>
      <p><strong>2. Runtime type information works.</strong> <code>typeof(T)</code>, <code>x is T</code>,
      <code>default(T)</code> and <code>new T()</code> all behave correctly. One consequence surprises people: <strong>every
      closed type gets its own static fields</strong>, which is the basis of a common caching idiom.</p>
      <pre>  static class TypeName&lt;T&gt;
  {
      public static readonly string Value = typeof(T).Name;   // computed once per T
  }

  TypeName&lt;int&gt;.Value;      // "Int32" — its own static
  TypeName&lt;Order&gt;.Value;    // "Order" — a separate static, although the code is shared</pre>
      <p><strong>3. Reflection, DI and serialisation see the real types.</strong> A container can register an open generic,
      <code>AddScoped(typeof(IRepository&lt;&gt;), typeof(Repository&lt;&gt;))</code>, and close it at runtime for
      <code>IRepository&lt;Order&gt;</code>. A serialiser knows a property is <code>List&lt;Order&gt;</code>, not a list of
      objects.</p>
      <p>The trade-offs are worth naming. Each value-type instantiation adds native code, which matters for NativeAOT binary
      size. And NativeAOT must know instantiations at build time, so <code>MakeGenericType</code> over a value type that never
      appears in the code can fail at runtime. The interviewer wants the <em>why</em> behind reification, including its
      costs.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> What is covariance vs contravariance, and why is <code>List&lt;T&gt;</code> invariant?</summary>
      <p>Variance answers whether a conversion between type arguments carries over to the constructed types.
      <code>Dog</code> converts to <code>Animal</code>. <strong>Covariance</strong> means <code>IEnumerable&lt;Dog&gt;</code>
      converts to <code>IEnumerable&lt;Animal&gt;</code>, in the same direction; <strong>contravariance</strong> means
      <code>IComparer&lt;Animal&gt;</code> converts to <code>IComparer&lt;Dog&gt;</code>, in the reverse direction.</p>
      <p>The rule is data flow. With <code>out T</code>, <code>T</code> appears only in <strong>output positions</strong> —
      return values and read-only properties — so a consumer only ever receives a <code>T</code>, and a <code>Dog</code>
      received as an <code>Animal</code> is always safe. With <code>in T</code>, <code>T</code> appears only in <strong>input
      positions</strong>: a comparer that accepts any animal can certainly accept a dog. The compiler enforces this; declaring
      <code>out T</code> and then taking <code>T</code> as a parameter is a compile error.</p>
      <p><code>List&lt;T&gt;</code> is <strong>invariant</strong> because <code>T</code> flows both ways: <code>Add(T)</code>
      takes it in and the indexer hands it out. Allowing a <code>List&lt;Dog&gt;</code> as a <code>List&lt;Animal&gt;</code>
      would let someone add a <code>Cat</code>. Arrays show what happens when a language allows it anyway. C# arrays are
      covariant for historical reasons, and the hole is patched with a runtime check:</p>
      <pre>  object[] items = new string[2];     // allowed: array covariance
  items[0] = "fine";
  items[1] = 42;                      // ArrayTypeMismatchException at runtime</pre>
      <p>That check runs on stores into reference-type arrays unless the JIT can prove it unnecessary. Invariant generics move
      the same error to compile time and avoid the cost.</p>
      <p>Two limits complete the picture. Variance applies only to <strong>interfaces and delegates</strong>, never to classes
      or structs. And it works only for <strong>reference-type arguments</strong>: <code>IEnumerable&lt;int&gt;</code> does not
      convert to <code>IEnumerable&lt;object&gt;</code>, because each <code>int</code> would need boxing — a change of
      representation, not a reinterpretation of the same reference. Use <code>Cast&lt;object&gt;()</code> there. The
      interviewer is probing whether you can derive these rules from data flow instead of reciting them.</p></details>''',
}, mistakes='''      <tr><td>An interface parameter for struct arguments on a hot path</td><td>Every call boxes the value</td><td>A generic method constrained to the interface</td></tr>
      <tr><td>Comparing two <code>T</code> values with <code>==</code></td><td>Does not compile unconstrained; reference equality when constrained to <code>class</code></td><td><code>EqualityComparer&lt;T&gt;.Default.Equals(a, b)</code></td></tr>
      <tr><td>Using <code>new()</code> when construction needs arguments</td><td>Forces parameterless constructors and mutable setup</td><td>Accept a <code>Func&lt;T&gt;</code> factory</td></tr>
      <tr><td>Assuming unconstrained <code>T?</code> means <code>Nullable&lt;T&gt;</code></td><td>For <code>T = int</code> it is plain <code>int</code>, so null never appears</td><td>Constrain to <code>struct</code>, or return a <code>bool</code> with an <code>out</code> value</td></tr>
      <tr><td>Expecting <code>IEnumerable&lt;int&gt;</code> to convert to <code>IEnumerable&lt;object&gt;</code></td><td>Variance works only for reference types</td><td><code>Cast&lt;object&gt;()</code></td></tr>
      <tr><td>Relying on array covariance</td><td><code>ArrayTypeMismatchException</code> at runtime</td><td>Pass <code>IReadOnlyList&lt;T&gt;</code> instead of <code>object[]</code></td></tr>
      <tr><td>Assuming a generic type's static field is shared</td><td>Each closed type has its own copy</td><td>Move shared state to a non-generic class</td></tr>
      <tr><td><code>MakeGenericType</code> over value types under NativeAOT</td><td>The instantiation was never compiled, so it fails at runtime</td><td>Use only instantiations known at build time</td></tr>''',
takeaways='''      <li><strong>Generics replace object-based reuse with compile-time checked reuse.</strong></li>
      <li><strong>Boxing, casts and late failures are the costs generics removed.</strong></li>
      <li><strong>An unconstrained <code>T</code> permits only what every type supports.</strong></li>
      <li><strong>Constraints are checked inside the method and at every call site.</strong></li>
      <li><strong>Add only the constraints the code actually uses.</strong></li>
      <li><strong>A constrained <code>T</code> avoids boxing that an interface parameter would cause.</strong></li>
      <li><strong>Value-type instantiations get their own native code; reference types share one body.</strong></li>
      <li><strong>Each closed generic type has its own static fields.</strong></li>
      <li><strong>DI containers close open generic registrations at runtime.</strong></li>
      <li><strong>Variance applies only to interfaces and delegates with reference-type arguments.</strong></li>
      <li><strong>Array covariance is a runtime-checked hole that invariant generics avoid.</strong></li>
      <li><strong>Compare generic values with <code>EqualityComparer&lt;T&gt;.Default</code>.</strong></li>''')

apply("tutorials/dotnet/index.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> What are the CLR, IL, and JIT, and how do they relate?</summary>
      <p>They are three stages of one pipeline. <strong>Roslyn</strong>, the C# compiler, turns source into <strong>IL</strong>
      plus metadata, packaged in an assembly. The <strong>CLR</strong> loads that assembly and supervises execution. The
      <strong>JIT</strong>, one component of the CLR, turns each method's IL into native machine code the first time the method
      is called.</p>
      <p><strong>IL</strong> is a stack-based, CPU-neutral instruction set. The <strong>metadata</strong> beside it describes
      every type, member, signature and referenced assembly. That makes an assembly self-describing — there are no header
      files — and it is what reflection, dependency injection, serialisers and cross-language calls are built on.</p>
      <pre>  static int Add(int a, int b) =&gt; a + b;

  // IL, in the .dll — identical on every platform
  ldarg.0
  ldarg.1
  add
  ret

  // what the JIT emits on x64 Windows, at the first call
  lea  eax, [rcx+rdx]
  ret</pre>
      <p>The mechanics of "first call" are worth knowing. Every method starts out pointing at a small <strong>stub</strong>. The
      first call lands in the stub, which invokes the JIT; the JIT compiles the method and <strong>patches the entry
      point</strong>, so later calls go straight to native code. With tiered compilation, a hot method is later recompiled with
      full optimisation and the entry point is patched again.</p>
      <p>The CLR does much more than JIT compilation: it loads and checks types, runs the garbage collector, unwinds
      exceptions, manages threads and marshals calls into native libraries. And on servers and desktops it does not interpret
      IL; every method is compiled before it runs.</p>
      <p>The interviewer is checking that you understand C# is compiled twice, and can connect that to real behaviour:
      first-call latency, benchmark warm-up, and why ReadyToRun and NativeAOT exist to move the second compilation to build
      time.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> .NET Framework vs .NET Core vs .NET 8/9 — untangle the names.</summary>
      <p>The names describe <strong>three eras of one platform</strong>, and the confusion comes from a decade in which two of
      them overlapped.</p>
      <pre>  .NET Framework 1.0 – 4.8.1   2002–   Windows-only, installed into the OS, feature-frozen
  .NET Core 1.0 – 3.1          2016–   cross-platform rewrite, open source, side by side
  .NET 5, 6, 7, 8, 9, 10 ...   2020–   "Core" dropped; one platform, a release every November
  .NET Standard 2.0 / 2.1              an API specification, not a runtime</pre>
      <p><strong>.NET Framework</strong> is installed machine-wide as part of Windows and updated in place, so every app on the
      machine shares one runtime. Version 4.8.1 is the last; it still receives security fixes as a Windows component, but no
      new features. Technologies such as WCF server, WebForms, AppDomains and remoting exist only there.</p>
      <p><strong>.NET Core</strong> was the 2016 rewrite: cross-platform, open source, installed <strong>side by side</strong>
      so different apps can use different runtime versions, and deployable self-contained with the app. It deliberately left
      the Windows-only technologies behind.</p>
      <p><strong>.NET 5</strong> dropped "Core" to signal that this was now the only line going forward, and skipped the
      number 4 to avoid confusion with Framework 4.x. Since then there has been one release a year: even-numbered releases are
      <strong>Long Term Support</strong> for three years, odd ones Standard Term Support with a shorter window. "Core" survives
      in <strong>ASP.NET Core</strong> and <strong>EF Core</strong> to distinguish them from their Framework-era
      predecessors.</p>
      <p><strong>.NET Standard</strong> was the bridge: a contract of APIs that a library could target to run on both Framework
      and Core. <code>netstandard2.0</code> is still the right target for a library that Framework apps must consume; code
      for modern .NET only should target <code>net8.0</code> or later directly. The interviewer is probing whether you can
      tell a legacy estate from a modern one, and what that means for dependencies and migration.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> What is tiered compilation, and what practical behaviors does it explain?</summary>
      <p>Tiered compilation resolves a tension in any JIT. Heavy optimisation produces fast code but takes time to compile,
      which hurts startup; light optimisation starts fast but leaves throughput on the table. Since .NET Core 3.0 the runtime
      does <strong>both, in stages</strong>.</p>
      <p>A method is first compiled at <strong>tier 0</strong> — quickly, with minimal optimisation — or uses ReadyToRun code
      if the assembly was precompiled. The runtime counts calls; after roughly 30 calls the method is queued for <strong>tier
      1</strong>, recompiled with full optimisation on a background thread, and its entry point is swapped. Long-running loops
      are handled by <strong>on-stack replacement</strong>, which lets a loop already running in tier-0 code jump into
      optimised code without waiting for the next call.</p>
      <p><strong>Dynamic PGO</strong>, on by default since .NET 8, adds profiling. An instrumented tier records which concrete
      types reach virtual and interface calls and which branches are taken, and tier 1 uses that data to <strong>devirtualise
      and inline</strong> the common case behind a cheap type check.</p>
      <pre>  &lt;TieredCompilation&gt;false&lt;/TieredCompilation&gt;   &lt;!-- full JIT up front: slower start --&gt;
  &lt;TieredPGO&gt;false&lt;/TieredPGO&gt;                   &lt;!-- keep the tiers, drop profiling --&gt;
  &lt;PublishReadyToRun&gt;true&lt;/PublishReadyToRun&gt;   &lt;!-- precompiled code as the first tier --&gt;</pre>
      <p>It explains several behaviours: a freshly deployed service answering its first requests slowly; a microbenchmark
      without warm-up measuring tier-0 code and the JIT itself; a profiler showing the same method compiled twice; and a
      long-running process that keeps getting faster for its first minutes. Turning tiering off to "fix" warm-up is rarely
      right, because it slows startup and loses PGO.</p>
      <p>The interviewer is probing whether you understand that the running code is not fixed at first compilation. That shapes
      deployment choices: ReadyToRun for faster starts, and NativeAOT, which starts instantly but has no Dynamic PGO, so its
      steady-state throughput can be lower.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> Walk through what a modern .csproj controls and why SDK-style projects matter.</summary>
      <p>A <code>.csproj</code> is an <strong>MSBuild project</strong>. The SDK attribute imports a large set of default
      properties and targets, so the file only has to state what differs from the defaults. Legacy project files spelled
      everything out — every source file, GUIDs, imports — and ran to hundreds of lines that were painful to merge.</p>
      <pre>  &lt;Project Sdk="Microsoft.NET.Sdk.Web"&gt;
    &lt;PropertyGroup&gt;
      &lt;TargetFrameworks&gt;net8.0;net9.0&lt;/TargetFrameworks&gt;
      &lt;Nullable&gt;enable&lt;/Nullable&gt;
      &lt;TreatWarningsAsErrors&gt;true&lt;/TreatWarningsAsErrors&gt;
      &lt;InvariantGlobalization&gt;true&lt;/InvariantGlobalization&gt;
    &lt;/PropertyGroup&gt;
    &lt;ItemGroup&gt;
      &lt;PackageReference Include="Serilog.AspNetCore" /&gt;
      &lt;ProjectReference Include="../Shop.Domain/Shop.Domain.csproj" /&gt;
    &lt;/ItemGroup&gt;
  &lt;/Project&gt;</pre>
      <p>The file controls the <strong>target frameworks</strong> (multi-targeting is one line), the <strong>output
      type</strong>, compiler switches such as <code>Nullable</code>, <code>LangVersion</code> and warnings-as-errors,
      <strong>package and project references</strong>, and publish settings such as <code>PublishAot</code>. The SDK variant
      matters too: <code>Microsoft.NET.Sdk.Web</code> adds the ASP.NET Core framework reference and web-specific implicit
      usings. The C# version defaults from the target framework: C# 12 for <code>net8.0</code>, C# 13 for
      <code>net9.0</code>.</p>
      <p>Source files are included by <strong>globbing</strong>: every <code>.cs</code> file under the project folder compiles
      unless excluded. That removed the merge conflicts, but it also means a stray file in a subfolder is silently part of the
      build.</p>
      <p>At scale, the real power is in files beside the projects. <code>Directory.Build.props</code> is imported automatically
      by every project beneath it, so one file can enforce nullable, analysers and warnings across fifty projects.
      <code>Directory.Packages.props</code> enables <strong>central package management</strong> — one version per package for
      the whole repository, which is why the reference above has no version. <code>global.json</code> pins the SDK.</p>
      <p>The interviewer is probing whether you treat the project file as reviewable configuration, and whether you know that
      the IDE, the CLI and CI all run the same MSBuild evaluation — so "builds locally but not in CI" usually means a different
      SDK or an unpinned setting.</p></details>''',
}, mistakes='''      <tr><td>Timing code in a Debug build</td><td>The JIT generates unoptimised, debuggable code, so the numbers mean nothing</td><td>Measure Release builds with BenchmarkDotNet</td></tr>
      <tr><td>No <code>global.json</code> in the repository</td><td>Machines and CI build with different SDKs and analyser rules</td><td>Pin the SDK version</td></tr>
      <tr><td>Package versions scattered across project files</td><td>Version drift and conflicting transitive dependencies</td><td>Central package management in <code>Directory.Packages.props</code></td></tr>
      <tr><td>Targeting <code>netstandard2.0</code> for code only modern apps use</td><td>Loses newer APIs and performance overloads</td><td>Target <code>net8.0</code> or later unless Framework consumers exist</td></tr>
      <tr><td>Staying on a release past its end of support</td><td>No more security patches</td><td>Track support dates and upgrade on schedule</td></tr>
      <tr><td>A project folder nested inside another project's folder</td><td>The outer project also compiles the inner project's files</td><td>Sibling folders, or exclude with <code>Compile Remove</code></td></tr>
      <tr><td>Deploying a framework-dependent app to a host without the runtime</td><td>The app fails to start</td><td>Install the runtime in the image, or publish self-contained</td></tr>
      <tr><td>Disabling tiered compilation to fix warm-up</td><td>Slower startup and no Dynamic PGO</td><td>ReadyToRun, or warm up before taking traffic</td></tr>''',
takeaways='''      <li><strong>Roslyn produces IL and metadata; the JIT produces machine code.</strong></li>
      <li><strong>Metadata makes assemblies self-describing.</strong></li>
      <li><strong>A method is JIT-compiled on its first call, then its entry point is patched.</strong></li>
      <li><strong>The server and desktop CLR compiles IL before running it; it does not interpret.</strong></li>
      <li><strong>Tiered compilation starts fast and re-optimises hot methods.</strong></li>
      <li><strong>Dynamic PGO uses observed runtime types to devirtualise and inline.</strong></li>
      <li><strong>Measure Release builds, after warm-up.</strong></li>
      <li><strong>.NET Framework 4.8.1 is the end of the Framework line.</strong></li>
      <li><strong>.NET 5 dropped "Core"; even-numbered releases are LTS.</strong></li>
      <li><strong>.NET Standard is an API specification, not a runtime.</strong></li>
      <li><strong><code>Directory.Build.props</code> and central package management keep many projects consistent.</strong></li>
      <li><strong>Pin the SDK with <code>global.json</code> so every machine builds the same way.</strong></li>''')

apply("tutorials/dotnet/inheritance.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> Explain <code>virtual</code>, <code>override</code>, and <code>abstract</code>, and why C# requires the <code>override</code> keyword.</summary>
      <p><code>virtual</code> gives a method a <strong>slot in the type's method table</strong> with a default implementation.
      <code>override</code> puts a different implementation into that slot for the derived type. <code>abstract</code> declares
      the slot with no implementation at all, which forces the class to be abstract and every concrete subclass to fill it. A
      call through a base-typed reference reads the slot from the actual object's method table, so the most-derived override
      runs.</p>
      <p>In C#, methods are <strong>non-virtual by default</strong>, unlike Java. That is deliberate: a non-virtual call is
      direct and easy to inline, and every <code>virtual</code> member is a promise to subclasses that the base author must
      keep for as long as the class exists. Opting in keeps extension points explicit.</p>
      <p>The required <code>override</code> keyword exists mainly for <strong>versioning</strong>. Suppose you derive from a
      library class and add a method, and a later version of the library adds a virtual method with the same name:</p>
      <pre>  // your code, written against library v1
  public class FancyWidget : Widget { public void Refresh() { ... } }

  // library v2 adds a virtual member with the same name
  public class Widget
  {
      public virtual void Refresh() { ... }
      public void Render() { Refresh(); }
  }

  // FancyWidget.Refresh does NOT become an override: warning CS0114,
  // and Widget.Render() still calls Widget.Refresh().</pre>
      <p>In a language where overriding is implicit, your method would silently become an override, and the base class would
      start calling code that was never written for it. In C#, behaviour does not change until you decide, by writing
      <code>override</code> or <code>new</code>. The keyword also catches mistakes in the other direction: an
      <code>override</code> with no matching virtual member — a typo, or a wrong parameter type — is error CS0115.</p>
      <p>Interviewers are probing two things: whether you know the dispatch mechanism, and whether you can explain the
      <em>why</em> — safe evolution of base classes — rather than just the syntax.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What is polymorphism, and what does it let you do that you couldn't otherwise?</summary>
      <p>Polymorphism means <strong>one call site, many behaviours</strong>, with the behaviour chosen by the object's runtime
      type. When payroll code calls <code>e.CalculatePay()</code> on an <code>Employee</code> variable, the runtime dispatches
      to the actual object's override, so the calling code never needs to know which kinds of employee exist.</p>
      <p>What it lets you do is <strong>add new types without editing existing code</strong>. The alternative is a type check
      repeated wherever behaviour differs — <code>if (e is SalariedEmployee) ... else if (e is Contractor) ...</code> — and
      every new subtype means finding and updating each one, with the compiler unable to tell you which you missed. With a
      virtual method, the new subtype carries its own behaviour and the payroll loop is untouched.</p>
      <p>A classic follow-up tests whether you can separate <strong>overriding</strong> from <strong>overloading</strong>:</p>
      <pre>  void Print(object o) =&gt; Console.WriteLine("object");
  void Print(string s) =&gt; Console.WriteLine("string");

  object o = "hi";
  Print(o);                          // "object": overloads are chosen by STATIC type
  Console.WriteLine(o.ToString());   // "hi": overrides are chosen by RUNTIME type</pre>
      <p>Dispatch has a cost — an indirect call that normally cannot be inlined — but modern .NET recovers much of it. The JIT
      <strong>devirtualises</strong> calls when it can prove the type, for example on a <code>sealed</code> class, and Dynamic
      PGO inlines the common implementation behind a cheap type check.</p>
      <p>The senior nuance is the <strong>trade-off</strong>. Polymorphism makes adding a new <em>type</em> cheap and adding a
      new <em>operation</em> expensive, because every subtype must implement it. A switch expression over a closed set of
      records is the opposite: new operations are cheap, new types are not. Choose based on which axis your domain changes
      along. The interviewer is looking for that judgment, not just the definition.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> When would you choose an interface over an abstract class, and vice versa? Give the combined pattern.</summary>
      <p>The real question is <strong>what you are promising, and to whom</strong>. An interface promises callers a capability
      and says nothing about how it is built. An abstract class also gives implementers a partial implementation and shared
      state, at the price of their only base class.</p>
      <p>Choose an <strong>interface</strong> when unrelated types may provide the capability, when a type needs several
      contracts, when <strong>structs or records</strong> must implement it (structs cannot derive from classes), or when the
      abstraction is a seam for dependency injection and testing. Choose an <strong>abstract class</strong> when a genuine
      is-a family shares fields, constructor logic and a fixed algorithm with a few variable steps.</p>
      <p>Modern C# has blurred the line in two ways, and knowing the caveats is the senior part. <strong>Default interface
      methods</strong> let you add a member without breaking implementers, but they cannot hold instance state, and a default
      member is reachable only through the interface type, not through a variable typed as the class. <strong>Static abstract
      members</strong> (C# 11) let an interface require static operations — <code>T.Parse</code>, operators,
      <code>T.Zero</code> — which no abstract class can express.</p>
      <p>The combined pattern puts the contract in the interface and the shared plumbing in an optional base:</p>
      <pre>  public interface INotificationSender
  {
      Task SendAsync(Message m, CancellationToken ct);
  }

  public abstract class NotificationSenderBase : INotificationSender
  {
      public async Task SendAsync(Message m, CancellationToken ct)
      {
          Validate(m);                        // fixed steps, shared
          await SendCoreAsync(m, ct);         // the step that varies
      }
      protected abstract Task SendCoreAsync(Message m, CancellationToken ct);
      private static void Validate(Message m) { ... }
  }

  public sealed class EmailSender : NotificationSenderBase { ... }
  public sealed class SmsSender(ISmsGateway gateway) : INotificationSender { ... }</pre>
      <p>Consumers and the DI container only ever see <code>INotificationSender</code>. <code>EmailSender</code> uses the base
      to avoid boilerplate; <code>SmsSender</code> does not fit it and implements the interface directly. That freedom is the
      point: the base is a convenience for implementers, never a requirement imposed on consumers.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> Explain "composition over inheritance" with the classic bird/duck example. What symptoms tell you a hierarchy is wrong?</summary>
      <p>Inheritance fixes behaviour along <strong>one axis, at compile time</strong>, and real domains vary along several. For
      birds, how a bird moves and how it feeds vary independently, and a class hierarchy makes every subclass commit to its
      base's assumptions about both.</p>
      <p>It starts innocently: <code>Bird</code> has a virtual <code>Fly()</code>. Then <code>Penguin</code> overrides it to
      throw, and <code>RubberDuck</code> overrides <code>Fly()</code> and <code>Eat()</code> to do nothing. Now any code that
      loops over birds calling <code>Fly()</code> crashes or silently does the wrong thing — the subtype is no longer
      substitutable for its base, a Liskov violation. Fixing it with more inheritance leads to a <strong>combinatorial
      explosion</strong>:</p>
      <pre>  // inheritance: one class per COMBINATION
  FlyingHuntingBird, FlyingForagingBird, SwimmingHuntingBird, SwimmingForagingBird, ...
  // movement kinds × feeding kinds = classes (3 × 3 = 9, and multiplying)

  // composition: one class per PART, combined at construction
  new Bird(new Flying(),     new Hunting());      // eagle
  new Bird(new Swimming(),   new Hunting());      // penguin
  new Bird(new Stationary(), new NoFeeding());    // rubber duck
  // movement kinds + feeding kinds = parts (3 + 3 = 6)</pre>
      <p>With composition, <code>Bird</code> <strong>has</strong> an <code>IMovement</code> and an <code>IFeeding</code>.
      Nothing is disabled, every combination is valid by construction, and behaviour can even be swapped at runtime.</p>
      <p>The symptoms of a wrong hierarchy: overrides that throw <code>NotSupportedException</code>; empty overrides; boolean
      flags on the base such as <code>CanFly</code>; <code>if (this is Penguin)</code> checks inside base code; subclasses
      that exist only to set a few values; a base that changes whenever one subtype needs something; and tests that must
      build a deep chain to exercise one method.</p>
      <p>Composition has costs — more small types, more wiring, one more hop when debugging — but primary constructors and DI
      make it cheap in modern C#. The interviewer wants you to name the symptoms and describe the refactor: extract an
      interface for the varying behaviour, inject it, delete the overrides.</p></details>''',
}, mistakes='''      <tr><td>Calling a virtual method from a base constructor</td><td>The override runs before the derived constructor body, on unset fields</td><td>Keep constructors non-virtual; use a factory or an explicit initialise step</td></tr>
      <tr><td>Forgetting <code>base.Method()</code> in an override that should extend</td><td>Base cleanup or configuration is skipped, e.g. in <code>Dispose(bool)</code></td><td>Call the base, or expose a separate hook for subclasses</td></tr>
      <tr><td>A derived method with a slightly different signature</td><td>It becomes an overload, so base-typed calls never reach it</td><td>Write <code>override</code> so the compiler checks the signature</td></tr>
      <tr><td>Calling a default interface method through the class type</td><td>Compile error — defaults are reachable only through the interface</td><td>Call it via the interface, or implement it on the class</td></tr>
      <tr><td>Passing structs as interface parameters on hot paths</td><td>Each call boxes the struct</td><td>A generic method constrained to the interface</td></tr>
      <tr><td>Type-check chains over subclasses in an open hierarchy</td><td>Every new subtype means hunting down each chain</td><td>Move the behaviour into a virtual method</td></tr>
      <tr><td>Protected mutable fields in a base class</td><td>Subclasses can break the base's invariants</td><td>Private fields behind protected members that enforce the rules</td></tr>
      <tr><td>Deriving from <code>List&lt;T&gt;</code> to customise <code>Add</code></td><td>Its methods are not virtual, so you can only hide them</td><td>Wrap a private list, or derive from <code>Collection&lt;T&gt;</code></td></tr>''',
takeaways='''      <li><strong>A virtual call reads a method-table slot chosen by the runtime type.</strong></li>
      <li><strong>C# methods are non-virtual unless the base author opts in.</strong></li>
      <li><strong>The required <code>override</code> keyword protects subclasses when a base library evolves.</strong></li>
      <li><strong>An <code>override</code> with no matching virtual member is a compile error.</strong></li>
      <li><strong>Overloads are chosen by static type; overrides by runtime type.</strong></li>
      <li><strong>Sealed types let the JIT devirtualise calls.</strong></li>
      <li><strong>Polymorphism makes new types cheap and new operations expensive.</strong></li>
      <li><strong>Default interface members are reachable only through the interface.</strong></li>
      <li><strong>Static abstract interface members express contracts no abstract class can.</strong></li>
      <li><strong>Composition needs one part per variation; inheritance needs one class per combination.</strong></li>
      <li><strong>A chain of type checks over subclasses is a missing virtual method.</strong></li>
      <li><strong>Never call virtual members from a constructor.</strong></li>''')

apply("tutorials/dotnet/linq.html", iq={
1: '''<details class="solution"><summary><strong>Q1 (Beginner):</strong> What is LINQ, and what are the two syntaxes?</summary>
      <p>LINQ is really <strong>three things working together</strong>: a library of extension methods —
      <code>Enumerable</code> for <code>IEnumerable&lt;T&gt;</code> and <code>Queryable</code> for
      <code>IQueryable&lt;T&gt;</code>; the language features that make those methods pleasant — lambdas, extension methods,
      type inference, anonymous types and expression trees; and an optional <strong>query syntax</strong> on top.</p>
      <p><strong>Method syntax</strong> chains the operators directly. <strong>Query syntax</strong> reads like SQL, and the
      compiler translates it mechanically into the same method calls before anything else happens:</p>
      <pre>  var q = from o in orders
          where o.Total &gt; 100
          orderby o.Date descending
          select new { o.Id, o.Total };

  // what the compiler actually emits:
  var q = orders
      .Where(o =&gt; o.Total &gt; 100)
      .OrderByDescending(o =&gt; o.Date)
      .Select(o =&gt; new { o.Id, o.Total });</pre>
      <p>Because it is a syntactic rewrite, the two forms have <strong>identical performance</strong>. The translation is also
      pattern-based: it works on any type with suitably shaped <code>Where</code> and <code>Select</code> methods, which is
      how the same syntax targets <code>IQueryable</code> and becomes SQL.</p>
      <p>Method syntax dominates in practice because query syntax has keywords for only some operators. <code>Count</code>,
      <code>Any</code>, <code>First</code>, <code>Take</code>, <code>Distinct</code> and <code>ToList</code> have none, so a
      query expression usually ends up in parentheses with method calls attached. Query syntax earns its place for
      <strong>joins, multiple <code>from</code> clauses and <code>let</code></strong>, where the method-syntax equivalent needs
      anonymous types to carry intermediate values from step to step.</p>
      <p>The interviewer is checking that you know query syntax is compile-time sugar, not a separate engine. A strong answer
      also shows you are current: recent releases keep adding operators, such as <code>DistinctBy</code>, <code>MinBy</code>
      and <code>Chunk</code> in .NET 6, and <code>CountBy</code>, <code>AggregateBy</code> and <code>Index</code> in
      .NET 9.</p></details>''',
2: '''<details class="solution"><summary><strong>Q2 (Beginner):</strong> What's the difference between <code>First</code>, <code>FirstOrDefault</code>, and <code>Single</code>?</summary>
      <p>The operators differ only in how they treat <strong>zero matches</strong> and <strong>more than one match</strong>:</p>
      <pre>                       0 matches      1 match      2+ matches
  First(p)             throws         returns it   returns the first
  FirstOrDefault(p)    default(T)     returns it   returns the first
  Single(p)            throws         returns it   throws
  SingleOrDefault(p)   default(T)     returns it   throws</pre>
      <p>Choosing between them is about <strong>what the data guarantees</strong>. <code>Single</code> encodes an invariant:
      there is exactly one. Use it for lookups by a unique key, where a second match means corrupt data, and the exception is a
      detector you want to fire. <code>First</code> means "any one of possibly many will do", and it is usually paired with an
      <code>OrderBy</code> so that "first" is well defined. Against a database, <code>First</code> without an ordering returns
      an <strong>arbitrary row</strong>, because SQL guarantees no default order.</p>
      <p>There is a cost difference. To prove uniqueness, <code>Single</code> must keep looking after it finds a match: in
      memory it scans the rest of the sequence, and EF Core translates it to <code>TOP(2)</code> rather than
      <code>TOP(1)</code>. That is almost always worth paying where uniqueness matters.</p>
      <p>The <code>OrDefault</code> variants have a trap with value types. <code>default</code> is <code>0</code>,
      <code>false</code> or an all-zero struct, which can be a legitimate value, so you cannot tell "missing" from "zero".
      Since .NET 6 there are overloads that take an explicit fallback, such as <code>FirstOrDefault(p, -1)</code>, and with
      nullable reference types enabled the result is annotated as nullable, so the compiler warns if you dereference it
      unchecked.</p>
      <p>The interviewer is probing whether you choose by intent. A <code>First</code> that throws "Sequence contains no
      elements" is not a bug in itself; it is correct when absence really is exceptional.</p></details>''',
3: '''<details class="solution"><summary><strong>Q3 (Mid):</strong> Explain deferred execution and a bug it commonly causes.</summary>
      <p>An operator such as <code>Where</code> does not filter anything. It returns an <strong>iterator object</strong> that
      holds the source and the lambda. Work happens only when something calls <code>MoveNext</code> — a <code>foreach</code>,
      or an operator that needs values. Chained operators nest these iterators, so enumeration pulls each element through the
      whole pipeline.</p>
      <p>It helps to know three categories. <strong>Streaming</strong> operators such as <code>Where</code> and
      <code>Select</code> handle one element at a time. <strong>Buffering</strong> operators such as <code>OrderBy</code>,
      <code>GroupBy</code> and <code>Reverse</code> are still deferred, but the first <code>MoveNext</code> consumes the entire
      source. <strong>Immediate</strong> operators — <code>ToList</code>, <code>Count</code>, <code>First</code>,
      <code>Sum</code>, <code>Any</code> — run the pipeline as soon as they are called.</p>
      <p>A common production bug is a query that <strong>outlives the resource it reads from</strong>:</p>
      <pre>  IEnumerable&lt;string&gt; ActiveNames()
  {
      using var db = new ShopContext();
      return db.Customers.Where(c =&gt; c.Active).Select(c =&gt; c.Name);
  }   // db is disposed here, but no query has run yet

  foreach (var name in ActiveNames())   // the query runs NOW, on a disposed context
      Console.WriteLine(name);          // ObjectDisposedException</pre>
      <p>The same shape appears with files and streams, and it sits beside the other classics: enumerating twice does the work
      twice, captured variables are read at enumeration time, and objects created in a <code>Select</code> are <strong>new
      objects on every enumeration</strong>, so changes made to them in one pass are gone in the next. The fix is to
      <strong>materialise at the boundary</strong>: return <code>ToList()</code> as an <code>IReadOnlyList&lt;T&gt;</code>
      before the resource goes away.</p>
      <p>Deferral exists for good reasons: you can build a query in steps, add filters conditionally, stream huge sequences,
      stop early, and let <code>IQueryable</code> turn a whole chain into one SQL statement. The interviewer wants to see that
      you can predict <em>when</em> code runs, and that you treat a method boundary as the place to resolve
      laziness.</p></details>''',
4: '''<details class="solution"><summary><strong>Q4 (Mid):</strong> What's the difference between <code>IEnumerable</code> and <code>IQueryable</code>, and why does it matter for EF Core?</summary>
      <p>The difference starts in the signatures:</p>
      <pre>  // System.Linq.Enumerable
  IEnumerable&lt;T&gt; Where&lt;T&gt;(this IEnumerable&lt;T&gt; source, Func&lt;T, bool&gt; predicate);

  // System.Linq.Queryable
  IQueryable&lt;T&gt;  Where&lt;T&gt;(this IQueryable&lt;T&gt; source, Expression&lt;Func&lt;T, bool&gt;&gt; predicate);</pre>
      <p>The same lambda text compiles to one of two things. For <code>Enumerable</code> it becomes a <strong>delegate</strong>:
      compiled code that runs per element in your process. For <code>Queryable</code> it becomes an <strong>expression
      tree</strong>: a data structure describing the code. An <code>IQueryable</code> carries that tree and a provider; each
      operator adds a node, and when the query is enumerated, EF Core translates the whole tree into SQL, turns captured
      variables into parameters, and runs it in the database.</p>
      <p>The crucial point is that <strong>the static type of the source picks the overload</strong>, at compile time. So the
      classic trap often hides in a harmless-looking signature: a repository method declared as <code>IEnumerable&lt;Order&gt;
      GetOrders() =&gt; _db.Orders;</code>. Every caller's <code>.Where(...).Take(10)</code> now binds to
      <code>Enumerable</code>, and the SQL sent is a bare <code>SELECT</code> of the whole table, filtered in memory. Changing
      the return type to <code>IQueryable&lt;Order&gt;</code> makes the same calling code produce <code>SELECT TOP(10) ...
      WHERE</code>.</p>
      <p>Since EF Core 3.0, an expression the provider cannot translate <strong>throws</strong> instead of silently running on
      the client. The exception is the final projection: a C# method call in the last <code>Select</code> runs in memory after
      the rows arrive. To see what you are really sending, call <code>ToQueryString()</code> on the query or enable EF Core's
      SQL logging.</p>
      <p>There is a design trade-off behind this. Exposing <code>IQueryable</code> outside the data layer lets callers compose
      efficient queries, but it leaks persistence: callers can build queries you never tested or indexed, and enumerate after
      the context is gone. Returning a materialised <code>IReadOnlyList&lt;T&gt;</code> from intention-revealing methods is
      safer. The interviewer is probing whether you understand that the type, not the syntax, decides where the code
      runs.</p></details>''',
}, mistakes='''      <tr><td>Returning a deferred query from a method that disposes its context</td><td><code>ObjectDisposedException</code> when the caller enumerates</td><td>Materialise before the resource is disposed</td></tr>
      <tr><td>Returning <code>IEnumerable&lt;T&gt;</code> over a <code>DbSet</code></td><td>Every later operator runs in memory after a full-table read</td><td>Return <code>IQueryable&lt;T&gt;</code> inside the data layer, or materialised results</td></tr>
      <tr><td><code>First</code>, <code>Skip</code> or <code>Take</code> on an unordered database query</td><td>Arbitrary rows and unstable paging</td><td><code>OrderBy</code> with a unique tiebreaker first</td></tr>
      <tr><td>Chaining a second <code>OrderBy</code> as a tiebreak</td><td>The last <code>OrderBy</code> becomes the primary sort</td><td><code>ThenBy</code></td></tr>
      <tr><td><code>FirstOrDefault</code> on value types to detect absence</td><td><code>0</code> or <code>false</code> is indistinguishable from "missing"</td><td>The fallback overload, a nullable projection, or <code>Any</code></td></tr>
      <tr><td><code>.ToList().ForEach(...)</code> just to loop</td><td>Allocates a copy of the sequence for nothing</td><td>A plain <code>foreach</code></td></tr>
      <tr><td><code>list.Contains(x)</code> inside a <code>Where</code> over another large list</td><td>Quadratic time</td><td>Build a <code>HashSet&lt;T&gt;</code> first</td></tr>
      <tr><td><code>Distinct()</code> on a class without value equality</td><td>Compares references, so nothing is removed</td><td><code>DistinctBy</code>, a record, or implemented equality</td></tr>''',
takeaways='''      <li><strong>Query syntax is compile-time sugar for the same method calls.</strong></li>
      <li><strong>Many operators have no query keyword, so method syntax dominates.</strong></li>
      <li><strong><code>Single</code> proves uniqueness by looking for a second match.</strong></li>
      <li><strong><code>First</code> without <code>OrderBy</code> returns an arbitrary database row.</strong></li>
      <li><strong>Streaming operators pull one item at a time; <code>OrderBy</code> and <code>GroupBy</code> buffer the whole source.</strong></li>
      <li><strong>Operators that return a value or a collection run immediately.</strong></li>
      <li><strong>Resolve laziness before the resources a query depends on are disposed.</strong></li>
      <li><strong>The static type of the source decides whether <code>Enumerable</code> or <code>Queryable</code> runs.</strong></li>
      <li><strong><code>IQueryable</code> lambdas become expression trees that a provider translates.</strong></li>
      <li><strong>Returning <code>IEnumerable</code> over a <code>DbSet</code> moves every later operator into memory.</strong></li>
      <li><strong>Inspect generated SQL with <code>ToQueryString</code> or EF Core logging.</strong></li>
      <li><strong>Use <code>ThenBy</code> for tiebreaks; a second <code>OrderBy</code> becomes the primary sort.</strong></li>''')
