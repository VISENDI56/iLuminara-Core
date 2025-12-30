# ------------------------------------------------------------------------------
# Copyright (c) 2025 iLuminara (VISENDI56). All Rights Reserved.
# Licensed under the Polyform Shield License 1.0.0.
# 
# COMPETITOR EXCLUSION: Commercial use by entities offering Sovereign/Health OS 
# solutions is STRICTLY PROHIBITED without a commercial license.
# 
# The Sovereign Immune System (Omni-Law) and JEPA-MPC Architecture are 
# proprietary inventions of iLuminara.
# ------------------------------------------------------------------------------

# Event-driven message bus for robust data synchronization

import os
import json
from typing import Any

class KafkaProducer:
    def __init__(self, brokers=None, topic="iluminara-events"):
        self.brokers = brokers or os.getenv("KAFKA_BROKERS", "localhost:9092")
        self.topic = topic
        try:
            from kafka import KafkaProducer as KP
            self.producer = KP(bootstrap_servers=self.brokers)
        except ImportError:
            self.producer = None
            print("Kafka not available, will use disk fallback.")

    def send(self, event: Any):
        data = json.dumps(event).encode()
        if self.producer:
            self.producer.send(self.topic, data)
        else:
            # Fallback: append to local disk buffer
            with open("offline_event_buffer.jsonl", "a") as f:
                f.write(json.dumps(event) + "\n")
