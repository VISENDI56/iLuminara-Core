import json

class HealthIoTGateway:
    """
    Handles incoming telemetry from LoRaWAN/MQTT sensors.
    """
    def on_message_received(self, topic, payload):
        data = json.loads(payload)
        sensor_type = data.get("type")
        
        print(f"   📡 [IoT Gateway] Data from {topic}: {data}")
        # Route to TargetedSanitationAgent or ColdChainMonitor
        return {"route": "PUBLIC_HEALTH_STACK", "data": data}

if __name__ == "__main__":
    gateway = HealthIoTGateway()
    gateway.on_message_received("sensors/district_9/water", '{"type": "coliform", "value": 450}')