from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'output_topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='output-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consuming processed messages...")

for message in consumer:
    print(f"Processed Message: {message.value['processed_message']}")