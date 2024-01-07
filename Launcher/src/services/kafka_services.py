"""
Module to properly manage kafka instance
"""

import json
import logging
import kafka


class _Exceptions:
    """Manage kafka services errors"""

    kafka_not_running = ("kafka server could not be resolved "
                         "check connection to %s")

    write_timeout = "Kafka write operation timeout"

    unable_to_read_output = ("An exception occured while reading "
                             "output data")


class KafkaServices:
    """
    Kafka Services to properly manage kafka instance
    """

    _log = logging.getLogger(__name__)

    def __init__(self, server_ip='localhost', server_port='9093'):
        """
        Init Kafka producer distributed on provided server_ip and server_port
        """

        server_addr = server_ip + ':' + server_port

        try:

            self.producer = kafka.KafkaProducer(
                bootstrap_servers=server_addr,
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )

            connect_status = self.producer.bootstrap_connected()
            self._log.info("Initialized Kafka on %s, status: %s",
                           server_addr,
                           connect_status)

        except kafka.errors.NoBrokersAvailable:
            self._log.error(_Exceptions.kafka_not_running, server_addr)
            exit(1)

    def write(self, file_path: str, topic='launcher', timeout=60):
        """
        Write the content of the provided file into kafka
        """

        try:
            file = open(file_path, encoding='utf-8')
            data = json.load(file)

            future = self.producer.send(topic, data)

            # Block until message is sent (or timeout)
            result = future.get(timeout=timeout)
            self._log.info("Kafka write result: %s", result)

        except FileNotFoundError:
            self._log.error(_Exceptions.unable_to_read_output)
            exit(1)
        except kafka.errors.KafkaTimeoutError:
            self._log.error(_Exceptions.write_timeout)
            exit(1)
