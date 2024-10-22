from kafka import KafkaProducer
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:19092',
    value_serializer=lambda x: x.encode('utf-8')
)

turtle_messages = [
    """
    @prefix ex: <http://example.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:element1 a ex:Element ;
        ex:density "2500"^^xsd:float ;
        ex:volume "10"^^xsd:float ;
        ex:kbobUuid "UUID-123" ;
        ex:ebkpH "E1" .
    """,
    """
    @prefix ex: <http://example.org/> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    ex:element2 a ex:Element ;
        ex:density "2400"^^xsd:float ;
        ex:volume "8"^^xsd:float ;
        ex:kbobUuid "UUID-456" ;
        ex:ebkpH "E2" .
    """
]

for msg in turtle_messages:
    producer.send('input_topic', msg)
    print(f"Sent RDF Turtle data")
    time.sleep(1)  # Simulate delay

producer.flush()
producer.close()
