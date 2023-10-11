# -*- coding: utf-8 -*-
import re


def str_to_camel_case(text: str) -> str:
    return re.sub("_(.)", lambda m: m.group(1).upper(), text.lower())

def str_to_snake_case(text: str) -> str:
    return re.sub("(.[A-Z])", lambda x: x.group(1)[0] + "_" + x.group(1)[1], text).lower()
