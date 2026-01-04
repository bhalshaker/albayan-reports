```sh
podman run -d --name dynamodb-local -p 8000:8000 docker.io/amazon/dynamodb-local:latest
```

```sh
AWS_ACCESS_KEY_ID=dummy AWS_SECRET_ACCESS_KEY=dummy \
aws dynamodb list-tables \
--endpoint-url http://localhost:8000 \
--region us-east-1
```

```sh
podman run -d --name dynamodb-admin \
  -p 8001:8001 \
  -e DYNAMO_ENDPOINT=http://localhost:8000 \
  -e AWS_REGION=us-east-1 \
  -e AWS_ACCESS_KEY_ID=dummy \
  -e AWS_SECRET_ACCESS_KEY=dummy \
  --net=host \
  aaronshaf/dynamodb-admin
```

```sh
AWS_ACCESS_KEY_ID=dummy AWS_SECRET_ACCESS_KEY=dummy \
aws dynamodb list-tables \
--endpoint-url http://localhost:8000 \
--region us-east-1
```

```sh
terraform init
```

```sh
TF_VAR_is_local=true TF_VAR_aws_region=us-east-1 TF_VAR_access_key=dummy TF_VAR_secret_key=dummy TF_VAR_dynamodb=http://localhost:8000 \
terraform apply
```

```sh

```

```sh
cd /home/devnation/vscode/albayan-reports/apps/backendworker
uvicorn albayanworker.main:app --port 8080
```

```sh
cd infra/containers
podman-compose up -d --build
```
