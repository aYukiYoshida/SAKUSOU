# -*- coding: utf-8 -*-
from __future__ import annotations

import copy
from abc import ABCMeta
from typing import Any, Dict, Tuple

from ._utility import str_to_snake_case


class Entity(object, metaclass=ABCMeta):
    PROPERTY_NAMES: Tuple[str, ...] = ()

    def __init__(self):
        pass

    @classmethod
    def from_response(cls, response: Dict[str, Any]):
        return cls(**{str_to_snake_case(name): response.get(name)
                      for name in cls.PROPERTY_NAMES})

    @property
    def properties(self) -> Dict[str, Any]:
        return {name: self.__dict__.get(str_to_snake_case(name))
                for name in self.PROPERTY_NAMES}

    def copy(self) -> Entity:
        return copy.deepcopy(self)
