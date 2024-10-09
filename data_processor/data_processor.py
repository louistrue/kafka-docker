from kafka import KafkaConsumer, KafkaProducer
import os
import json

# Get Kafka bootstrap servers from environment variable
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'broker:9092')

# Initialize consumer to read from 'input_topic'
consumer = KafkaConsumer(
    'input_topic',
    bootstrap_servers=bootstrap_servers,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-processor-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# Initialize producer to write to 'output_topic'
producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

print("Starting data processor...")

for message in consumer:
    input_data = message.value['message']
    print(f"Received: {input_data}")

    # Process the data (e.g., convert to uppercase)
    processed_data = input_data.upper()
    print(f"Processed: {processed_data}")

    # Send processed data to 'output_topic'
    producer.send('output_topic', {'processed_message': processed_data})
    producer.flush()