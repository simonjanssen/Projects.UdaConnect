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

2. Deploy with ArgoCD:
```bash
kubectl apply -f argocd/udaconnect.yaml
```

3. Sync applications: 
    - For this project, auto-sync is not enabled so you need to sync the apps manually.
    - The ArgoCD setup follows the [App of Apps Pattern](https://argo-cd.readthedocs.io/en/stable/operator-manual/cluster-bootstrapping/). The **udaconnect** app acts as the parent app that needs to be synced first.
    - You can then sync all the other apps. I would recommend to sync **configuration**, **postgres** and **kafka** apps first as the other apps depend on them.

4. Available endpoints after cluster startup:
    - The following endpoints are externally available on your host system:
        - [localhost:30100](http://localhost:30100): pgAdmin Frontend
        - [localhost:30101](http://localhost:30101): Udaconnect Frontend
        - [localhost:30102](http://localhost:30102): LocationAPI
        - [localhost:30103](http://localhost:30103): PersonAPI
    - The following endpoints are cluster-internal only:
        - [postgres-svc:5432](tcp://postgres-svc:5432): PostgreSQL database
        - [kafka:9092](tcp://kafka:9092): Kafka server
        - [person-service-svc:5005](tcp://person-service-svc:5005): gRPC server

5. Generate some data:
    - Generate some mock persons using the **PersonAPI** endpoint (cf. [postman collection](docs/postman.json)). The interactive SwaggerUI provides you with some mock data you can directly `post`. I would recommend to add at least two different persons.
    - Generate some mock location data using the **LocationAPI** endpoint (cf. [postman collection](docs/postman.json)). Again, you can use the interactive SwaggerUI to `post` some data. Alternatively, you can start mock clients that generate some random location data for particular `persons`:
```bash
python applications/udaconnect-test-clients/client.py -i PERSON_ID
```

Note that due to the async database update (`location-service`) and the async connections calculation (`exposure-service`) it may take two or three minutes until you see the data in the **frontend**.


## Architecture

Architecture decisions are described in [docs/architecture_decisions](docs/architecture_decisions.txt).

Architecture diagram:
![architecture diagram](docs/architecture_design.png)


## OpenAPI Documentation

The refactored applications implements two REST APIs. The OpenAPI documentation is auto-generated using [FastAPI Interactive Docs](https://fastapi.tiangolo.com/#interactive-api-docs) based on the [Pydantic Models](https://docs.pydantic.dev/latest/concepts/models/) in [build/types/schemas.py](build/types/schemas.py).

Once you have deployed the application, the interactive SwaggerUI is available at the `/docs` endpoint for both APIs. You can also find a copy of both docs in [docs/openapi](docs/openapi/).
- **LocationAPI**: [localhost:30102/docs](http://localhost:30102/docs) (or [docs/openapi/LocationAPI.json](docs/openapi/LocationAPI.json))
- **PersonAPI**: [localhost:30103/docs](http://localhost:30103/docs) (or [docs/openapi/PersonAPI.json](docs/openapi/PersonAPI.json))


## Postman Collection

