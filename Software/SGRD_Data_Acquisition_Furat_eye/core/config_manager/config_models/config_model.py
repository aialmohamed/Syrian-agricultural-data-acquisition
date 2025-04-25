from typing import Type, TypeVar, Generic
from dataclasses import is_dataclass

T = TypeVar("T")

class ConfigModel(Generic[T]):
    def __init__(self, config_section: dict, model_class: Type[T]):
        if not is_dataclass(model_class):
            raise TypeError(f"{model_class.__name__} must be a dataclass")

        self._model = model_class(**config_section)

    @property
    def model(self) -> T:
        return self._model