
class EventListener:
    def __init__(self):
        self.event_types = {}

    def subscribe_to_events(self, event_provider, signal_event_occurred):
        for et in self.event_types:
            event_provider.subscribe(et, signal_event_occurred.emit)
        signal_event_occurred.connect(self.handle_event)

    def handle_event(self, data):
        handler = self.event_types.get(data.get('type'))
        if handler:
            handler(data)
