"""
Bittorrent  bencoding implementation as per BEP-003 specification.
Consult the BEP-003 specification for details. http://www.bittorrent.org/beps/bep_0003.html 
>>> encode(42)
b'i42e'
>>> decode(b'i42e')
(42, b'')
"""


from typing import Any, Dict, List, Tuple

"""
    Encoder code block
"""


def _encode_int(n: int) -> bytes:
    """
    Encodes an integer into a bencoded string.
    """
    return f"i{n}e".encode("utf-8")


def _encode_string(s: str) -> bytes:
    """
    Encode a python string into a bencoded string.
    """
    return f"{len(s)}:{s}".encode("utf-8")


def _encode_list(l: List) -> bytes:
    """
    Encode a python list into a bencoded string.
    """
    encoded_list = b""
    for element in l:
        encoded_list += encode(element)
    return b"l" + encoded_list + b"e"


def _encode_dict(d: Dict) -> bytes:
    """
    Encode a python dictionary into a bencoded string.
    """
    encoded_dict = b""
    for key, value in d.items():
        encoded_dict += encode(key)
        encoded_dict += encode(value)
    return b"d" + encoded_dict + b"e"


def encode(value) -> bytes:
    """
    Encodes a python object into a bencoded string.
    """
    if isinstance(value, str) or isinstance(value, bytes):
        return _encode_string(value)
    if isinstance(value, int):
        return _encode_int(value)
    if isinstance(value, list):
        return _encode_list(value)
    if isinstance(value, dict):
        return _encode_dict(value)
    raise ValueError(f"cannot encode value of type {type(value)}")


"""
    Decode code block
"""


def _decode_int(s: str) -> Tuple[int, str]:
    """
    Decode a bencoded int into a python int object.
    """
    i = 1
    token_text = ""
    while True:
        if s[i] == "e":
            break
        token_text += s[i]
        i += 1
    t = int(token_text)
    return t, s[i + 1 :]


def _decode_string(s: str) -> Tuple[str, str]:
    """
    Decode a bencoded string into a python string object.
    """
    colon_pos = s.find(":")
    length = int(s[:colon_pos])
    t = s[colon_pos + 1 : colon_pos + 1 + length]
    s = s[colon_pos + 1 + length :]

    return t, s


def _decode_list(s) -> Tuple[List, str]:
    """
    Decode a bencoded list into a python list object.
    """
    if s[0] != "l":
        raise ValueError("invalid list encoding")
    s = s[1:]
    result = []
    while s:
        if s[0] == "e":
            s = s[1:]
            break
        t, s = decode(s)
        result.append(t)

    return result, s


def _decode_dict(s: str) -> Tuple[Dict, str]:
    """
    Decode a bencoded dictionary into a python dictionary object.
    """
    if s[0] != "d":
        raise ValueError("invalid dict encoding")
    s = s[1:]
    result = {}
    while s:
        if s[0] == "e":
            s = s[1:]
            break
        key, s = decode(s)
        value, s = decode(s)
        result[key] = value
    return result, s


def decode(s) -> Tuple[Any, str]:
    """
    Decode a bencoded string into a python object.
    """
    if isinstance(s, bytes):
        s = s.decode("ANSI")
    if s[0] == "i":
        return _decode_int(s)
    if s[0] == "l":
        return _decode_list(s)
    if s[0] == "d":
        return _decode_dict(s)
    if s[0] in "0123456789":
        return _decode_string(s)
    raise ValueError("cannot decode value")
