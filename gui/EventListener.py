
class EventListener:
    event_types = {}

    def subscribe_to_events(self, event_provider):
        for type in self.event_types:
            event_provider.subscribe(type, self.emit_event_occurred)


    def emit_event_occurred(self, data):
        pass

    def handle_event(self, data):
        pass