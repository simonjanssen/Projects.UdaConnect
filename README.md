# Projects.UdaConnect

## Repository Structure

- [applications](applications): source code for all refactored custom microservices
- [build/types](build/types): common models, schemas and proto files shared with all applications. These files are copied within the ci-workflow to avoid duplicates and allow central management of all message definitions.
- [.github/workflows/app-build.yaml](.github/workflows/app-build.yaml): github ci-workflow to build and push applications to docker hub registry [hub.docker.com/u/simonshub](https://hub.docker.com/u/simonshub)
- [argocd](argocd): argocd application config files. Follows the `app of apps` schema.
- [charts](charts): helm charts for Kafka (copied from [bitnami/kafka](https://github.com/bitnami/charts/tree/main/bitnami/kafka))
- [manifests](manifests): kubernetes declarative deployment manifests for all other applications
- [docs](docs): additional documentation required for project submission


## How To Run This Project

Assuming you have kubernetes, kubectl and argocd ready:

1. Configure volumes on host: [pgadmin](https://www.pgadmin.org/docs/pgadmin4/latest/container_deployment.html#mapped-files-and-directories) and [kafka](https://github.com/bitnami/containers/blob/main/bitnami/kafka/README.md#persisting-your-data) need specific user ids on host to access mounted volumes from their containers.

```bash
mkdir -p /mnt/data/postgres
mkdir -p /mnt/data/pgadmin
mkdir -p /mnt/data/kafka
chown -R 5050:5050 /mnt/data/pgadmin
chown -R 1001:1001 /mnt/data/kafka 
```

2. Deploy with argocd:
```bash
kubectl apply -f argocd/udaconnect.yaml
```

## Architecture

Architecture decisions are described in [docs/architecture_decisions](docs/architecture_decisions.txt).

Architecture diagram:
![architecture diagram](docs/architecture_design.png)


## OpenAPI Documentation

The refactored applications implements two REST APIs. The OpenAPI documentation is auto-generated using [FastAPI Interactive Docs](https://fastapi.tiangolo.com/#interactive-api-docs) based on the [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/) in [build/types/schemas.py](build/types/schemas.py).

Once you have deployed the application, the interactive SwaggerUI is available at the `/docs` endpoint for both APIs. You can also find a copy of both docs in [docs/openapi](docs/openapi/).
- **LocationAPI**: [localhost:30102/docs](localhost:30102/docs) (or [docs/openapi/LocationAPI.json](docs/openapi/LocationAPI.json))
- **PersonAPI**: [localhost:30103/docs](localhost:30103/docs) (or [docs/openapi/PersonAPI.json](docs/openapi/PersonAPI.json))


## Postman Collection

