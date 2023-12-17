from kafka import KafkaProducer, errors
import json

class KafkaServices:

    def __init__(self, server_ip = 'localhost', server_port='9093'):
        
        serializer = lambda v: json.dumps(v).encode('utf-8')
        server_addr = server_ip + ':' + server_port
        
        
        self.producer = KafkaProducer(
            bootstrap_servers=server_addr, 
            value_serializer=serializer
        )

        connect_status = self.producer.bootstrap_connected()
        print("Initialized Kafka on {}, connection status: {}".format(server_addr, connect_status))


    def write(self, file_path: str, topic = 'launcher', timeout = 60):

        file = open(file_path)
        data = json.load(file)

        future = self.producer.send(topic, data)
    
        # Block until message is sent (or timeout)
        result = future.get(timeout=timeout)
        print(result)