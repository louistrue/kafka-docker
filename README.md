# Kafka Docker Setup Guide (Windows Edition)

This guide provides instructions on how to interact with Kafka running in Docker containers on a Windows system.

## Prerequisites

- **Docker Desktop for Windows**: Ensure that Docker is installed and running on your Windows machine.
- **Python**: Python 3.x installed for running Python scripts.
- **Command Prompt or PowerShell**: You can use either, but some commands may vary slightly.

## Starting the Docker Containers

To start Kafka and related services, navigate to your project directory in the Command Prompt or PowerShell:

```cmd
cd \path\to\kafka-docker
docker-compose up --build
```

- **Note**: Replace `\path\to\kafka-docker` with the actual path to your project directory.
- The `--build` flag ensures that any changes to your Docker configuration are applied.

This command will start all the services defined in the `docker-compose.yml` file.

## Important Notes

- **Inside Docker Containers**: When running Kafka commands inside a container (e.g., from the `broker` or `data_processor` containers), use `broker:9092` as the bootstrap server. This allows Kafka clients within the Docker network to connect to the broker.

- **From the Host Machine**: When running Kafka commands from the host machine (e.g., running `simulate_input.py` or `consume_output.py`), use `localhost:19092` as the bootstrap server. This is because the Kafka broker is configured to expose port `19092` for external connections.

## Accessing the Kafka Container

To access the Kafka container's shell from Windows:

1. Open Command Prompt or PowerShell.
2. Run the following command:

   ```cmd
   docker exec -it broker sh
   ```

   - **Note**: The `sh` shell is used inside the container. If you encounter issues, you can use `bash` if available.

3. Once inside the container, navigate to the Kafka bin directory:

   ```sh
   cd /opt/kafka/bin/
   ```

## Common Kafka Operations

### Creating a Topic

- **From Inside the Kafka Container**:

  ```sh
  ./kafka-topics.sh --create --topic test-topic --bootstrap-server broker:9092 --partitions 1 --replication-factor 1
  ```

- **From the Host Machine**:

  Since the Kafka scripts are inside the Docker container, you need to run them from within the container. Alternatively, you can run them from your host machine if you have Kafka installed locally.

  **Option 1: Run from the Container**

  ```cmd
  docker exec -it broker sh -c "/opt/kafka/bin/kafka-topics.sh --create --topic test-topic --bootstrap-server broker:9092 --partitions 1 --replication-factor 1"
  ```

  **Option 2: If Kafka is Installed Locally on Windows**

  If you have Kafka installed on your Windows machine, you can run:

  ```cmd
  .\bin\windows\kafka-topics.bat --create --topic test-topic --bootstrap-server localhost:19092 --partitions 1 --replication-factor 1
  ```

  - **Note**: Replace `.\bin\windows\` with the path to your local Kafka installation's `bin\windows\` directory.

### Listing Topics

- **From Inside the Kafka Container**:

  ```sh
  ./kafka-topics.sh --list --bootstrap-server broker:9092
  ```

- **From the Host Machine**:

  ```cmd
  docker exec -it broker sh -c "/opt/kafka/bin/kafka-topics.sh --list --bootstrap-server broker:9092"
  ```

  **Or, if Kafka is installed locally:**

  ```cmd
  .\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:19092
  ```

### Producing Messages

- **From Inside the Kafka Container**:

  ```sh
  ./kafka-console-producer.sh --bootstrap-server broker:9092 --topic test-topic
  ```

  - Type your messages and press Enter to send them.

- **From the Host Machine**:

  **Option 1: Using Docker Exec**

  ```cmd
  docker exec -it broker sh -c "/opt/kafka/bin/kafka-console-producer.sh --bootstrap-server broker:9092 --topic test-topic"
  ```

  **Option 2: If Kafka is Installed Locally:**

  ```cmd
  .\bin\windows\kafka-console-producer.bat --bootstrap-server localhost:19092 --topic test-topic
  ```

### Consuming Messages

- **From Inside the Kafka Container**:

  ```sh
  ./kafka-console-consumer.sh --bootstrap-server broker:9092 --topic test-topic --from-beginning
  ```

- **From the Host Machine**:

  **Option 1: Using Docker Exec**

  ```cmd
  docker exec -it broker sh -c "/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server broker:9092 --topic test-topic --from-beginning"
  ```

  **Option 2: If Kafka is Installed Locally:**

  ```cmd
  .\bin\windows\kafka-console-consumer.bat --bootstrap-server localhost:19092 --topic test-topic --from-beginning
  ```

## Kafka Configuration Details

The Kafka broker is configured with multiple listeners to handle both internal and external connections.

- **Listeners Configuration**:

  - `KAFKA_LISTENERS`: Defines where the broker listens for incoming connections.

    - `INTERNAL://broker:9092`: For internal Docker container communication.
    - `EXTERNAL://0.0.0.0:19092`: Listens on all interfaces on port `19092` for external connections.
    - `CONTROLLER://:9093`: For controller communication.

  - `KAFKA_ADVERTISED_LISTENERS`: Defines the addresses that the broker advertises to clients.
    - `INTERNAL://broker:9092`: Advertised to internal Docker containers.
    - `EXTERNAL://localhost:19092`: Advertised to external clients (host machine).

