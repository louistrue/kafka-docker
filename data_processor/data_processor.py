from kafka import KafkaConsumer, KafkaProducer
import os
import json
from rdflib import Graph, Namespace, RDF, Literal
import logging
import time
from kafka.errors import NoBrokersAvailable

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get Kafka bootstrap servers from environment variable
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'broker:9092')

# Function to create Kafka consumer with retry logic
def create_kafka_consumer(max_retries=5, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            consumer = KafkaConsumer(
                'input_topic',
                bootstrap_servers=bootstrap_servers,
                auto_offset_reset='earliest',
                enable_auto_commit=True,
                group_id='my-processor-group',
                value_deserializer=lambda x: x.decode('utf-8')
            )
            logging.info("Successfully connected to Kafka broker")
            return consumer
        except NoBrokersAvailable:
            logging.warning(f"No brokers available. Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
            retries += 1
    raise Exception("Failed to connect to Kafka broker after multiple attempts")

# Initialize consumer to read from 'input_topic'
consumer = create_kafka_consumer()

# Initialize producer to write to 'output_topic'
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Starting data processor...")

for message in consumer:
    turtle_data = message.value
    logging.info(f"Received Turtle data:\n{turtle_data}")

    # Parse the RDF Turtle data
    g = Graph()
    try:
        g.parse(data=turtle_data, format='turtle')
    except Exception as e:
        logging.error(f"Error parsing RDF data: {e}")
        continue  # Skip to the next message

    # Process the RDF data
    # For example, extract subjects of type ex:Element and get their properties
    ex = Namespace('http://example.org/')

    processed_results = []
    for s in g.subjects(RDF.type, ex.Element):
        # Extract properties
        kbob_uuid = g.value(s, ex.kbobUuid)
        ebkp_h = g.value(s, ex.ebkpH)

        # Convert literals to Python types
        kbob_uuid = str(kbob_uuid) if kbob_uuid else None
        ebkp_h = str(ebkp_h) if ebkp_h else None

        # Perform some processing
        if kbob_uuid and ebkp_h:
            combined_value = f"{kbob_uuid}_{ebkp_h}"
            processed_results.append({
                'element': str(s),
                'combined_value': combined_value
            })

    if processed_results:
        # Send processed data to 'output_topic'
        producer.send('output_topic', {'processed_results': processed_results})
        producer.flush()
        logging.info("Sent processed results to output_topic")
    else:
        logging.warning("No valid data to process in this message")
