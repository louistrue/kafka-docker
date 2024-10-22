from kafka import KafkaConsumer, KafkaProducer
import os
import json
from rdflib import Graph, Namespace, RDF, Literal
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Get Kafka bootstrap servers from environment variable
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'broker:9092')

# Initialize consumer to read from 'input_topic'
consumer = KafkaConsumer(
    'input_topic',
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-processor-group',
    value_deserializer=lambda x: x.decode('utf-8')
)

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
        density = g.value(s, ex.density)
        volume = g.value(s, ex.volume)
        kbob_uuid = g.value(s, ex.kbobUuid)
        ebkp_h = g.value(s, ex.ebkpH)

        # Convert literals to Python types
        density = float(density) if isinstance(density, Literal) else None
        volume = float(volume) if isinstance(volume, Literal) else None
        kbob_uuid = str(kbob_uuid) if kbob_uuid else None
        ebkp_h = str(ebkp_h) if ebkp_h else None

        # Example processing: calculate mass = density * volume
        if density is not None and volume is not None:
            mass = density * volume
            result = {
                'element': str(s),
                'mass': mass,
                'kbob_uuid': kbob_uuid,
                'ebkp_h': ebkp_h
            }
            processed_results.append(result)
            logging.info(f"Processed element {s}: mass = {mass}")
        else:
            logging.warning(f"Missing density or volume for element {s}")

    if processed_results:
        # Send processed data to 'output_topic'
        producer.send('output_topic', {'processed_results': processed_results})
        producer.flush()
        logging.info("Sent processed results to output_topic")
    else:
        logging.warning("No valid data to process in this message")