- **Listener Security Protocol Map**:

  - `KAFKA_LISTENER_SECURITY_PROTOCOL_MAP`: Maps listener names to security protocols.
    - `INTERNAL:PLAINTEXT`
    - `EXTERNAL:PLAINTEXT`
    - `CONTROLLER:PLAINTEXT`

- **Inter-Broker Listener Name**:

  - `KAFKA_INTER_BROKER_LISTENER_NAME`: Specifies the listener used for inter-broker communication.
    - Set to `INTERNAL`.

## Adjusting Your Python Scripts

- **For Scripts Running on the Host Machine** (e.g., `simulate_input.py`, `consume_output.py`):

  ```python
  # Use 'localhost:19092' for bootstrap servers
  bootstrap_servers = 'localhost:19092'
  ```

- **For Scripts Running Inside Docker Containers** (e.g., `data_processor.py`):

  ```python
  # Use 'broker:9092' for bootstrap servers
  bootstrap_servers = 'broker:9092'
  ```

## Running the Data Processor Application

### 1. Start the Docker Containers

In Command Prompt or PowerShell, navigate to your project directory and run:

```cmd
cd \path\to\kafka-docker
docker-compose up --build
```

### 2. Create the Required Kafka Topics

Since the Kafka utilities are inside the Docker container, you can execute them using `docker exec`.

```cmd
docker exec -it broker sh -c "/opt/kafka/bin/kafka-topics.sh --create --topic input_topic --bootstrap-server broker:9092 --partitions 1 --replication-factor 1"
docker exec -it broker sh -c "/opt/kafka/bin/kafka-topics.sh --create --topic output_topic --bootstrap-server broker:9092 --partitions 1 --replication-factor 1"
```

### 3. Run the Consumer Script on the Host Machine

Ensure your `consume_output.py` script has `bootstrap_servers` set to `'localhost:19092'`.

In Command Prompt or PowerShell:

```cmd
python consume_output.py
```

- You should see:

  ```
  Consuming processed messages...
  ```

### 4. Run the Producer Script on the Host Machine

Ensure your `simulate_input.py` script has `bootstrap_servers` set to `'localhost:19092'`.

In a new Command Prompt or PowerShell window:

```cmd
python simulate_input.py
```

- You should see:

  ```
  Sent RDF Turtle data
  Sent RDF Turtle data
  ```

### 5. Monitor the Output

Check the window where `consume_output.py` is running. You should see the processed messages appearing:

```
Consuming processed messages...
Element: http://example.org/element1, Mass: 25000.0, KBOB UUID: UUID-123, eBKP-H: E1
Element: http://example.org/element2, Mass: 19200.0, KBOB UUID: UUID-456, eBKP-H: E2
```

## Troubleshooting

### Connection Errors from the Host Machine

- **DNS Lookup Failed for `broker:9092`**:

  - Ensure that you are using `localhost:19092` as the bootstrap server in your host machine scripts.

- **Port Not Accessible**:

  - Verify that port `19092` is exposed in the `docker-compose.yml` and not used by other services.
  - You can check if the port is listening using:

    ```cmd
    netstat -ano | findstr 19092
    ```

### Connection Errors Inside Docker Containers

- **Unable to Connect to Kafka Broker**:

  - Ensure that services within Docker are using `broker:9092` as the bootstrap server.

- **Service Names and Networking**:

  - Docker Compose sets up a default network where services can communicate using their service names. Ensure that the service name `broker` is correct.

### Kafka Topics Not Found

- **Topics Not Created**:

  - Ensure that the topics you are trying to access have been created. You can create topics using the `kafka-topics.sh` script inside the Kafka container, as shown above.

### Windows Line Endings

- Be cautious about line endings in scripts. Windows uses `CRLF` (`\r\n`), which can sometimes cause issues in scripts that expect Unix-style `LF` (`\n`). Ensure that your text editor is configured to use Unix-style line endings for scripts that will run inside Docker containers.

## Additional Resources

- **Apache Kafka Documentation**: [https://kafka.apache.org/documentation/](https://kafka.apache.org/documentation/)
- **Docker Desktop for Windows**: [https://docs.docker.com/desktop/windows/](https://docs.docker.com/desktop/windows/)
- **Kafka Python Client (`kafka-python`)**: [https://kafka-python.readthedocs.io/en/master/](https://kafka-python.readthedocs.io/en/master/)
- **rdflib Documentation**: [https://rdflib.readthedocs.io/en/stable/](https://rdflib.readthedocs.io/en/stable/)
