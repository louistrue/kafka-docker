from kafka import KafkaProducer
import time
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

messages = ['Message 1', 'Message 2', 'Message 3']

for msg in messages:
    producer.send('input_topic', {'message': msg})
    print(f"Sent: {msg}")
    time.sleep(1)  # Simulate delay

producer.flush()
producer.close()