# Kafka Docker Setup Guide

This README provides instructions on how to interact with Kafka running in Docker containers.

## Starting the Docker Containers

To start the Kafka and related services, we navigate to the project directory and run:

```bash
cd \kafka-docker
docker-compose up
```

This will start all the services defined in the `docker-compose.yml` file.

## Important Note

When running Kafka commands inside the container, we are using `broker:9092` instead of `localhost:9092`. This ensures that the Kafka client can connect to the broker running in the same Docker network.

## Accessing the Kafka Container

To access the Kafka container's shell:

```bash
docker exec -it broker sh
```

Once inside the container, we navigate to the Kafka bin directory:

```bash
cd /opt/kafka/bin/
```

## Common Kafka Operations

### Creating a Topic

```bash
./kafka-topics.sh --create --topic test-topic --bootstrap-server broker:9092 --partitions 1 --replication-factor 1
```

### Listing Topics

```bash
./kafka-topics.sh --list --bootstrap-server broker:9092
```

### Producing Messages

```bash
./kafka-console-producer.sh --bootstrap-server broker:9092 --topic test-topic
```

### Consuming Messages

```bash
./kafka-console-consumer.sh --topic test-topic --from-beginning --bootstrap-server broker:9092
```
