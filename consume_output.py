from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'output_topic',
    bootstrap_servers='localhost:19092',
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='output-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

print("Consuming processed messages...")

for message in consumer:
    processed_results = message.value.get('processed_results', [])
    for result in processed_results:
        print(f"Element: {result['element']}, Mass: {result['mass']}, KBOB UUID: {result['kbob_uuid']}, eBKP-H: {result['ebkp_h']}")
