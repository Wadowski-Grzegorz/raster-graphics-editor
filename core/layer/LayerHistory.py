import copy


class LayerHistory:
    def __init__(self, max_actions=10):
        self._history = [] # (data, action)
        self._max_actions = max_actions

    def push(self, data, action: str):
        d_cp = copy.deepcopy(data)
        self._history.append((d_cp, action))
        if len(self._history) > self._max_actions:
            self._history.pop(0)

    def pop(self):
        if not self._history:
            return

        return self._history.pop()