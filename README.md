## 1. Built infra on GCP using:
  * Ansible in ./infrastructure/ansible
  * Terraform in ./infrastructure/terraform
## 2. Infra scheme
1 Load Balancer --> 2 app instances --> 1 DB Instance
## 3. CI/CD system - Github Acions
Manifests in ./github/workflows
