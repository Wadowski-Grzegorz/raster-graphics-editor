import copy


class LayerHistory:
    def __init__(self, event_provider, max_operations=10):
        self._history = []
        self._max_operations = max_operations
        self._event_provider = event_provider

    def push(self, data, operation: str):
        d_cp = copy.deepcopy(data)
        self._history.append((operation, d_cp))
        if len(self._history) > self._max_operations:
            self._history.pop(0)

    def pop(self):
        if not self._history:
            return False

        operation, data = self._history.pop()
        if operation == 'order':
            self._event_provider.notify({"type": "layer_order_history_pop", 'order': data})
        else:
            layer = data["layer"]
            self._event_provider.notify({
                "type": "layer_history_pop",
                "idx": layer.get_idx(),
                "layer": layer,
                "order": data["order"],
                "current_idx": data["current_idx"],
                "operation": operation
            })