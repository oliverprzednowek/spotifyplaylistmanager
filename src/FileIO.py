import json

PLAYLIST_FILE = "playlists.txt"
BASIC_INFO = "BASIC_INFO.json"


def addPlaylist(playlist: str):
    with open(PLAYLIST_FILE, "a") as file:
        file.write(playlist + "\n")
    print("Playlist saved")


def loadPlaylists() -> list:
    playlistLinks = []
    try:
        with open(PLAYLIST_FILE, "r") as file:
            playlistLinks = file.read().splitlines()
    except FileNotFoundError:
        print("Playlist file not found")
    return playlistLinks


def savePlaylists(playlists: list[str]):
    with open(PLAYLIST_FILE, "w") as file:
        for playlist in playlists:
            file.write(playlist + "\n")


def loadBasicInfo() -> dict:
    basicInfo = {}
    try:
        with open(BASIC_INFO, "r") as file:
            basicInfo = json.load(file)
    except FileNotFoundError:
        print("basic info file not found")
        return {}
    if not basicInfo:
        return {}
    return basicInfo
