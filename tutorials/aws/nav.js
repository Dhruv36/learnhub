// AWS track curriculum — single source of truth for every page's sidebar.
renderSidebar([
  { title: "1. Basics", items: [
    ["Accounts, IAM & Regions", "index.html"],
    ["EC2 & Auto Scaling", "ec2-compute.html"],
    ["S3 & CloudFront", "s3-cloudfront.html"],
    ["VPC Networking", "vpc-networking.html"]] },
  { title: "2. Intermediate", items: [
    ["RDS & DynamoDB", "rds-dynamodb.html"],
    ["Lambda & API Gateway", "lambda-serverless.html"],
    ["SQS, SNS & EventBridge", "messaging.html"],
    ["ECS / EKS / Fargate", "containers.html"]] },
  { title: "3. Advanced", items: [
    ["IAM Deep Dive (policies, roles, STS)", "iam-deep-dive.html"],
    ["Observability (CloudWatch, X-Ray)", "observability.html"]] },
  { title: "4. Ultra-Advanced (Production)", items: [
    ["Infrastructure as Code (Terraform/CDK)", "iac.html"],
    ["Well-Architected: Cost, Multi-region & DR", "well-architected.html"]] },
  { title: "Practice", items: [
    ["📝 Quizzes (10 sets × 20 Qs)", "quiz.html"]] }
]);
