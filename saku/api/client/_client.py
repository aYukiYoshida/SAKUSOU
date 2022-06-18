# -*- coding: utf-8 -*-
from __future__ import annotations

import json
import os
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import Any, Dict, Optional, Tuple, Union
from urllib.parse import urlencode, urlunparse

import curlify
import requests

from ._utility import str_to_camel_case, str_to_snake_case


class ApiClient(object, metaclass=ABCMeta):
    EMPTY = {'request': None}  # for empty request body
    REMOVE = {'property': None}  #
    DEFAULT_HEADERS = {'content-type': 'application/json',
                       'accept': '*/*'}

    def __init__(self, base_uri: str, protocol: str = 'https',
                 default_key_case: str = 'camel'):
        '''
        args:
            base_uri: str   base uri
            protocol: str   communication protocol. Default is https.
            default_key_case: str
        '''
        self.__base_uri = base_uri
        self.__protocol = protocol
        self.__default_key_case = default_key_case

    @property
    def base_uri(self) -> str:
        return self.__base_uri

    @property
    def protocol(self) -> str:
        return self.__protocol

    @property
    def default_key_case(self) -> KeyCase:
        return self.KeyCase(self.__default_key_case)

    @classmethod
    def join_path(cls, *paths: str) -> str:
        '''
        description
            wrapper of os.path.join
        '''
        return os.path.join(*paths)

    @classmethod
    def convert_to_camel_case_keys(cls, body: Dict[str, Any]) -> Dict[str, Any]:
        return {str_to_camel_case(key) if '_' in key else key: value
                for key, value in body.items()}

    @classmethod
    def convert_to_snake_case_keys(cls, body: Dict[str, Any]) -> Dict[str, Any]:
        return {str_to_snake_case(key) : value
                for key, value in body.items()}

    def convert_to_default_case_keys(self, body: Dict[str, Any]) -> Dict[str, Any]:
        _method = {self.KeyCase.CAMEL: self.convert_to_camel_case_keys,
                   self.KeyCase.SNAKE: self.convert_to_snake_case_keys}[self.default_key_case]
        return _method(body)

    def reprocess_request_body(self, properties: Dict[str, Any],
                               defaults: Dict[str, Any],
                               convert_key: bool = False) -> Dict[str, Any]:
        ''' デフォルトのプロパティ値をすり替えたオブジェクトを再生成する
        '''
        properties = {key: properties.get(key, value)
                      for key, value in defaults.items()}
        if convert_key:
            properties = self.convert_to_default_case_keys(properties)
        return properties

    @classmethod
    def prepare_query_string(cls, query: Dict[str, str]) -> str:
        return urlencode(query=query)

    def prepare_request_url(self, path: str, parameters: Optional[str] = None,
                             query: Optional[str] = None, fragment: Optional[str] = None) -> str:
        return urlunparse((self.protocol, self.base_uri, path, parameters, query, fragment))

    @classmethod
    def prepare_request_headers(cls, headers: Dict[str, str]) -> Dict[str, str]:
        '''
        args:
            headers: Dict[str, str]      additional headers
        '''
        headers = cls.DEFAULT_HEADERS.copy()
        headers.update(headers)
        return headers

    @classmethod
    def dispatch_request(cls, url: str, method: Method,
                         request_headers: Dict[str, str],
                         request_body: Optional[Dict[str, Any]] = None,
                         upload_file: Optional[Dict[str, Tuple[str, str, str]]] = None) -> Tuple[Request, Response]:
        if request_body == cls.EMPTY:
            request_body = None
        if upload_file is None:
            data = json.dumps(request_body).encode() if not request_body is None \
                else request_body
        else:
            data = request_body  # upload file がある場合: str, bytes にしない
            _ = request_headers.pop('Content-Type')
        response = requests.request(method=str(method), url=url,
                                    data=data, headers=request_headers, files=upload_file)
        try:
            response_body = response.json()
        except json.JSONDecodeError:
            response_body = {}
        response_header = dict()
        for k, v in response.headers.items():
            try:
                response_header[k] = json.loads(v)
            except json.JSONDecodeError:
                response_header[k] = v

        return (cls.Request(url, str(method), dict(response.request.headers),
                            request_body, upload_file, curlify.to_curl(response.request)),
                cls.Response(response.status_code, response_header, response_body, response.reason))

    @abstractmethod
    def request(self):
        pass

    class Method(Enum):
        GET = auto()
        POST = auto()
        PUT = auto()
        DELETE = auto()
        PATCH = auto()

        def __str__(self):
            return self.name

    class KeyCase(Enum):
        CAMEL = 'camel'
        SNAKE = 'snake'

    @dataclass
    class Response:
        status: int
        header: Dict[str, Any]
        body: Dict[str, Any]
        reason: str

    @dataclass
    class Request:
        uri: str
        method: str
        header: Dict[str, Any]
        body: Optional[Dict[str, Any]]
        upload_file: Optional[Dict[str, Tuple[str, str, str]]]
        curl: str = 'curl --help'

__all__ = ['ApiClient']