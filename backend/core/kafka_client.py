from kafka import KafkaConsumer
from util import load_setting, LoadYaml
from pathlib import Path
import json

class KafkaClient:
    def __init__(self, path: Path):
        self.config = LoadYaml(path)['kafka']
    def kafka_consumer(self, topic):
        return KafkaConsumer(
            topic,
            bootstrap_servers = f"{load_setting.VM_IP}:{self.config['BOOTSTRAP_SERVERS']}",
            auto_offset_reset = self.config['auto_offset_reset'],
            enable_auto_commit=self.config['enable_auto_commit'],
            group_id= self.config['group_id'],
            value_deserializer=lambda x: json.loads(x.decode("utf-8"))
        )