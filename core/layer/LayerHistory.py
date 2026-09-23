import copy

class LayerHistory:
    def __init__(self, context, max_operations=10):
        self._history = [] # (operation, Layer)
        self._max_operations = max_operations
        self._context = context

    def push(self, layer, operation: str):
        l_cp = copy.deepcopy(layer)
        ob = (operation, l_cp)
        self._history.append(ob)
        if len(self._history) > self._max_operations:
            self._history.pop(0)

    def pop(self):
        if not self._history:
            return False

        operation, layer = self._history.pop()
        self._context.event_provider.notify({"type": "layer_history_pop", "idx": layer.idx, "layer": layer, "operation": operation})