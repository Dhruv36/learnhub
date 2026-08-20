// AWS track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Foundations", items: [
    ["Shared Responsibility, Accounts & Regions", "index.html"],
    ["IAM: Identities, Policies & Evaluation", "iam-basics.html"],
    ["IAM Advanced: STS, Roles & Trust", "iam-deep-dive.html"],
    ["Cost: Pricing Models & Data Transfer", "billing-cost.html"]] },
  { title: "2. Networking", items: [
    ["VPCs, Subnets & Security Groups", "vpc-networking.html"],
    ["Connecting VPCs, PrivateLink & On-Prem", "connectivity.html"],
    ["Route 53, Load Balancers & CloudFront", "edge-dns.html"]] },
  { title: "3. Compute", items: [
    ["EC2, EBS & Auto Scaling", "ec2-compute.html"],
    ["ECS, EKS & Fargate", "containers.html"],
    ["Lambda & API Gateway", "lambda-serverless.html"]] },
  { title: "4. Data", items: [
    ["S3: Storage Classes, Access & Cost", "s3.html"],
    ["RDS & Aurora", "rds-aurora.html"],
    ["DynamoDB", "dynamodb.html"],
    ["SQS, SNS, EventBridge & Kinesis", "messaging.html"]] },
  { title: "5. Operations", items: [
    ["Observability: CloudWatch & X-Ray", "observability.html"],
    ["Infrastructure as Code", "iac.html"],
    ["Encryption, Secrets & Audit", "security-ops.html"]] },
  { title: "6. Architecture", items: [
    ["The Well-Architected Trade-offs", "well-architected.html"],
    ["Resilience & Disaster Recovery", "resilience-dr.html"],
    ["Scaling Patterns", "scaling-patterns.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
