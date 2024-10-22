from kafka import KafkaProducer
import time
import uuid

producer = KafkaProducer(
    bootstrap_servers='localhost:19092',
    value_serializer=lambda x: x.encode('utf-8')
)

def generate_turtle_message(element_id, kbob_uuid, ebkp_h):
    return f"""
    @prefix ex: <http://example.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:element{element_id} a ex:Element ;
        ex:kbobUuid "{kbob_uuid}" ;
        ex:ebkpH "{ebkp_h}" .
    """

# Initial messages
turtle_messages = [
    generate_turtle_message(1, "BD66B05D-27E3-4ADF-85A2-E0ABBBA686A5", "C02.01"),
    generate_turtle_message(2, "B9689582-8BDE-4FE1-849D-BBBED840E410", "C04.02")
]

# Function to generate new messages
def generate_new_messages():
    new_element_id = len(turtle_messages) + 1
    new_kbob_uuid = str(uuid.uuid4()).upper()
    new_ebkp_h = f"C{new_element_id:02d}.{new_element_id:02d}"
    
    # New message
    turtle_messages.append(generate_turtle_message(new_element_id, new_kbob_uuid, new_ebkp_h))
    
    # Update an existing message (if there's more than one)
    if len(turtle_messages) > 1:
        update_index = (new_element_id - 1) % (len(turtle_messages) - 1)  # Cycle through existing messages
        updated_kbob_uuid = str(uuid.uuid4()).upper()
        updated_ebkp_h = f"U{update_index+1:02d}.{update_index+1:02d}"
        turtle_messages[update_index] = generate_turtle_message(update_index + 1, updated_kbob_uuid, updated_ebkp_h)

# Generate new messages until we have 10 in total
while len(turtle_messages) < 10:
    generate_new_messages()

print(f"Sending {len(turtle_messages)} messages...")

for msg in turtle_messages:
    producer.send('input_topic', msg)
    print(f"Sent RDF Turtle data")
    time.sleep(1)  # Simulate delay

producer.flush()
producer.close()

print("All messages sent. Run this script again to send more messages and updates.")
