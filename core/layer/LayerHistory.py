import copy


class LayerHistory:
    def __init__(self, max_actions=30):
        self._undo = [] # (data, action)
        self._redo = [] # (data, action)
        self._max_actions = max_actions

    def add_undo(self, data, action: str, reset=True):
        d_cp = copy.deepcopy(data)
        self._undo.append((d_cp, action))
        if reset:
            self._redo.clear()

        if len(self._undo) > self._max_actions:
            self._undo.pop(0)

    def undo(self):
        if not self._undo:
            return
        
        snap = self._undo.pop()
        return snap

    def add_redo(self, data, action: str): 
        d_cp = copy.deepcopy(data)
        self._redo.append((d_cp, action))
        if len(self._redo) > self._max_actions:
            self._redo.pop(0)
    
    def redo(self):
        if not self._redo:
            return
        
        snap = self._redo.pop()
        return snap