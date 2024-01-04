from SpotifyModel import Playlist
from SpotifyController import SpotifyController


def showMenu() -> int:
    while True:
        print("Please select from the following options:\n")
        print("1 -> add a playlist")
        print("2 -> remove duplicates")
        print("3 -> print playlists")
        print("4 -> quit program")
        choice = input()
        if choice in ["1", "2", "3", "4"]:
            return int(choice)
        print("Please enter a valid option\n")


def printStr(string: str):
    print(string)


def getPlaylist(sp: SpotifyController) -> str:
    """get a reference playlist and list of playlists from user"""
    while True:
        playlistLink = input("Enter the link to a playlist, or 0 to exit: ")
        if playlistLink == "0":
            return ""
        if sp.validatePlaylist(playlistLink):
            return playlistLink
        else:
            print("Invalid playlist")


def chooseConfig(playlists: list[Playlist]) -> list:
    """function lets users choose a config to load"""
    otherPlaylists = []
    printPlaylistNames(playlists)
    print(
        "\nEnter the number associated with the playlist to be your reference playlist, or 0 to exit: ",
        end="",
    )
    choice = getPlaylistInput(len(playlists))
    if choice == -1:
        return []
    refpl = playlists[choice]
    while True:
        print(
            "\nEnter the number associated with a playlist to check, or 0 to finish: ",
            end="",
        )
        choice = getPlaylistInput(len(playlists))
        if choice == -1:
            break
        otherPlaylists.append(playlists[choice])

    if len(otherPlaylists) == 0:
        return []

    return [refpl, *otherPlaylists]


def printPlaylistNames(playlists: list[Playlist]):
    """function to print playlist names"""
    for i, pl in enumerate(playlists):
        print("%d -> %s\n" % (i + 1, pl))


def getPlaylistInput(numPlaylists: int) -> int:
    choice = -1
    while True:
        choice = input()
        try:
            choice = int(choice)
        except ValueError:
            print("Please enter a number\n")
            continue
        else:
            int(choice)
            if 0 <= choice <= numPlaylists:
                choice -= 1
                break
            else:
                print(
                    "Please enter a number between %d, %d inclusive\n"
                    % (1, numPlaylists)
                )
                continue

    return choice


def confirmRemoval(duplicates: list) -> bool:
    print("Songs to delete are:")
    print(*duplicates, sep="\n")
    remove = input("Enter y to continue, anything else to quit: ")
    if remove == "y":
        return True
    return False
