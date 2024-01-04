import ui
import FileIO
from SpotifyController import SpotifyController


class Controller:
    def __init__(self):
        self.__sp = SpotifyController()

    def menu(self):
        while True:
            choice = ui.showMenu()
            match choice:
                case 1:
                    self.addPlaylist()
                case 2:
                    self.declutterPlaylist()
                case 3:
                    self.printPlaylists()
                case 4:
                    return

    def printPlaylists(self):
        if not self.__sp.getPlaylists():
            print("No playlists loaded")
            return
        print("Playlists loaded are:")
        print(*(self.__sp.getPlaylists()), sep="\n")

    def addPlaylist(self):
        playlist = ui.getPlaylist(self.__sp)
        playlistObj = self.__sp.getPlaylistObject(playlist)
        if playlistObj:
            FileIO.addPlaylist(playlist)
            self.__sp.addPlaylist(playlistObj)

    def declutterPlaylist(self) -> bool:
        if len(self.__sp.getPlaylists()) < 2:
            print("You have to load at least 2 playlists to use this tool.\n")
            return False

        playlists = ui.chooseConfig(self.__sp.getPlaylists())
        if not playlists:
            return False

        ref = playlists[0]
        otherPlaylists = playlists[1:]
        self.__sp.removeDuplicateSongs(ref, otherPlaylists)
        print("songs removed")
        return True
