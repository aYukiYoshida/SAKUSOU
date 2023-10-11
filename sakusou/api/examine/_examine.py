# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple, Union


from ..client import ApiClient


class Examine(object):
    NoneType = type(None)
    EMPTY = ApiClient.EMPTY

    @classmethod
    def validate_status(cls, response: ApiClient.Response, expected: int) -> None:
        """ Validate response status code

        Args:
            response (ApiClient.Response): actual response
            expected (int): expected response status code
        """
        assert response.status == expected, f'expected: response status code is {expected}.'

    @classmethod
    def validate_body(cls, response: ApiClient.Response,
                      expected: Dict[str, Any]) -> None:
        """Validate response body

        Args:
            response (ApiClient.Response): actual response
            expected (Dict[str, Any]): expected response body
        """
        assert response.body == expected, f'expected: response body is consistent with the expected.'

    @classmethod
    def is_included(cls, response_body: Dict[str, Any], expected_keys: Iterable,
                    include: bool = True) -> None:
        '''
        note: 期待したキー以外のプロパティが含まれていても PASS する.
        '''
        for key in expected_keys:
            if include:
                assert key in response_body.keys(), \
                    f'expected: property of {key} is included in response body.'
            else:
                assert key not in response_body.keys(), \
                    f'expected: property of {key} is not included in response body.'

    @classmethod
    def is_key_consistent(cls, request_body: Dict[str, Any], expected_keys: Iterable) -> None:
        assert set(request_body.keys()) == set(expected_keys), \
            f'expected: response has to contain properties of {", ".join(expected_keys)}.'

    @classmethod
    def is_correct_type(cls, response_body: Dict[str, Any],
                        expected_types: List[Tuple[str, Union[type, Tuple[Union[type, Tuple[Any, ...]], ...]]]]):
        for key, expected_type in expected_types:
            assert isinstance(response_body.get(key), expected_type), \
                f'expected: type of {key} is {expected_type}.'

    @classmethod
    def is_member(cls, value: str, members: List[str]) -> None:
        assert value in members, \
            'expected: {} is either {}'.format(value, ' or '.join(members))
