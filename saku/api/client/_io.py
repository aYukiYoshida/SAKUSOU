# -*- coding: utf-8 -*-
import json
import pathlib
from typing import Any, Dict, Optional, Union

import yaml


def read_json(file_path: Union[str, pathlib.Path]) -> Dict[str, Any]:
    if isinstance(file_path, pathlib.Path):
        file_path = file_path.as_posix()
    with open(file_path, 'r') as f:
        return json.loads(f.read())


def read_yaml(file_path: Union[str, pathlib.Path]) -> Dict[str, Any]:
    if isinstance(file_path, pathlib.Path):
        file_path = file_path.as_posix()
    with open(file_path, 'r') as f:
        return yaml.safe_load(f.read())


def write_json(data: Optional[Dict],
               file_path: Union[str, pathlib.Path] = 'output.json') -> pathlib.Path:
    if isinstance(file_path, pathlib.Path):
        file_path = file_path.as_posix()
    with open(file_path, "w") as file:
        file.write(json.dumps(data))
    return pathlib.Path(file_path)


def write_yaml(data: Optional[Dict],
               file_path: Union[str, pathlib.Path] = 'output.yaml') -> pathlib.Path:
    if isinstance(file_path, pathlib.Path):
        file_path = file_path.as_posix()
    with open(file_path, "w") as file:
        yaml.safe_dump(data, file)
    return pathlib.Path(file_path)


__all__ = ['read_json', 'read_yaml',
           'write_json', 'write_yaml']
