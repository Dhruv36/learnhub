# LearnHub — Project Status

**Live:** https://dhruv36.github.io/learnhub/ · **Repo:** github.com/Dhruv36/learnhub (GitHub Pages, main branch → auto-deploy on push)

A GeeksforGeeks/W3Schools-style learning site: plain HTML/CSS/JS, no build step. Goal: deep, curated, mid/senior-interview-ready content the engineering community can use as a single reference. Every track = ~20 lessons (Basics → Ultra-Advanced) + **10 quizzes × 20 questions = 200 Qs** with per-answer explanations.

---

## ▶️ RESUME HERE (last updated 2026-08-21)

**Last completed:** ✅ **AWS v4 (track 17) — COMPLETE.** All **20 lessons** at v4 depth (54–90KB, every
one `det=12 ex=6`) across 6 sections, both end-of-track chores done, and the **quiz bank rewritten to the
v4 curriculum** (200 fresh questions, `10 200 0`, 0 duplicate stems, de-skewed 65/66/69). Whole track
passes `python validate.py tutorials/aws` with **0 errors and 0 warnings** (23 files); pushed & live.
The two closing lessons: `resilience-dr.html` (**HA survives a component dying, DR restores destroyed
state** — Multi-AZ covered 2 of 14 real incidents and replicated an accidental DELETE in 11 ms; RTO/RPO
derived from downtime cost and tiered; a designed 4h RTO measured **9h47m** then **52 min** after ~3
engineer-days; **"available" ≠ usable** — a 2 TB restore served 18× latency for 40 more minutes; restores
lose the endpoint, alarms, Multi-AZ and TTL settings; Vault Lock compliance + Object Lock in a separate
account; **RPO is lag at failure** — Aurora Global p50 310 ms but 21.7 s in the batch window; DynamoDB
global tables' silent last-writer-wins; S3 CRR has no ordering; **static stability** and the four
control-plane defects that blocked drill 1; failover = health check + TTL + JVM cache + pool =
**7m12s vs a 90 s claim**, fixed to 1m35s; ARC at ~$2,190/mo; cells/shuffle sharding 3.6%; failback and
the 52 → 71 min announced-vs-unannounced delta) · `scaling-patterns.html` (**USL: throughput peaks then
DECLINES** — 8,760 req/s at 16 instances, 7,900 at 24, from a shared sequence row; **the constraint always
moves**; Little's Law for pool sizing; the five statelessness pins and idempotency as the enabling
property; **the ASG control loop measured 4m40s → 1m25s tuned** and still cannot serve a 30 s spike;
CPU is the wrong metric for I/O-bound work (34% CPU, p99 4.2 s, zero scaling activities);
`default_instance_warmup` ends flapping; **a queue adds patience, not capacity** — a 400/min deficit
became a **4.1M backlog** that aged out of retention; backlog-per-instance = target ÷ processing time;
**retry storms** turning 4% errors into 3× load; **load shedding: 6.1% rejected in 2 ms held p99 at
310 ms and goodput at 94%** vs 14.2 s and 61%; connections, replica lag, TTL jitter and single-flight,
the 1,000 WCU per-partition ceiling at 6% utilisation; quotas, cells, and the known-spike playbook).

**Previously:** ✅ **Kubernetes v4 (track 16) — COMPLETE.** All **22 lessons** rebuilt from 12 v3
lessons (~10KB) to v4 depth (49–57KB, every one `det=12 ex=6`) across 6 sections, + **quiz bank
rewritten to the v4 curriculum** (200 fresh questions, `10 200 0`, 0 duplicate stems, de-skewed
69/78/53). Whole track passes `python validate.py tutorials/kubernetes` with **0 errors** (28 files);
pushed & live.

*§1 Foundations ×5* — `index.html` (**level-triggered, not edge-triggered**; the scheduler writes one
field; control-plane outage = "cannot change", not "everything down"; frozen endpoints black-holed
11/30 requests; deletion is a request) · `objects-yaml.html` (three-way merge, **SSA field
ownership**, HPA/Git conflict = 23 scale events in 10 min, `--dry-run=server`) · `pods.html`
(namespace sharing proven, **native sidecars: Job 30min → 14s**, bare pods never rescheduled) ·
`deployments.html` (**surge arithmetic measured 5 exist/3 ready**, ConfigMap change rolls out
nothing, no auto-rollback after ProgressDeadlineExceeded) · `scheduling.html` (**requests not usage**,
the hidden 300s toleration ≈341s to evict, spread 2/2/1 vs anti-affinity 3 Running 2 Pending)
*§2 Networking ×4* — `services.html` (**ClusterIP has no process**; per-connection balancing
200/0/0/0; `Local` gave 133/134/133 vs 400; preStop 22 → 0 dropped) · `dns-discovery.html`
(**ndots:5 = 10 queries, 48ms → 7ms**; the 5.000s conntrack race; hostNetwork DNS trap;
publishNotReadyAddresses deadlock) · `ingress-gateway.html` (Ingress is data not a proxy; **Prefix
matches elements — /api ≠ /apifoo**; 1MB body-size default; Gateway API role split) ·
`network-policy.html` (**one extra dash = OR**, hostile ns granted itself access; ClusterIP allow does
nothing; **silent no-op on Flannel**)
*§3 Config & State ×4* — `config-secrets.html` (Secret read from etcd; **env never / volume ~60s /
subPath never**; create pods = get secrets) · `storage.html` (**reclaimPolicy Delete destroys the
disk**; WaitForFirstConsumer zone trap; **RWO = one NODE, two writers proven**; CSI attach limits) ·
`statefulsets.html` (identity survives rescheduling; ordered rollout blocks; **partition canary**;
PVCs outlive everything; force-delete split brain) · `jobs-cronjobs.html` (**backoffLimit counts pods
not restarts**; **100-miss trap kills a CronJob permanently**; podFailurePolicy for spot; alert on
last success)
*§4 Scaling & Reliability ×4* — `probes.html` (**a probe may only test what its remedy can fix** —
liveness on the DB restarted 4/4 replicas, 137 failures → 0; startup probe: ready 94s AND 11s
detection) · `resources.html` (QoS eviction by usage-vs-request; **62% avg CPU at every quota while
p99 went 41→96→488ms**; LimitRange before ResourceQuota) · `autoscaling.html` (**utilisation is % of
the REQUEST**; 300s scale-down window; HPA+VPA oscillation 3→23 replicas; CA scale-up 194s → 12s with
balloons) · `disruptions.html` (**PDBs are voluntary-only**; eviction 429 vs delete; `--disable-eviction`
bypasses every PDB; preStop 22 → 0)
*§5 Security ×2* — `rbac.html` (**there is no User object**; create pods → every Secret AND any SA's
permissions; escalate/bind/impersonate; projected tokens die with the pod) · `pod-security.html`
(**hostPath read other pods' Secrets from a create-pods-only SA**; PSA validates PODS not Deployments;
**mutation runs before validation**)
*§6 Operating ×3* — `helm.html` (**release ledger in cluster Secrets**; `--set 1.20` → `1.2`;
pending-upgrade wedges every deploy; **crds/ never upgraded**) · `gitops.html` (**Sync ≠ Health**;
prune + empty render = everything deleted; **kubectl fix has a 3-minute half-life**) ·
`debugging-production.html` (**events expire in ~1h**; status over spec; ephemeral containers for
distroless; layered network test; event flood = diagnosis)

Also: the five v3 files orphaned by the nav split (`pods-deployments`, `services-ingress`,
`probes-resources`, `statefulsets-storage`, `rbac-network`) are now **redirect stubs**.

⚠️ **Scaffolding reminder:** any newly-copied `quiz.html` must be checked for BOTH the stale
`← CSS Track` link AND mojibake (`·`, `→` — double-encoded UTF-8) before committing.

**✅ AWS v4 (track 17) — COMPLETE** — `tutorials/aws/`, 12 v3 lessons (~12KB) rebuilt into
**20 lessons at v4 depth** (54–90KB, `det=12 ex=6`) across 6 sections. Per-lesson findings:

