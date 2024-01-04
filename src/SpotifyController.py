from SpotifyModel import Playlist
from SpotifyMethods import SpotifyMethods
import FileIO
import ui


class SpotifyController:
    def __init__(self):
        basicInfo = self.__loadBasicInfo()
        if not basicInfo:
            return
        self.__sp = SpotifyMethods(basicInfo)
        self.__playlists = self.__loadPlaylists()

    def __loadBasicInfo(self):
        info = FileIO.loadBasicInfo()
        if not info:
            print("Error, unable to open config file.")
            return None
        return info

    def __loadPlaylists(self) -> list:
        playlistLinks = FileIO.loadPlaylists()
        playlists = []
        invalidLinks = []

        if not playlistLinks:
            return []
        # get playlist objects for each link
        for link in playlistLinks:
            playlist = self.__sp.getPlaylist(link)
            if playlist:
                playlists.append(playlist)
            else:
                invalidLinks.append(link)

        if invalidLinks:
            FileIO.savePlaylists(
                [link for link in playlistLinks if link not in invalidLinks]
            )
        return playlists

    def getPlaylistObject(self, link: str):
        playlist = self.__sp.getPlaylist(link)
        if not playlist:
            return None
        return playlist

    def getPlaylists(self) -> list:
        return self.__playlists

    def addPlaylist(self, playlist: Playlist):
        if playlist is not None:
            self.__playlists.append(playlist)

    def hasPlaylists(self) -> bool:
        return bool(self.__playlists)

    def validatePlaylist(self, link: str) -> bool:
        return self.__sp.validatePlaylist(link)

    def removeDuplicateSongs(self, removeFrom: Playlist, playlists: list[Playlist]):
        self.__sp.updatePlaylistTracks(removeFrom)
        for pl in playlists:
            self.__sp.updatePlaylistTracks(pl)

        duplicateSongs = self.__sp.getDuplicateSongs(removeFrom, playlists)
        if not ui.confirmRemoval(duplicateSongs):
            return

        self.__sp.removeSongs(duplicateSongs, removeFrom)
        ui.printStr("Songs removed")
