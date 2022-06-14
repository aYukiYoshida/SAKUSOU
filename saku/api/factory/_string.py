# -*- coding: utf-8 -*-

import random
import secrets
import string
import uuid

__HIRAGANA = ['あ', 'い', 'う', 'え', 'お', 'か', 'き', 'く', 'け', 'こ',
              'さ', 'し', 'す', 'せ', 'そ', 'た', 'ち', 'つ', 'て', 'と',
              'な', 'に', 'ぬ', 'ね', 'の', 'は', 'ひ', 'ふ', 'へ', 'ほ',
              'ま', 'み', 'む', 'め', 'も', 'や', 'ゆ', 'よ',
              'ら', 'り', 'る', 'れ', 'ろ', 'わ', 'を', 'ん']
__KATAKANA = ['ア', 'イ', 'ウ', 'エ', 'オ', 'カ', 'キ', 'ク', 'ケ', 'コ',
              'サ', 'シ', 'ス', 'セ', 'ソ', 'タ', 'チ', 'ツ', 'テ', 'ト',
              'ナ', 'ニ', 'ヌ', 'ネ', 'ノ', 'ハ', 'ヒ', 'フ', 'ヘ', 'ホ',
              'マ', 'ミ', 'ム', 'メ', 'モ', 'ヤ', 'ユ', 'ヨ',
              'ラ', 'リ', 'ル', 'レ', 'ロ', 'ワ', 'ヲ', 'ン']

def alphanumeric(n: int) -> str:
    '''指定された文字数のランダムな英数字の文字列を生成する
    '''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))

def alphanumeric_symbol(n: int) -> str:
    ''' 指定された文字数のランダムな英数字+記号の文字列を生成する
    '''
    return ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=n))

def jp_alphabet(n: int) -> str:
    '''指定された文字数のランダムなひらがなとカタカナの文字列を生成する
    '''
    return ''.join(random.choices(__HIRAGANA+__KATAKANA, k=n))

def decimal(digit: int) -> str:
    '''指定された文字数のランダムな数字の文字列を生成する
    '''
    return str(random.randint(10**(digit-1), 10**digit-1))

def hexadecimal(n: int) -> str:
    '''指定された文字数のランダムな16進数の文字列を生成する
    '''
    return secrets.token_hex(int(n*0.5))

def uuid() -> str:
    return str(uuid.uuid4())

def ip_address() -> str:
    return '.'.join([str(random.randint(1, 2**8)-1) for _ in range(4)])

def email_address(n: int, domain:str='testing.com') -> str:
    n = n - 1 - len(domain)
    account = ''.join(random.choices(string.ascii_letters + string.digits + '._+-', k=n))
    return account + '@' + domain

__all__ = ['alphanumeric', 'alphanumeric_symbol', 'jp_alphabet',
           'decimal', 'hexadecimal', 'uuid',
           'ip_address', 'email_address']