"""
Kafka Services to properly manage kafka instace
"""

import json
from kafka import KafkaProducer


class KafkaServices:
    """
    Kafka Services to properly manage kafka instace
    """

    def __init__(self, server_ip='localhost', server_port='9093'):
        """
        Init Kafka producer distributed on provided server_ip and server_port
        """

        server_addr = server_ip + ':' + server_port

        self.producer = KafkaProducer(
            bootstrap_servers=server_addr,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

        connect_status = self.producer.bootstrap_connected()
        print(f"Initialized Kafka on {server_addr}, status: {connect_status}")

    def write(self, file_path: str, topic='launcher', timeout=60):
        """
        Write the content of the provided file into kafka
        """

        file = open(file_path, encoding='utf-8')
        data = json.load(file)

        future = self.producer.send(topic, data)

        # Block until message is sent (or timeout)
        result = future.get(timeout=timeout)
        print(result)
