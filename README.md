# Projects.UdaConnect


## Deployment

Configure volumes on host: [pgadmin](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html#mapped-files-and-directories) and [kafka](https://github.com/bitnami/containers/blob/main/bitnami/kafka/README.md#persisting-your-data) need specific user ids on host to access mounted volumes from within containers.

```bash
mkdir -p /mnt/data/postgres
mkdir -p /mnt/data/pgadmin
mkdir -p /mnt/data/kafka
chown -R 5050:5050 /mnt/data/pgadmin
chown -R 1001:1001 /mnt/data/kafka 
```

Deploy with argocd:
```bash
kubectl apply -f argocd/udaconnect.yaml
```