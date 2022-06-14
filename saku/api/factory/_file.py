# -*- coding: utf-8 -*-
import pathlib
from typing import Tuple, Union

import cv2
import numpy as np

from ._string import alphanumeric_symbol

def __setup_make_file(file_path: Union[str, pathlib.Path]) -> pathlib.Path:
    if isinstance(file_path, str):
        file_path = pathlib.Path(file_path)
    output_directory = file_path.absolute().parents[0]
    if not output_directory.exists:
        output_directory.mkdir()
    return file_path.absolute()


def make_binary_file(size: int = 128,
                       file_path: Union[str, pathlib.Path] = 'output.bin') -> pathlib.Path:
    file_path = __setup_make_file(file_path)
    with open(file_path.as_posix(), "wb") as file:
        file.write(bytes(int(size)))
    return file_path


def make_ascii_file(size: int = 128,
                    file_path: Union[str, pathlib.Path] = 'output.txt') -> pathlib.Path:
    file_path = __setup_make_file(file_path)
    with open(file_path.as_posix(), "w") as f:
        f.write(alphanumeric_symbol(size))
    return file_path


def make_image_file(size: Tuple[int, int] = (128, 128),
                    file_path: Union[str, pathlib.Path] = 'output.png') -> pathlib.Path:
    file_path = __setup_make_file(file_path)
    cv2.imwrite(file_path.as_posix(), np.random.randint(0, 128, size))
    return file_path


def make_video_file(size: Tuple[int, int, int] = (128, 128, 128),
                    file_path: Union[str, pathlib.Path] = 'output.mp4') -> pathlib.Path:
    file_path = __setup_make_file(file_path)
    _image_directory = file_path.parent.joinpath(f'images')
    _image_directory.mkdir()
    image_files = [make_image_file(
        size=size[:2],
        file_path=_image_directory.joinpath(f'{str(i).zfill(8)}.png'))
        for i in range(size[2])]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video_writer = cv2.VideoWriter(file_path.as_posix(), fourcc, 20.0, size[:2])
    for image_file in image_files:
        image = cv2.imread(image_file.as_posix())
        video_writer.write(image)
        image_file.unlink()
    _image_directory.rmdir()
    return file_path

__all__ = ['make_ascii_file', 'make_binary_file',
           'make_image_file', 'make_video_file']

