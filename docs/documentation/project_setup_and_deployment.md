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
