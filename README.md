# Github Actions Test project
## 1. Built infra on GCP using:
  * Ansible in ./infrastructure/ansible
  * Terraform in ./infrastructure/terraform
## 2. Infra scheme
  GCP Load Balancer + HTTP healthcheck --> 2 app instances --> 1 DB Instance (Postgres)
## 3. CI/CD system - Github Acions
Manifests in ./github/workflows
check addr - http://35.239.242.112/health

## 4. Request Example
### Write
```
curl -H "Content-Type: application/json"  -X PUT -d '{"dateOfBirth":"2019-01-23"}' 35.239.242.112/hello/username
```

### Read
curl 35.239.242.112/hello/username
```
{"message":"Hello username! Your birthday is in 129 days"}
```
