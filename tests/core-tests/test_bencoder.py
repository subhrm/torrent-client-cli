import pytest
from torrent_client_cli.core import bencoder


# Test becoder


@pytest.mark.parametrize(
    ("data", "encoded_str"),
    [
        ("spam", b"4:spam"),
        (3, b"i3e"),
        (-3, b"i-3e"),
        (0, b"i0e"),
        (["spam", "eggs"], b"l4:spam4:eggse"),
        ({"cow": "moo", "spam": "eggs"}, b"d3:cow3:moo4:spam4:eggse"),
        ({"spam": ["a", "b"]}, b"d4:spaml1:a1:bee"),
    ],
)
def test_encode_using_bep003_examples(data, encoded_str):

    assert bencoder.encode(data) == encoded_str


@pytest.mark.parametrize(
    ("data", "encoded_str"),
    [
        ("spam", b"4:spam"),
        (3, b"i3e"),
        (-3, b"i-3e"),
        (0, "i0e"),
        (["spam", "eggs"], b"l4:spam4:eggse"),
        ({"cow": "moo", "spam": "eggs"}, b"d3:cow3:moo4:spam4:eggse"),
        ({"spam": ["a", "b"]}, b"d4:spaml1:a1:bee"),
    ],
)
def test_decode_using_bep003_examples(data, encoded_str):

    decoded, _ = bencoder.decode(encoded_str)
    assert type(decoded) == type(data)
    assert str(decoded) == str(data)


@pytest.mark.parametrize(
    "obj",
    [
        0,
        10000,
        -1,
        -263263263,
        "hello",
        [],
        [1, 2, 3],
        ["xyz", "abc"],
        ["xyz", "abc", 100, 200],
        {},
        {1: 2},
        {1: 2, 3: 4},
        "abc",
    ],
)
def test_encoder_decoder_chain(obj):
    encoded = bencoder.encode(obj)
    decoded, residual = bencoder.decode(encoded)

    print(obj, encoded, decoded, residual)

    assert residual == ""
    if type(obj) in (list, dict):
        assert type(obj) == type(decoded)
        assert str(obj) == str(decoded)
    else:
        assert decoded == obj
