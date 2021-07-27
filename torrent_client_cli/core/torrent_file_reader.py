from . import bencoder

# Open and parse a .torrent file


def read_torrent_file(torrent_file_path: str):
    """
    Open and parse a .torrent file
    """
    torrent_file_information = None
    try:
        with open(torrent_file_path, "rb") as f:
            torrent_file_content = f.read()
            torrent_file_information, _ = bencoder.decode(torrent_file_content)
    except IOError:
        print("Error: File not found")
    except ValueError:
        print("Error: Invalid .torrent file")

    return torrent_file_information
