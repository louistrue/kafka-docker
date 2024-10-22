from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'output_topic',
    bootstrap_servers='localhost:19092',
    auto_offset_reset='latest',  # Change this to 'latest' to only get new messages
    enable_auto_commit=True,
    group_id='output-consumer-group',
    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
    api_version=(2, 5, 0)  # Add this line to specify the API version
)

print("Consuming processed messages...")

# Dictionary to store the latest result for each element
latest_results = {}

for message in consumer:
    processed_results = message.value.get('processed_results', [])
    for result in processed_results:
        element = result['element']
        
        # Check if the new format (combined_value) is present
        if 'combined_value' in result:
            combined_value = result['combined_value']
        else:
            # If not, construct it from the old format
            kbob_uuid = result.get('kbob_uuid', 'Unknown')
            ebkp_h = result.get('ebkp_h', 'Unknown')
            combined_value = f"{kbob_uuid}_{ebkp_h}"
        
        latest_results[element] = combined_value
        
        # Print the latest result for each element
        print(f"Element: {element}, Combined Value: {combined_value}")

    # Optional: Clear the console to only show the latest state
    # import os
    # os.system('cls' if os.name == 'nt' else 'clear')
    # for element, combined_value in latest_results.items():
    #     print(f"Element: {element}, Combined Value: {combined_value}")