*§1 Foundations ×4* — ✅ `index.html` (**the shared-responsibility line moves per service**; AZ *names*
are randomised per account so cross-account placement must use **Zone IDs**; the `us-east-1` control-plane
dependency for IAM/Route 53/CloudFront/ACM; **the account is the blast radius**; **SCPs only subtract** —
an "Allow s3:*" SCP grants nobody anything; quotas are per-account *per-Region* and a new account gets
**5 vCPUs**; throttling, jittered retries and eventual consistency; the day-one baseline) ·
✅ `iam-basics.html` (**explicit Deny always wins** — AdministratorAccess did not override a one-line
inline Deny; **cross-account needs BOTH sides**, and SSE-KMS needs a third grant on the key policy;
`NotAction`+`Allow` grants every future service; **`iam:PassRole` on `*` + `lambda:CreateFunction` = admin**,
demonstrated creating a backdoor user from a role explicitly denied `iam:CreateUser`; confused deputy via
`aws:SourceArn`/`sts:ExternalId`; ABAC + **permission boundaries**, with an SCP enforcing the tag at
creation; Access Analyzer found **243 services granted and never used**)
✅ `iam-deep-dive.html` (**AssumeRole returns a new principal**, two policies per role; the **silent 1-hour
role-chaining cap** that killed a 4-hour nightly job — `--duration-seconds 14400` returned a 1-hour expiry;
**IMDSv1 SSRF credential theft** demonstrated end to end, blocked by `--http-tokens required` +
`--http-put-response-hop-limit 1`; **an audience-only GitHub OIDC trust policy is assumable by every repo on
GitHub** — pin `sub` to `repo:acme/shop:environment:production`; session policies as break-glass ceilings;
revoking un-deletable temporary credentials via **`aws:TokenIssueTime`** while the workload recovers on its
next refresh; the credential resolution chain and `aws configure list`) ·
✅ `billing-cost.html` (four billing shapes; **group by USAGE TYPE, not service** — a 4× S3 bill was PUTs,
storage barely moved; **Savings Plans commit to spend** and break even only at utilisation ≥ (1 − discount),
so sizing on the average instead of the floor cost **$3,066/month more than no plan**; transfer priced **per
direction** — a **free** S3 gateway endpoint replaced **$181/month** of NAT processing, and 196 TB of cross-AZ
traffic was one API returning **412 KB to answer a boolean**; colder S3 tiers charge per object, impose a
**128 KB minimum billable size** and minimum durations → a measured **93-month payback**, fixed by aggregating
to Parquet not by tiering; the **U-shaped Lambda memory curve** where 1024 MB is cheapest AND 10× faster than
128 MB; CloudWatch Logs ingestion at $0.50/GB exceeding the compute; **cost allocation tags are NOT
retroactive**; billing lags 24h so quotas bound a runaway, budgets only describe one)

