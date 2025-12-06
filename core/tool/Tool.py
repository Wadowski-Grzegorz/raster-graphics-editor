from abc import abstractmethod, ABC


class Tool(ABC):
    id_counter = 0

    def __init__(self, name: str = 'Tool'):
        super().__init__()

        Tool.id_counter += 1
        self._idx = Tool.id_counter
        self._name = name

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> int:
        return self._idx