import pytest

from torrent_client_cli.core import torrent_file_reader, bencoder
import json

def test_read_sample_torrent_file():
    torrent_file_path = "./tests/data/ubuntu-18.04.5-desktop-amd64.iso.torrent"
    with open(torrent_file_path, "rb") as f:
            torrent_file_content = f.read()
            info, _ = bencoder.decode(torrent_file_content)

    with open("./tests/data/ubuntu-18.04.5-desktop-amd64.iso.json", "w") as fout:
        fout.write(json.dumps(info, indent=4))
        
    assert type(info) == dict