*§2 Networking ×3* — ✅ `vpc-networking.html` (**a VPC is a routing domain, not a device**; CIDRs immutable and
overlap makes peering permanently impossible; **5 reserved IPs per subnet** so a /28 gives 11; **"public" is a
route to an IGW *plus* a public IP**, and an unassociated subnet silently inherits the **main** route table;
SGs stateful/allow-only/unioned and **referencing other SGs** so rules survive scaling — plus **tracked flows
survive rule revocation** and the untracked-flow inversion; NACLs stateless and the **ephemeral-port trap**
diagnosed from an ACCEPT/REJECT pair in flow logs; **EKS caps at 29 pods/m5.large** and `FailedCreatePodSandBox`
is a *scheduling success* — **prefix delegation → 110 pods**, no renumbering; five faults, one identical
timeout, and a fixed read-only debugging order)
✅ `connectivity.html` (**network vs service reachability** is the question that picks the technology;
**peering is non-transitive and the API *refuses* the route** — same rule blocks a peer's IGW/NAT/gateway
endpoints; n(n−1)/2 mesh growth; **create a TGW with default association AND propagation disabled** or the
segmentation does not exist; TGW route tables as an **isolation proof diffed in CI and tested to fail**, plus
an SCP so drift cannot happen; **$0.05/hr per attachment is not free** ($2,295/mo for 30 + 60 TB); **appliance
mode** for stateful inspection; **PrivateLink proven between two VPCs both on `10.0.0.0/16`** with
`ip route get` showing traffic never leaves; **`--private-dns-enabled` is a VPC-wide DNS change** that removes
the public fallback; **DX carries NO encryption** and one circuit has no SLA; **hybrid DNS is two separate
systems** — inbound *and* outbound resolver endpoints, both UDP and TCP/53) ·
✅ `edge-dns.html` (**a CNAME can never sit at the apex** → the alias record, free + health-aware; **lower TTLs
the day BEFORE**; **weighted DNS splits resolver answers not requests** — a 5% weight measured **3.4% one day,
17% another** — so canary at the ALB with weighted target groups; **failover measured at 47s best case and
NEVER on a default JVM** (`networkaddress.cache.ttl=-1`); **a health check on the LB reports healthy while
every target fails**, and a deep check on a *shared global* dependency turns a partial outage into a total one;
**NLB client-IP preservation is OFF by default for IP targets over TCP/TLS**; **ALB cross-zone is free+always
on, NLB's is off+billable**; **backend keepalive must EXCEED the ALB idle timeout** — Node's 5s default gives
502s with no app log, and `headersTimeout` must exceed `keepAliveTimeout`; the 5xx decoder keyed on
`target_status_code="-"` + `target_processing_time`; **CloudFront cache key 0.3% → 94.1%** by moving fields to
the *origin request* policy, with over-collapsing named as the dangerous direction)
*§3 Compute ×3* — ✅ `ec2-compute.html` (**a vCPU is a hyperthread** — 4.72× scaling vs Graviton's 7.90×, making
a 15% price gap an **88% price/perf gap**; the two *silent* burstable failures — **T2 throttles to 20%** with p99
178→**4,241 ms** while the graph looks idle, **T3 bills $884/mo of surplus** with no symptom; **gp2 IOPS tied to
size** and the burst cliff measured **2,987→301**, while the *instance's* EBS baseline is the real ceiling; Nitro
`/dev/nvme*` breaking fstab; **snapshots restore LAZILY** — 1,204 vs 11,890 IOPS, **an hour to reach baseline
under load**, and FSR costs ~$547/mo per snapshot per AZ; **`HealthCheckType: EC2` never replaces a dead app** —
capacity leaked 6→3 while desired still read 6 — and fixing it without a grace period gives an infinite boot
loop; **target tracking oscillates when time-to-serve (252 s) exceeds the evaluation window (180 s)** — 4→19→5→17,
fixed with `--default-instance-warmup` + warm pools, cutting p99 **and** instance-hours together; **CloudWatch has
no memory metric**) ·
✅ `containers.html` (**ECS/EKS are orchestrators, Fargate is a capacity provider** — "ECS or Fargate?" is a
category error; **execution role = the agent, task role = your code**, proven from the container credential
endpoint which serves *only* the task role; **`awsvpc` ENI density capped an m5.large at 2 tasks with 45% CPU
idle** → 10 with trunking — **density is an addressing limit before a resource limit**; Fargate's **fixed
CPU/memory menu** forcing wasted vCPU on memory-heavy work; **the utilisation crossover is ~61%**, and a cluster
measured at **17% used made Fargate 55% cheaper**; IRSA `sub` pinning; **EKS access entries replaced `aws-auth`**
— and the **node-group role must be recreated as `EC2_LINUX` before the one-way switch** or every node goes
NotReady; ECR pull-through cache for the **Docker Hub per-IP limit that fails deploys while scaling out**;
**exit 137 with NO OutOfMemoryError in the log = a JVM sized to the whole cgroup limit**) ·
✅ `lambda-serverless.html` (**INIT runs once per environment, the handler once per invocation** — 412→**71 ms**
warm, and the same reuse **leaks one user's state to the next**; **concurrency = rps × duration**, reserved
concurrency is a **floor AND a ceiling** and **0 disables the function**; the shared account pool means **any
function's bug is every function's outage** — 947 of 1,000 held by a thumbnailer; **async retries twice then
silently drops** (~2,996 events/week lost); **one poison record blocks a shard for 24 h** with **IteratorAge
growing LINEARLY** — `BisectBatchOnFunctionError` isolated it in 15 splits; **Lambda vs RDS is a structural
mismatch** — 387 connections vs 90, and raising `max_connections` traded refusals for **8.4-second queries**;
**API Gateway's 29 s wall returns 504 while the function completes and bills** — 47 customers charged twice,
fixed **idempotency-first**; SnapStart's shared-snapshot uniqueness trap)
*§4 Data ×4* — ✅ `s3.html` (**no folders** — `CommonPrefixes` proven synthetic, `mv` = COPY+DELETE, LIST a
billion objects = **1 M requests / $5 / 5.5 h**; **strong consistency since Dec 2020** and **random prefixes
obsolete since 2018**, both still circulating; per-prefix limits driven into `503 SlowDown` — **3,204 → 25,500
req/s across 8 prefixes**, adaptive retries absorbing a 31% throttle rate; **`BlockPublicPolicy` REFUSES TO
STORE** the policy being debugged; **DELETE writes a marker so deleting makes the bucket bigger** — console and
`s3 ls` hid **10.2 TB** that CloudWatch and the invoice both counted; the 4-clause lifecycle rule **14.0 → 2.6
TB (81%)**; **Bucket Keys $577 → $3.71/mo**; **compliance-mode Object Lock irreversible by root**) ·
✅ `rds-aurora.html` (**Multi-AZ is availability, not scale** — no standby endpoint, not even listed, and it
costs the same as single-AZ+replica while buying the opposite thing; failover **38 s AWS / 49 s Node / NEVER on
a default JVM / 9 s behind RDS Proxy**; replica lag **0/200 failures idle, 187/200 under write load**;
**Aurora ships redo log records not pages** → **1,841 s vs 21 ms** lag and **47 min vs 4.6 min** to add a
replica with zero writer impact; **retention 0 silently disables PITR**; **a restore returns a NEW hostname,
default parameter group, default SG, no Multi-AZ** — real RTO **32 min vs a runbook claiming 11**; Performance
Insights wait events picking a **$0 index worth 32×** over a **$8,064/yr resize worth 1.3×**) ·
✅ `dynamodb.html` (model from access patterns not entities; **hot partition = 69% throttled at 2.5%
consumed**, capacity doubled to no effect, sharded to **21,840/s**; **`FilterExpression` applies AFTER the
read** — 482,104 items / 60,263 RCU to return 12, vs **1.5 RCU** on a GSI, with **`ScannedCount` vs `Count`**
as the diagnostic; **a throttled GSI rejected 92% of BASE-TABLE writes** while the table sat at 1%;
single-table design with every pattern proven one Query + a hot-partition review of *index* keys;
**read-modify-write lost 947 of 1,000 units silently** and the atomic conditional fix is *cheaper*) ·
✅ `messaging.html` (queue/topic/bus/stream chosen by **backpressure, retention, replay**; visibility timeout
**14 of 20 jobs run twice with perfect metrics**; **long polling = 401× fewer requests AND 10× lower latency**,
no trade-off; filter policies **−40% deliveries, −99.2%** for one subscriber; poison message received **43×
in 90 s**, capped by `maxReceiveCount` + rate-limited redrive; **the FIFO message group ID is ordering AND
parallelism** — **304 msg/s on one group with 20 idle workers, 18,420 on sixty**; **EventBridge archive is NOT
retroactive** — a `FilterArns`-scoped replay recovered **3,632 events** without touching 3 healthy consumers;
**everything is at-least-once → key idempotency on BUSINESS ids, not message ids**)
*§5 Operations ×3* — ✅ `observability.html` (four tools, four questions, and the defaults answering none:
**CloudTrail data events OFF** so "who downloaded the export?" is unanswerable — scoped to one bucket
**$0.04 vs $200/mo**; **Average hides outages** — 3 broken hosts of 20 read **1,243 ms while p99 was
8,103 ms**, and **p50 alongside p99** separates "all slow" from "a subset failing"; **`INSUFFICIENT_DATA` is
not an alarm** so a *partial* failure fires and a *total* failure silences — fix with
`--treat-missing-data breaching`, a traffic alarm, and a canary; **metric-dimension cardinality computed at
$37M/mo**, replaced by **EMF at $32.40** with per-customer latency still queryable; **ingestion $0.50/GB
dwarfs retention $0.03/GB**; **X-Ray sampled 0.20% of traffic**, and **annotations are indexed, metadata is
not** — `deployVersion` turns "when did this start?" into a filter) ·
✅ `iac.html` (**IaC is for review and reproducibility, not automation**, and **state is the hard part**;
**a one-line diff produced `Replacement: True`** on a production DB — review the *plan*, and fail CI on it;
**`DeletionPolicy` does NOT cover replacements** — `Retain` was set and the database was destroyed anyway;
two concurrent applies **orphaned a real resource**, and state holds **passwords in plaintext despite
`sensitive`**; **CDK logical IDs derive from the construct path** so a cosmetic rename destroys the bucket;
drift **triaged as revert-it or adopt-it** via CloudTrail, then made *impossible* with an SCP; import as an
iterate-until-**"0 to change"** loop) ·
✅ `security-ops.html` (envelope encryption, and **the KMS key policy is authoritative** — `AdministratorAccess`
+ `kms:*` **still denied**, the error naming the resource-based policy; **RDS encryption is a migration, not a
setting** — snapshot→copy→restore→cut over, **~80 min + a real window**, restore returns defaults; **Lambda env
vars are readable by `ReadOnlyAccess`**; **rotation is two halves and teams ship one** — TTL cache + one retry
cut failures to **1**, RDS Proxy + IAM auth to **0**; 3 high-severity GuardDuty findings **unread for 6 days**
while mining ran → route to a containment fn that **snapshots before isolating and never terminates**;
**leaked temporary creds cannot be deleted** → deny on `aws:TokenIssueTime`; baseline as StackSets + SCPs +
**a check tested to fail**)

*§6 Architecture ×3* — ✅ `well-architected.html` (**the pillars conflict** — architecture is choosing which to
sacrifice, in writing; **serial dependencies multiply** to **99.32% / 293 min per month** while every
component's own SLA looks fine, and **one homegrown auth service contributed 215 of those minutes**; each nine
priced against downtime cost — **99.99%→99.999% saves $3.6k and costs $960k** — with the **break-even
$/hour as a dated revisit trigger**; **queueing delay = ρ/(1−ρ)** measured on a real fleet (**p99 118 → 402 ms
between 48% and 81%**), so the answer was **14 instances where the proposal said 12**; **a control people
bypass is worse than none** → preventive and invisible, plus audited break-glass; an ADR ending the
multi-Region argument on incident history — **all 5 outages in 3 years were self-inflicted and would have
replicated**; **3.25 engineer-days closed a contractual SLA breach**)
✅ `resilience-dr.html` and ✅ `scaling-patterns.html` — summarised in the RESUME block at the top.

**BOTH END-OF-TRACK CHORES DONE:** `s3-cloudfront.html` and `rds-dynamodb.html` are now redirect stubs
(→ `s3`/`edge-dns` and `rds-aurora`/`dynamodb`), and the quiz bank was rewritten to the v4 curriculum
(`10 200 0`, 0 duplicate stems, de-skewed with `node tools/quizshuffle.js`).

**✅ CI/CD v4 (track 18) COMPLETE** — all **21 lessons** rebuilt from 12 v3 (~11KB) to v4 (59–67KB,
every one `det=12 ex=6`) across 6 sections, both end-of-track chores done, and the **quiz bank rewritten
to the v4 curriculum** (200 fresh questions, `10 200 0`, 0 duplicate stems, de-skewed 60/63/77). Whole
track passes `python validate.py tutorials/cicd` with **0 errors and 0 warnings** (29 files); pushed & live.

*§1 Foundations ×4* — `index.html` (**CI is merge frequency, not owning a pipeline**; branch-age conflicts
4%→61%; 34-min pipeline = 71 engineer-hours/week vs $140/month compute; batch arithmetic 26% vs 1.5%; the
five guarantees; the silent zero; red main = 927 engineer-hours/quarter; merge queue 61→7; revert-first
38→6 min) · `git-workflows.html` · `first-pipeline.html` (**a job is a machine, a step is a new shell**;
concurrency cancelled 41% of runs, queue 6m20s→47s; critical path 34→11 min; **artifact vs cache and the
load-bearing-cache bug**) · `pipeline-as-code.html` (copy-paste = 61 PRs/11 weeks/23 unpatched;
composite-action capability boundary; **`@main` broke 47 repos in 2 min**; config complexity clock)
*§2 Building & Testing ×4* — `test-strategy.html` (**diagnosis time 4/18/71 min**; mock drift = 8 defects
in 5 months; **impact selection 41→6 min**; 84% coverage vs 47% mutation) · `flaky-tests.html`
(**0.1% × 1,100 = 33% green**; polling not sleeping −31%/−94%; quarantine with a 14-day deadline;
**19 of 63 were real product bugs**) · `quality-gates.html` (**a routed-around gate is worse than none**;
FP cliff at ~1%/20%; the ratchet 2,412→0 in 9 months; observe→warn→block; break glass) ·
`build-artifacts.html` (build once promote the digest; reproducibility; retention that deleted prod's image;
41TB→6.2TB)
*§3 Pipeline Engineering ×4* — `containers-in-ci.html` (cold cache 8m52s→47s; QEMU 14× slower;
**host socket = root on the runner**) · `pipeline-performance.html` (feedback = queue+setup+critical
path+publish; four levers in order; sharding curve; capacity in money) · `runners-infrastructure.html`
(self-host for capability — 31 engineer-days/yr; **fork PRs = RCE inside your network**; labels are not a
boundary; disk = 61% of infra failures) · `pipeline-reliability.html` (CI as production with SLIs and a
priced error budget; classified retries; layered timeouts + watchdog; detection-first postmortems)
*§4 Deployment ×4* — `deployment-strategies.html` (blast radius × detection; draining 1,840 dropped
requests → 0; **canary sample-size statistics**; rollback drilled 7m10s→74s) · `environments-promotion.html`
(staging caused 9 incidents and caught 8; 61 config differences; digest promotion with an evidence record;
previews $310 vs $4,900) · `database-migrations.html` (**code rolls back, data does not**; expand/contract
as six phased releases; `ADD COLUMN … DEFAULT gen_random_uuid()` = 4m12s exclusive lock; backfills as jobs;
compatibility matrix) · `progressive-delivery.html` (deploy ≠ release; **flag vendor on the request path =
41-min outage**; deterministic bucketing; 312 flags with 71% dead; peeking 4.9%→22.4%)
*§5 Security & Supply Chain ×3* — `secrets-and-auth.html` (**OIDC `sub` condition or the role is public**;
masking fails on base64; rotate-first — key used 61 s after the push; `permissions: {}`) ·
`supply-chain.html` (four links; provenance vs SBOM; **100% signed, 0% verified**; SBOM from the image
214→389 components; admission audit-first found 3 hand-built images) · `dependency-management.html`
(47 chosen, 1,284 installed; weekly grouped updates 2 days/month vs 19/batch; bot merge rate 41%→94%;
847 advisories → 9 exploitable)
*§6 Operating & Measuring ×2* — `dora-metrics.html` (the four keys as pairs; definitions decide the numbers
9d vs 4h; 340% frequency from empty deploys; the constraint moves across three quarters) ·
`platform-rollout.html` (paved road vs queue vs mandate; adoption 12→57/60 in 12 weeks; **10 of 14 opt-outs
were platform defects**; honest funding case with the shortfall stated)

Also: the 7 orphaned v3 files (`what-is-ci`, `github-actions`, `testing-gates`, `artifacts-versioning`,
`secrets-oidc`, `docker-in-ci`, `feature-flags`) are now **redirect stubs**.

**⏳ NEXT: MongoDB v4 (track 19)** — the last v3 track. 12 v3 lessons (~9KB) → ~20 at v4.

**Track-wide note (2026-08-21 audit, still open):** 19 of 23 quiz banks are answer-skewed (correct answer at
index 1 for ~100% of questions); `cicd`, `docker`, `kubernetes`, `leetcode` and `redis` are clean. Fix per
track with `node tools/quizshuffle.js tutorials/<track>` then `python tools/quizcheck.py tutorials/<track>` —
awaiting the user's go-ahead.



**Then the remaining infra two:** CI/CD → MongoDB, each 12 v3 → ~20 at v4.

**Tooling is committed in `tools/` — see `tools/README.md`. Nothing lives in a scratchpad.**
```
PYTHONIOENCODING=utf-8 python validate.py tutorials/<track>   # lessons: det=12 ex=6, 0 errors
python tools/quizcheck.py tutorials/<track>                   # bank: 10 200 0, no skew
node tools/quizshuffle.js tutorials/<track>                   # de-skew (idempotent)
```

**The remaining infra tracks, in the user's order:** AWS → CI/CD → MongoDB.

| Track | Dir | Now | Target |
|-------|-----|-----|--------|
| Docker | `tutorials/docker/` | ✅ **21 at v4** | done |
| Kubernetes | `tutorials/kubernetes/` | ✅ **22 at v4** | done |
| AWS | `tutorials/aws/` | ✅ **20 at v4 + bank** | done |
| CI/CD | `tutorials/cicd/` | 🚧 **12 — NEXT** | ~20 |
| MongoDB | `tutorials/mongodb/` | 12 | ~20 |

Each track: write `nav.js` first, then lessons (commit every 1–2), then retune the quiz bank to
`10 200 0` with de-skewed answer positions, then a whole-track validate.

**Format used** (matches the v4 language-track recipe): "What you'll master" intro with prerequisite
links → Parts 1–6 → one `.mistake-pair` → Common Mistakes table (12 rows) → 6 tiered interview Qs
(2 beginner / 2 mid / 2 senior) → 6 graded exercises with runnable checks and real measured output →
Key Takeaways → pager. Heavy cross-linking between pattern lessons.

Forward links to unwritten lessons show as "broken link" in validate.py; that is expected and clears as
each file lands. Re-run the whole-track validate at the end.

**Authoring notes for a 70–80KB v4 lesson (learned across the AWS track — applies to any track):**
- These files are too big for one comfortable `Write`. Write **part A** (intro → Parts 1–6 → mistake-pair
  → Common Mistakes → 6 interview `<details>`) and **part B** (6 exercise `<details>` → Takeaways → pager
  → closing `</main></div><script>…</body></html>`) to the scratchpad, then `cat A B > tutorials/<track>/<file>.html`.
  The scratchpad is only a staging area — the committed HTML is always the artifact.
- **`validate.py` catches two silent-corruption bugs**; always run it before committing:
  1. **Unescaped `<` inside `<pre>`** — e.g. `PK = TENANT#<id>#<shard>` or `<timestamp>`. Browsers swallow
     everything to the next `>`. Use `&lt;`/`&gt;`. (`<=` and `<0` are safe — a letter or `/` after `<` is
     what triggers it.) Hit twice on this track.
  2. **A stray `</p>` closing a `<div class="note">`** that never opened one. Hit twice; fixed with `sed`
     after assembly.
- **Mojibake check** (double-encoded UTF-8 from earlier sessions): `grep -c 'â€\|·\|→\|Ã' <file>` must
  print `0`. Write the arrows/bullets as real UTF-8 characters, never as escapes.
- Structural counts to confirm: `grep -c '<details class="solution">'` = **12**, `grep -c 'class="exercise"'` = **6**.
- Pager: `prev` = the previous lesson in `nav.js` order, `next` = the following one. The forward link
  errors until that file lands — expected.

**How to work:** write each lesson at v4 depth, then
```
PYTHONIOENCODING=utf-8 python validate.py tutorials/<track> <file>.html
```
must report `det=12 ex=6`, 0 errors. Commit per lesson or per pair. A forward link to the
not-yet-written next lesson shows as a "broken link" error — that is expected and clears when the
next file lands; re-run the whole-track validate at the end to confirm 0 errors.

**Then:** the infra six (~70 lessons: Docker, Kubernetes, AWS, CI/CD, MongoDB, Redis) — the last
remaining v3 tracks.

**Quiz-bank recipe (per the 2026-08-05 decision — a track is not done without it):**
sets are `{title:"Quiz N · Topic", desc, questions:[{q, options:[3], answer:<idx>, explain}×20]}`,
wrapped in `window.QUIZ_SETS=window.QUIZ_SETS||[]; window.QUIZ_SETS.push(...)`. Set 10 = mixed mock exam.
Validate with the node one-liner at the bottom of this file → must print `10 200 0`.

**Decisions settled 2026-08-05 (user, via AskUserQuestion):**
- **Infra-six scope: FULL EXPANSION** (~20 lessons each, ~70 total). The deepen-in-place recommendation was declined; build out the curricula.
- **Quiz banks: retune per track, as each track's lessons finish** — no longer deferred to the end. A track is not "done" until its bank validates `10 200 0` against the v4 curriculum.

---

## Track completion

| # | Track | Lessons | Quiz Qs | Status |
|---|-------|---------|---------|--------|
| 1 | HTML | 14 | 200 | ✅ DONE |
| 2 | CSS | 14 | 200 | ✅ DONE |
| 3 | JavaScript | 16 | 200 | ✅ DONE |
| 4 | React | 12 | 200 | ✅ DONE |
| 5 | Node.js | 12 | 200 | ✅ DONE |
| 6 | Python | 12 | 200 | ✅ **v4 DONE 12/12** (2026-08-04) |
| 7 | Java | 12 | 200 | ✅ DONE |
| 8 | SQL | 12 | 200 | ✅ **v4 DONE 12/12 + quiz retuned** (2026-08-05) |
| 9 | MongoDB | 12 | 200 | ✅ DONE |
| 10 | Redis | 11 → **21 (v4)** | 200 | ✅ **v4 COMPLETE** — 21/21 lessons, quiz retuned, 0 validate errors 
| 11 | Docker | 12 | 200 | ✅ DONE |
| 12 | Kubernetes | 12 | 200 | ✅ DONE |
| 13 | AWS | 12 | 200 | ✅ DONE |
| 14 | CI/CD | 12 | 200 | ✅ DONE |
| 15 | Angular | 12 | 200 | ✅ DONE |
| 16 | .NET (C#) | 23 (v4) | 200 | ✅ DONE |
| 17 | ASP.NET Core | 23 (v4) | 200 | ✅ **v4 DONE 23/23** (2026-08-04) |
| 18 | LeetCode Patterns | 21 lessons (Foundations ×3 + Core ×8 + Trees&Graphs ×4 + Advanced ×6) | 200 | ✅ **v4 DONE 21/21 + quiz retuned** (2026-08-13) |
| 19 | System Design | 36 lessons (Fundamentals ×11 + Deep Dives ×6 + Case Studies ×12 + Senior/Staff ×7) | 200 | ✅ DONE (v4) |
| 20 | 🆕 Database Concepts & Architecture | **15 (v4)** | 200 | ✅ **DONE 15/15 + quiz bank** (2026-08-07) |
| 21 | 🆕 Vector Databases & RAG | **15 (v4)** | 200 | ✅ **DONE 15/15 + quiz bank** (2026-08-11) |
| 22 | 🆕 Unix & Linux | **20 (v4)** | 200 | ✅ **DONE 20/20 + quiz bank** (2026-08-10) |

**v3 build-out done: 19 full tracks (3,800 quiz questions), all committed & pushed.**
**Tracks 20–22 are new (20–21 user-requested 2026-08-04, 22 added 2026-08-08) and built directly at v4 depth — no v3 stage.**

---

## 🚧 CURRENT PHASE: Mastery v4 rebuild (started 2026-07-12)

**User feedback:** v3 lessons (~9–13KB each) are too shallow — "can't even master a single topic" at beginner, mid, OR senior level. Directive: make learners masters of each topic.

**Decisions (user-confirmed via AskUserQuestion):**
1. **Expand curriculum** — split combined topics into focused lessons at 3–5× depth (not deepen-in-place). E.g., JS "Closures & this" → 4 separate lessons. Tracks grow from ~12–16 to ~30+ lessons.
2. ~~**Work in site order, tracks 1→19**~~ — **SUPERSEDED 2026-07-30 by the damage-order queue below.** Site order polished 8 tracks while the highest-value ones sat at v3. Still true: complete each track fully before moving on.

### v4 mastery lesson format (supersedes v3 skeleton for lesson depth; same HTML shell/header/sidebar/pager)
Target **~500–700 lines (~35–50KB)** per lesson. Structure:
1. `<h1>` + level badge + intro: what you'll master + prerequisites line (link previous lessons)
2. **Gradual concept build**: plain-language explanation → mental model → syntax → several worked, commented examples (never one example where three teach more)
3. **Step-by-step build section**: construct something real, incrementally, showing output at each step
4. **Deep-dive sections**: edge cases, browser/runtime behavior, spec gotchas, internals (the senior layer)
5. **Common Mistakes** table (grown, 6+ rows)
6. **Interview Questions**: 6+ `<details class="solution">`, explicitly graded — 2 beginner, 2 mid, 2 senior
7. **🏋️ Graded exercises WITH solutions**: 6–10, easy→hard, each with a `<details class="solution">` solution + explanation (this is new vs v3 — v3 had unsolved practice prompts)
8. Key Takeaways + pager

### v4 progress
| # | Track | v4 status |
|---|-------|-----------|
| 1 | HTML | ✅ **DONE** — all 32 mastery-depth lessons shipped (Foundations ×8, Forms Mastery ×6, Semantics & Structure ×3, Media & Embedding ×4, Accessibility ×3, SEO ×2, Performance ×2, Production ×4). Old combined pages (links-images.html, lists-tables.html) kept as redirect stubs to their split successors. Quiz bank NOT yet re-tuned to v4's expanded topic list — old 200 Qs still valid but could use a refresh pass later. |
| 2 | CSS | ✅ **DONE** — all 28 mastery-depth lessons shipped (Foundations ×7, Layout ×6, Motion & Interaction ×3, Modern CSS ×5, Architecture ×3, Production ×4). Old combined pages (colors-units-typography.html, transitions-animations.html, cross-browser-a11y.html) kept as redirect stubs. Link-audited clean (0 broken internal hrefs). Quiz bank not yet re-tuned. |
| 3 | JavaScript | ✅ **DONE (v4+ expanded, 2026-07-18)** — **38 lessons** at mastery depth (Language Core ×9, Objects & Data ×7, Async ×5, Browser & Web Platform ×5, Modules & Tooling ×2, Production ×10). **+5 new: Functional Patterns (Language Core), Dates/Time & Intl (Objects & Data), WebSockets & Real-Time (Browser), Testing JavaScript + Design Patterns in JavaScript (Production)**. Old combined pages kept as legacy stubs. Link-audited clean; quiz banks retuned to the new topics (sets 2/3/4/8/10) — validate 10/200/0. |
| 4 | React | ✅ **DONE** — all 28 mastery-depth lessons shipped (Foundations ×7, Effects & Lifecycle ×5, State Management ×5, Performance ×4, Patterns & Quality ×4, Full-Stack React ×3 incl. Server Components, Next.js, Production Patterns). Old combined pages (props-state, forms-events, context-state) kept as redirect stubs. Heavy cross-linking to JS track + between lessons (later lessons cite earlier by number). Link-audited clean; quiz banks validate 10/200/0 (not yet re-tuned to v4 topics). |
| — | Spring Boot | ✅ **DONE (v4+ expanded, 2026-07-18)** — **23 lessons** at full HTML-track depth (300–360 lines): Core Container ×5, Web Layer ×5, Data Layer ×3, Cross-Cutting ×3, Production ×4, **+ Event-Driven & Reactive ×3 (API Design & Versioning, Messaging & Kafka, Reactive/WebFlux)**. Every lesson: "what you'll master" intro → Parts 1–6 → deep-dive senior `.note` → Common Mistakes → 6 tiered interview Qs → 6 graded exercises → Key Takeaways → pager. Link-audited clean; quiz 10/200/0 (set 10 retuned to cover the new topics). All pushed & live. |
| — | Java | ✅ **DONE (v4+ expanded, 2026-07-18)** — **45 lessons** at full depth. Original 40 across Foundations/OOP/Core Libraries/Modern Java/Concurrency/JVM&Perf/Professional, **+5 new: Annotations & Reflection, Regular Expressions (Core Libraries); The Module System/JPMS (Modern Java); Concurrency Patterns & Pitfalls capstone (Concurrency); Benchmarking & JMH (JVM & Performance)**. Link-audited clean; quiz 10/200/0 (sets 5 & 7 retuned for the new topics; benchmarking already in set 8). All pushed & live. |
| 15 | Angular | ✅ **DONE (v4, 2026-07-19)** — **23 lessons** at mastery depth across 8 sections: Foundations ×4 (index=Components & Standalone, data-binding=Templates, directives=Control Flow, pipes), Components & Reactivity ×4 (component-communication, lifecycle, signals, change-detection), Services & DI ×2 (services-di, di-advanced), RxJS ×2 (rxjs, rxjs-patterns), Forms ×3 (template-forms, forms=Reactive, form-validation incl. CVA), Routing & HTTP ×3 (routing, guards-lazy, http), State ×2 (state-management, ngrx), Production ×3 (testing, performance, enterprise=SSR/i18n/security/monorepo). 12 rewritten in place + 11 new files. Modern Angular throughout: standalone, signals, @if/@for, functional guards/interceptors, zoneless, httpResource. Link-audited clean; quiz retuned (9 swaps: linkedSignal/resource, multi-providers, inject-context, catchError placement, takeUntilDestroyed, lifecycle, CVA, track identity) — 10/200/0. |
| 16 | .NET (C#) | ✅ **DONE (v4, 2026-07-27)** — **23 lessons** at mastery depth across 6 sections: Foundations ×5 (index=How It Runs, types, control-flow, strings, methods), Object-Oriented C# ×5 (oop, inheritance, records-structs, generics, pattern-matching), Core Libraries ×4 (collections-generics, linq, delegates-events, exceptions-nullability), Async & Concurrency ×3 (async-await, **async-patterns** new, **threading** new), Runtime & Performance ×2 (memory, performance-aot), Professional ×4 (di-hosting, efcore, testing, **modern-csharp** new capstone). 12 rewritten in place + 11 new files. Modern throughout: primary constructors, collection expressions, required/init, TimeProvider, Channels, ExecuteUpdate/Delete, source generators, NativeAOT. Link-audited clean (0 broken); pager chain verified against nav order end to end; quiz banks retuned (14 swaps) — 10/200/0. |
| 19 | System Design | ✅ **DONE (v4, 2026-07-30)** — **all 36 lessons rebuilt**, 30–61KB each (1.8 MB total), every one with 12 `<details>` (6 tiered interview Qs + 6 graded exercises), Common Mistakes table and Key Takeaways. **Whole track passes `python validate.py tutorials/system-design` with 0 errors.** §1 Fundamentals 11/11 · §2 Deep Dives 6/6 · §3 Case Studies 12/12 · §4 Senior/Staff 7/7. Uses the **tradeoff-driven SD format**; case studies use the **case-study format** (both below). Quiz bank still the v3 200-Q set — retune to the v4 curriculum when convenient. |
| 5 | Node.js | ✅ **DONE (v4, 2026-07-31)** — **25 lessons** at v4 depth (27KB median), commit `fe2219f`. Was "deep but narrow" at 10 lessons; expanded rather than deepened, as planned. |
| 17 | ASP.NET Core | ✅ **DONE (v4, 2026-08-04)** — **all 23 lessons** at v4 depth, 30–52KB each, every one `det=12 ex=6`. **Whole track passes `python validate.py tutorials/aspnet` with 0 errors.** §1 Foundations 5/5 (index, minimal-apis, routing, model-binding, configuration) · §2 The Pipeline 4/4 (middleware, di-config, filters, validation-errors) · §3 Building APIs 4/4 (controllers-mvc, api-design, versioning, openapi) · §4 Data 3/3 (efcore-data, efcore-advanced, caching) · §5 Security &amp; Realtime 4/4 (authn-authz, authorization, security, signalr) · §6 Production 4/4 (caching-background=Background Services, testing, clean-architecture, production-readiness). **Re-scoped v3 files:** `di-config` is DI-only (config split out), `validation-errors` is error-handling-only (validation moved to model-binding), `caching-background` is Background Services only (caching split out), `efcore-data` is modelling/querying only (change tracking split out). `routing-binding.html` became a redirect stub → routing + model-binding. Quiz bank still the v3 200-Q set — retune when convenient. |
| 6 | Python | ✅ **DONE (v4, 2026-08-04)** — **all 12 lessons** at v4 depth, 35–58KB each, every one `det=12 ex=6`. **Whole track passes `python validate.py tutorials/python` with 0 errors.** Order: index (Syntax/Types/Variables) → control-flow → data-structures → strings-io → oop → comprehensions-generators → decorators-context → modules-packaging → typing → concurrency → testing → fastapi. Uses the **language-track v4 format** (6 Parts → Common Mistakes → 6 tiered Qs → 6 graded exercises → Takeaways), *not* the SD tradeoff format. Rebuilt in place — the v3 content was thin but correct, so this was expansion rather than reconstruction, and no redirect stubs were needed. Quiz bank still the v3 200-Q set — retune when convenient. |
| 5, 7–18 | all others | ⏳ pending (still at v3 depth) — see damage-order queue below |

#### Python v4 — per-lesson status (all ✅, 0 validation errors)
| # | Lesson | v3 | v4 | Focus |
|---|--------|----|----|--------|
| 1 | index.html (Syntax, Types & Variables) | 8KB | **35KB** | name/object model · core types · strong+dynamic typing · idioms · deep dives: mutable default argument, copying |
| 2 | control-flow.html (Control Flow & Functions) | 8KB | **38KB** | truthiness · loops · 5 parameter kinds · LEGB/closures/late-binding · pattern matching · exceptions as control flow |
| 3 | data-structures.html | 8KB | **42KB** | complexity per operation · dicts/sets/hashability · tuples & immutability · collections · sorting · choosing by access pattern |
| 4 | strings-io.html | 7KB | **42KB** | immutability & O(n²) concat · format mini-language · str vs bytes & encoding · `with`/modes/streaming · pathlib · atomic writes |
| 5 | oop.html (OOP & Dataclasses) | 9KB | **48KB** | attribute lookup & shared class attrs · dunder protocols · dataclass slots/frozen · MRO & super() · properties/descriptors · composition |
| 6 | comprehensions-generators.html | 8KB | **47KB** | comprehension forms · iterator protocol & exhaustion · generators as frames · lazy pipelines · itertools · send/throw/close |
| 7 | decorators-context.html | 9KB | **50KB** | wraps & the 5 omissions · 3-layer factories · lru_cache method leak · `__exit__` returning True · @contextmanager · ExitStack |
| 8 | modules-packaging.html | 8KB | **47KB** | import once & side effects · sys.path shadowing · circular imports (4 fixes) · venv + lockfile chain · src layout · build/publish |
| 9 | typing.html (Type Hints) | 8KB | **49KB** | erasure · narrowing & assert_never · Protocol · generics & invariance · Literal/TypedDict/NewType · mypy vs Pydantic · rollout plan |
| 10 | concurrency.html (GIL, Threads, Async) | 9KB | **53KB** | what the GIL locks · decision table w/ numbers · asyncio & blocking calls · `+=` is not atomic · pickling boundary · cancellation/timeouts |
| 11 | testing.html (pytest) | 8KB | **55KB** | assertion introspection · parametrise boundaries · fixtures & scope · transaction-rollback DB · patch-where-used & autospec · flakiness |
| 12 | fastapi.html (Production APIs) | 9KB | **58KB** | types as contract · request/response model split · DI & overrides · async def vs def · BOLA/authz · errors/config/observability · deploy |

### ⚠️ Order changed 2026-07-30 (user: "junior, mid and senior can't refer to this — content not up to the mark")

Strict site order 1→19 polished 8 tracks while the highest-value ones stayed at v3. Audit of actual page sizes showed the site is really **two sites**: 8 v4 tracks at 22–32KB/lesson with 12 `<details>` blocks, and 12 v3 tracks at 5–13KB with 3. Worst offender was System Design — 34 lessons at 5KB median with **zero** exercises, zero graded interview Qs, zero Common Mistakes, despite being the most senior-referenced track on the site.

**New queue, by damage (user-confirmed):**
1. ~~**System Design** (36)~~ ✅ **COMPLETE 2026-07-30** — 36/36 at 30–61KB, 0 validation errors
2. ~~**Node.js**~~ ✅ **COMPLETE 2026-07-31** — 10 → 25 lessons @ 27KB median
3. ~~**ASP.NET Core**~~ ✅ **COMPLETE 2026-08-04** — 23/23 lessons, 0 validation errors
4. ~~**Python**~~ ✅ **COMPLETE 2026-08-04** — 12/12 lessons, 0 validation errors
5. ~~**SQL**~~ ✅ **COMPLETE 2026-08-05** — 12/12 lessons (47–57KB) + quiz bank retuned to v4 (20 swaps)
6. ~~**Database Concepts & Architecture**~~ ✅ **COMPLETE 2026-08-07** — 15/15 lessons (50–59KB) + quiz bank `10 200 0`
7. ~~**Unix & Linux**~~ ✅ **COMPLETE 2026-08-10** — new track, 20/20 lessons (44–59KB) + quiz bank `10 200 0`
8. ~~🆕 **Vector Databases & RAG**~~ ✅ **COMPLETE 2026-08-11** — new track, 15/15 lessons (51–68KB) + quiz bank `10 200 0`
9. ~~**LeetCode**~~ ✅ **COMPLETE 2026-08-13** — 21/21 lessons (48–59KB, all `det=12 ex=6`) + quiz bank retuned (27 swaps, answer positions de-skewed). Whole track validates 0 errors, 0 warnings.
10. **Infra six** — Docker, Kubernetes, AWS, CI/CD, MongoDB, Redis (9–12KB, all 3 `<details>`)

**Remaining: ~70 lessons across 6 tracks** (the infra six, under the approved full expansion).

#### SQL v4 — per-lesson status (as of 2026-08-05)
Rebuilt in place, no redirect stubs needed. Every done lesson `det=12 ex=6`, 0 validation errors.

| # | Lesson | v3 | v4 | Status / focus |
|---|--------|----|----|----------------|
| 1 | index.html (SELECT & Filtering) | 8KB | **49KB** | ✅ declarative thinking · logical order of execution · NULL & 3-valued logic · sargability · CASE/types · SELECT * hygiene |
| 2 | aggregates.html (Sorting, Limiting & Aggregates) | 7KB | **47KB** | ✅ NULL in aggregates · GROUP BY rule & MySQL ONLY_FULL_GROUP_BY · WHERE vs HAVING · FILTER/pivots · ROLLUP · empty-group problem · keyset pagination |
| 3 | joins.html | 8KB | **52KB** | ✅ join types & why Venn misleads · ON vs WHERE · anti/semi-joins · **fan-out** · self-join/LATERAL · N+1 · nested-loop/hash/merge |
| 4 | dml.html (INSERT/UPDATE/DELETE) | 8KB | **54KB** | ✅ affected-row-count discipline · COPY/RETURNING · upserts & concurrency · chunked deletes · soft delete · MVCC write mechanics |
| 5 | subqueries-ctes.html | 8KB | **50KB** | ✅ all subquery forms · correlated/decorrelation · NOT IN landmine · CTE optimisation fence (PG12 change) · recursive + cycle guards · LATERAL · data-modifying CTEs |
| 6 | window-functions.html | 8KB | **49KB** | ✅ OVER anatomy · ranking trio · **frames: ROWS vs RANGE, default-frame traps** · LAG/LEAD · gaps-and-islands · execution order · when LATERAL wins |
| 7 | schema-design.html | 9KB | **57KB** | ✅ keys (surrogate/natural/UUIDv4-vs-v7) · normal forms by anomaly · deliberate denormalisation + drift checks · types/constraints · temporal modelling · EAV/polymorphic anti-patterns |
| 8 | transactions.html (Constraints & Transactions) | 9KB | **52KB** | ✅ constraints make invalid states impossible · ACID promises & what they don't · savepoints & subtransaction overflow · lost update + 3 fixes · WAL/durability limits · txn in connection pools, outbox, idle-in-transaction |
| 9 | indexes.html (Indexes & Query Plans) | 9KB | **56KB** | ✅ B-tree page arithmetic · sargability derived · selectivity & why a good index is ignored · composite order & INCLUDE/index-only · EXPLAIN incl. **loops multiplier** · stats/correlated columns · CONCURRENTLY |
| 10 | isolation.html (Isolation Levels & Locking) | 10KB | **54KB** | ✅ anomalies as interleavings · levels vs the standard (PG≠MySQL) · MVCC snapshots · read-committed update anomaly · write skew & SSI · retry loops (40001/40P01, jitter) · lock queue & ACCESS EXCLUSIVE |
| 11 | optimization.html (Query Optimization) | 9KB | **53KB** | ✅ measure by **total_exec_time** not mean · planner cost model & random_page_cost · sargable rewrites · NOT IN landmine · N+1 · keyset pagination · COUNT(*) strategies · work_mem per node · guardrails |
| 12 | scaling.html (Replication, Partitioning, Sharding) | 10KB | **56KB** | ✅ what one node really does · replication lag as correctness (LSN/sticky reads) · partitioning ≠ write capacity · shard-key choice & shard maps · functional split before sharding · no-downtime migration |

**SQL quiz bank:** ✅ **RETUNED 2026-08-05** — 20 swaps across sets 4/7/8/9 covering v4-only concepts (EXPLAIN loops multiplier, heap fetches on index-only scans, CREATE STATISTICS, random_page_cost on SSD, CONCURRENTLY, affected-row count, outbox, idle-in-transaction, SKIP LOCKED, 40001 retries with jitter, ACCESS EXCLUSIVE lock queue, pg_stat_statements by total time, per-role work_mem, LSN read-your-writes, DETACH retention, shard-map routing, functional split). Validates `10 200 0`, no duplicates.

### 🆕 Two new Database-section tracks (user-requested 2026-08-04)

Both are **new tracks built directly at v4 depth** (no v3 to rebuild), added to the `Databases` section of the root `index.html` alongside SQL / MongoDB / Redis. Sequenced **after SQL, before LeetCode** (user-confirmed).

**A. Database Concepts & Architecture** (`tutorials/database-concepts/`) — ✅ **LESSONS 15/15 DONE 2026-08-06**
Scope confirmed by user: **"based on design perspective and storage engine internals"** — i.e. data-modelling/physical-design decisions *plus* how the engine actually works underneath. Deliberately **excludes** distribution topics (CAP, replication, consensus, sharding) — those already exist in System Design and must not be duplicated.

**As built** (whole track passes `python validate.py tutorials/database-concepts`, 0 errors, every lesson `det=12 ex=6` at 50–59KB):
1. *Storage Foundations* ×5 — `index.html` (How a Database Stores Data: the 6 layers, memory/disk gap, pages, RUM) · `pages-heap-files.html` (slotted pages, row layout, **alignment padding**, ctid, **HOT updates**, TOAST) · `btrees.html` (fanout/depth arithmetic, splits, **sequential vs random key density**, B-link concurrency, index bloat) · `lsm-trees.html` (memtable/SSTable, **bloom filter sizing**, size-tiered vs levelled vs time-window compaction, tombstones) · `buffer-pool.html` (hit-rate non-linearity, pinning, **clock sweep & ring buffers**, checkpoint storms, PG 25% vs InnoDB 75%)
2. *Durability & Concurrency* ×3 — `wal-recovery.html` (write-ahead + force-at-commit, **LSN's three jobs**, ARIES/repeating history, torn pages & full-page writes, fsync truth, group commit, one log → 4 features) · `mvcc.html` (visibility rule, **in-table vs undo-log**, vacuum blockers, **wraparound**, hint bits, snapshot ≠ serialisable) · `locking-latches.html` (locks vs latches, conflict matrix, **row locks stored in the tuple → no escalation**, deadlock detection, **lock queue outage**, advisory locks)
3. *Query Processing* ×3 — `query-planner.html` (5 stages, rewriter/views/RLS/CTE inlining, join-order search & GEQO, pushdown, **generic plan failure**) · `cost-models.html` (**cost formula by hand**, MCV/histogram/n_distinct, **independence assumption**, error propagation, calibrating random_page_cost) · `join-algorithms.html` (3 algorithms + costs, **nested loop as estimate-error signature**, hash spill batches, aggregation strategies, key skew)
4. *Design Perspective* ×4 — `physical-design.html` (**reversibility hierarchy**, key choice, row width, write-path design, partition key from query logs) · `oltp-olap.html` (row vs columnar arithmetic, **4 compression encodings**, vectorised execution, what columnar is bad at, the middle ground) · `engine-landscape.html` (**6 characterising questions**, Postgres/InnoDB/SQLite/DuckDB/LSM personalities) · `choosing-a-database.html` (6 workload dimensions, why PG is the default, decision tree, **costs evaluations miss**, PoC that can fail, ADRs)

✅ **Quiz bank DONE 2026-08-07** — sets 1–10 written from scratch against the v4 curriculum, one set per
theme: 1 How a DB Stores Data · 2 Pages/Heap/Row Layout · 3 B-Trees & LSM-Trees · 4 Buffer Pool ·
5 WAL/Recovery/Durability · 6 MVCC/Locking/Latches · 7 Query Planner · 8 Cost Models & Join Algorithms ·
9 Physical Design/OLTP-OLAP/Engine Choice · 10 mixed mock exam. Validates `10 200 0`, 0 duplicate stems.
**Track 20 is fully complete.**

**B. Vector Databases & RAG** (`tutorials/vector-databases/`) — ✅ **COMPLETE 2026-08-11, 15/15 + bank**
Scope: **vector stores + RAG patterns**, incl. evaluation and production ops. **As built** (whole track
passes `python validate.py tutorials/vector-databases`, 0 errors, every lesson `det=12 ex=6` at 51–68KB):
1. *Foundations* ×4 — `index.html` (What a Vector DB Is For: semantic vs lexical, the derived-index principle) · `embeddings.html` (lossy compression, **dilution**, model-space incompatibility) · `similarity-metrics.html` (cosine/IP/L2, **normalise then use IP**, pgvector's negated `<#>`) · `dimensionality.html` (distance concentration, **why learned manifolds escape it**)
2. *Indexing & Search* ×4 — `knn-vs-ann.html` (recall@k, the exact-scan crossover) · `hnsw.html` (layers, `m`/`ef_construction`/`ef_search`, **why deletes need neighbour-list repair**) · `ivf-pq.html` (centroids/probes, SQ/PQ/binary, **rescoring recovers quantisation loss**) · `tuning-recall.html` (the recall/latency/memory triangle, knee-finding, adaptive escalation)
3. *The Landscape* ×3 — `pgvector.html` (vectors as a column, operator-class mismatch → silent seq scan, **the planner's filter strategy switch**) · `dedicated-stores.html` (**segments + buffer + compaction**, tombstones, **fan-out tail latency arithmetic**, store-by-store differentiators, FAISS-is-a-library) · `hybrid-search.html` (**pre/post/during-traversal filtering by selectivity**, 1/s over-fetch cost, BM25 IDF, **RRF vs score blending**, filter BOTH branches)
4. *RAG in Production* ×4 — `chunking.html` (**dilution measured**, structural > recursive > semantic > fixed, overlap-is-cargo-cult, **contextual headers**, small-to-big, idempotent/incremental ingestion) · `retrieval-reranking.html` (**the funnel**, bi- vs cross-encoder, candidate-count knee, truncation + uncalibrated logits, query rewriting, **lost-in-the-middle assembly**) · `evaluation.html` (**pooling**, n≥200/500, recall vs nDCG, faithfulness + abstention, **judge validation & bias**, paired significance, **per-class CI gates**) · `scaling-ops.html` (memory formula, **cost is ~78% LLM tokens**, cache keys must include filters + index version, **short-results & max-score alerts**, parallel-index model migration, **context poisoning**)

**Quiz bank:** sets 1–5 = Foundations/Metrics/HNSW/IVF-Quantisation/pgvector-Stores;
6–10 = Filtering-Hybrid/Chunking/Reranking/Evaluation-Ops/mixed mock. `10 200 0`, 0 duplicate stems.

### ✅ Settled decision: infra six scope (2026-08-05)
**FULL EXPANSION — ~20 lessons each, ~70 total.** The build recommendation to deepen in place at 12 each (~40) was put to the user and **declined**; build out the curricula. Applies to Docker, Kubernetes, AWS, CI/CD, MongoDB and Redis.

### Session note 2026-08-07
Database Concepts quiz bank written and validated (`10 200 0`, no duplicate question stems) — track 20 done.
The `← CSS Track` nav bug from the quiz.html template struck again here (it was fixed in SQL on 2026-08-05);
**when scaffolding a new track's quiz.html from `tutorials/css/quiz.html`, replace all three strings, and
grep the new file for `CSS` before committing.**

### Session note 2026-08-11
Vector Databases & RAG finished from 9/15 → 15/15 + both quiz banks; track 21 done, all pushed & live.
**Two gotchas worth carrying forward:**
1. **`quiz.html` mojibake outlived its supposed fix.** The status file claimed it was repaired during
   scaffolding; it still held `·` ×5 and `→` ×1 (double-encoded UTF-8). The hub cards split titles on
   `" · "`, so mojibake silently breaks card subtitles. **Grep new quiz.html files for `Â` and `â†` as
   well as `CSS`.**
2. **`validate.py` earned its keep again** — it caught `<claim>` inside a `<pre>` in `evaluation.html`
   (unescaped `<` swallows content in browsers). Prompt templates containing `<placeholder>` tokens are a
   recurring source of this; escape them as `&lt;...&gt;`.
Next up: the infra six — Docker → Kubernetes → CI/CD → AWS → MongoDB → Redis.

### Session note 2026-08-06
SQL v4 finished (5 lessons: transactions → indexes → isolation → optimization → scaling) **and its quiz bank retuned** — the first track to satisfy the new "not done without the bank" rule. Then Database Concepts built from zero: nav.js, quiz.html, root index card, and all 15 lessons.

**Two validator catches worth remembering** (both are silent-corruption bugs in browsers, invisible to source review): an `<a href>` inside a `<pre>` block, and a bare `<` in `DROP INDEX <the 4 unused>`. `validate.py` flagged both. Also fixed a stale `← CSS Track` nav link in `tutorials/sql/quiz.html` that had been copy-pasted from the CSS template.

**Working note:** while writing a track in order, a forward `<a>` to the not-yet-written next lesson makes `validate.py` report a broken link. That is expected — it clears when the next file lands. Run the whole-track validate at the end to confirm 0 errors.

### Session note 2026-08-03
16 ASP.NET lessons written in one session. Sustained rate is ~1 lesson per 15–20 min at 32–47KB each, so the remaining ~112 lessons span multiple sessions. Every lesson is committed at each checkpoint — resume from this file plus `git log --oneline`. The v4 lesson format is stable and proven across 5 sections; no format changes pending. Quiz banks across *every* v4 track (HTML, CSS, JS, React, Angular, .NET, System Design) are still the v3 200-Q sets — not broken, but drifted from the expanded curricula. Retune pass deferred until lessons are done.

### Tradeoff-driven SD lesson format (System Design only — supersedes the language-track recipe for this track)
Language tracks hit depth via tiered interview Qs + graded coding exercises. System Design needs a different shape — same shell/sidebar/pager and same 12-`<details>` volume, but:
1. "What you'll master" intro + prerequisites line
2. **Mental model** before mechanics — and where a popular framing is *wrong*, say so explicitly (CAP's pick-2-of-3, "balanced keys = balanced load")
3. **Worked arithmetic, not asserted claims** — show the modulo remap table, show the QPS→servers chain, and state a **design consequence after every number**
4. `mistake-pair` divs for ❌ unbacked vs ✅ derived reasoning
5. **Deep dives on the mechanism** (how reconciliation actually works, how data moves at join time), plus **alternatives with when-NOT-to-use** — the strongest senior signal
6. Common Mistakes table, 7–8 rows
7. 6 tiered interview Qs (2 🟢 beginner / 2 🟡 mid / 2 🔴 senior) — senior answers are multi-paragraph and name the trade-off being accepted
8. 6 graded exercises easy→hard; solutions show the *reasoning chain*, and the hard ones often end by **renegotiating the requirement** (approximate rank beats exact rank; cap retention; question the spec)
9. Key Takeaways (8–10 bullets) + pager

### Case-study format (§3 Design X lessons — supersedes the above for those 12)
Same shell and same volume (12 `<details>` = 6 tiered Qs + 6 graded exercises, 24KB+), but structured as an interview walkthrough rather than concept teaching:
1. "What you'll master" + prerequisites, and **what this problem is really testing** (every case study has a signature skill — TinyURL = encoding + read-heavy caching; rate limiter = algorithm choice + distributed counting; chat = fan-out + delivery guarantees)
2. **Requirements clarification** — functional, non-functional, and explicitly *out* of scope. Model the questions a candidate should ask.
3. **Estimation** with a design consequence after each number (reuse the estimation-lesson method)
4. **High-level design** — the diagram and the request flow
5. **The core design decision** — a tradeoff table of 2–4 real options, then a justified pick. This is the section that carries the lesson.
6. **Deep dive on the hard part** (weight this heavily — it's what separates senior candidates)
7. **Bottlenecks & scaling** — what breaks first at 10×, and the fix
8. Common Mistakes → 6 tiered interview Qs → 6 graded exercises → Key Takeaways → pager

### ✅ validate.py — required check on every lesson, every track

**Run from repo root: `python validate.py tutorials/<track> [file.html ...]`**
- Arg 1 is the **directory**; extra args are filenames **relative to it** (`validate.py tutorials/python index.html`). Omit filenames to check the whole track.
- Checks: HTML tag nesting, **unescaped `<` inside `<pre>`**, required asset refs, v4 structure counts (`det=12 ex=6`), and resolves every internal link.
- Expect `[ ok ] name  NNkB  det=12 ex=6 tbl=N` and `0 errors`. Exits 1 on any error.
- On Windows, prefix with `PYTHONIOENCODING=utf-8` or the emoji/em-dashes crash the console writer (cp1252) — a *reporting* failure, not a file problem.

**This is not optional ceremony — it caught 6 real bugs in System Design** that source review missed, including an unescaped `<` that silently swallowed a document from line 200 to `</main>`, and an `<a>` tag nested inside a `<pre>`. Browsers fail these silently.

> **Fixed 2026-07-30:** explicit filenames weren't joined to the root dir, so `validate.py tutorials/python index.html` silently checked `./index.html` (the site homepage) and reported bogus missing-asset errors. A checker that inspects the wrong file while reporting confidently is worse than none — re-verify this behaviour if the script is ever refactored.

Quizzes: existing 200-Q banks stay; extend/retune only after a track's lessons are done, if question topics drifted.

**Build notes for resuming/replicating on remaining tracks:**
- Curriculum expansion pattern: split each v3 combined-topic lesson into 2-4 focused lessons at 3-5x depth (HTML: 14→32; CSS: 14→28). Group into thematic sections (e.g. CSS: Foundations/Layout/Motion/Modern/Architecture/Production) reflected in nav.js.
- Later lessons in a track deliberately cross-reference earlier ones by name — a capstone/consolidation lesson near the end of each major section that assembles several prior lessons' techniques into one real component (HTML's Production Patterns, CSS's Component Patterns) is a deliberate, recurring pedagogical device worth replicating.
- Old superseded combined-topic HTML files become tiny redirect stubs (meta http-equiv=refresh + links to the split successors) rather than being deleted, in case anything external links to the old URL.
- Commit in checkpoints of 1-4 lessons each, pushing after every checkpoint. Run a link-audit one-liner (grep every internal href, confirm the target file exists) before declaring a track done.

---

## How to build a new track (the repeatable recipe)

Directory: `tutorials/<track>/`

1. **`nav.js`** — `renderSidebar([{title, items:[[label, "file.html"], ...]}, ...])`; last group = `Practice` with `["📝 Quizzes (10 sets × 20 Qs)","quiz.html"]`.
2. **~12 lesson `.html` files** in the v3 format (below). Push every ~4 lessons.
3. **`quiz-bank-1.js`** (sets 1–5) + **`quiz-bank-2.js`** (sets 6–10). Each set: `{title:"Quiz N · Topic", desc, questions:[{q, options:[3 strings], answer:<idx>, explain}×20]}`. Wrapped in `window.QUIZ_SETS=window.QUIZ_SETS||[]; window.QUIZ_SETS.push(...)`. Set 10 = mixed mock exam.
4. **`quiz.html`** — copy from `tutorials/css/quiz.html`, then replace `CSS Quizzes`→`X Quizzes`, `← CSS Track`→`← X Track`, `All CSS quizzes`→`All X quizzes`.
5. **Validate** the bank: `node -e "global.window={};require('./tutorials/<track>/quiz-bank-1.js');require('./tutorials/<track>/quiz-bank-2.js');const s=global.window.QUIZ_SETS;let t=0,b=0;s.forEach(x=>{t+=x.questions.length;b+=x.questions.filter(q=>!(q.answer>=0&&q.answer<q.options.length&&q.explain&&q.q)).length});console.log(s.length,t,b)"` → must print `10 200 0`.
6. Add the track's card link on the homepage `index.html` if not already present, and `git add -A && git commit && git push`.

### v3 lesson HTML skeleton
```
<header> logo + nav(← Track / Quizzes)  →  <div class="tutorial-layout"><aside class="sidebar" id="sidebar">
<main class="content">
  <h1>Title <span class="level-badge level-basic|level-adv|level-ultra">Basics</span></h1>
  <p>intro</p>
  <h2>…</h2>  <pre>code</pre>  <table class="tbl">…</table>  <div class="note">key insight</div>
  <h2>Common Mistakes</h2> <table class="tbl">…</table>
  <h2>Interview Questions</h2> 3× <details class="solution"><summary>Q</summary><p>A</p></details>
  <div class="exercise"><strong>🏋️ Practice:</strong> …</div>
  <div class="takeaways"><h3>🎯 Key Takeaways</h3><ul>…</ul></div>
  <div class="pager"> ← prev / next → </div>
</main>
<script src="../../js/sidebar.js"></script><script src="nav.js"></script>
```
**Content bar:** model-first (explain WHY, not just API), name the traps, cross-link to related lessons/tracks, cover the non-negotiable mid/senior concepts.

---

## Ops notes
- Shared assets: `css/style.css`, `js/sidebar.js` (renderSidebar), `js/quiz.js` (v2 engine: explanations after submit + retake), `playground/` (sandboxed iframe editor — used by frontend tracks).
- GitHub Pages occasionally fails deploy with a transient "try again later". Fix: `gh api repos/Dhruv36/learnhub/pages/builds -X POST`.
- Windows line-ending warnings on commit (LF→CRLF) are harmless.
