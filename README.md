## 1. Built infra on GCP using:
  * Ansible in ./infrastructure/ansible
  * Terraform in ./infrastructure/terraform
## 2. Infra scheme
  GCP Load Balancer + HTTP healthcheck --> 2 app instances --> 1 DB Instance (Postgres)
## 3. CI/CD system - Github Acions
Manifests in ./github/workflows
check addr - http://35.239.242.112/health

