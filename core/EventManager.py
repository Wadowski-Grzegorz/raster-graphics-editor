class EventManager:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name, listener):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def unsubscribe(self, event_name, listener):
        if event_name in self._listeners:
            self._listeners[event_name].remove(listener)

    def notify(self, event_name, data):
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(data)