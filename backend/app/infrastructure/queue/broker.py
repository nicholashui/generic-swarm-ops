class QueueBroker:
    def publish(self, name: str, payload: dict) -> dict:
        return {"queue": name, "payload": payload}
