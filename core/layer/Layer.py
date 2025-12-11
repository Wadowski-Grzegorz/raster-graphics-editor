from abc import abstractmethod


class Layer:
    id_counter = 0
    def __init__(
            self,
            visible: bool,
            position: tuple,
            name: str,
        ):

        super().__init__()

        Layer.id_counter += 1
        self._idx = Layer.id_counter
        self._visible = visible
        self._position = position # x, y
        self._name = name

    def get_id(self) -> int:
        return self._idx

    def get_visible(self):
        return self._visible

    def get_position(self):
        return self._position

    def get_name(self) -> str:
        return self._name

    def switch_visible(self):
        self._visible = not self._visible

    def move(self, dx, dy):
        self._position = (self._position[0] + dx, self._position[1] + dy)

    @abstractmethod
    def get_layer(self):
        pass

    @abstractmethod
    def get_layer_q(self):
        pass

    @abstractmethod
    def can_change(self) -> bool:
        pass