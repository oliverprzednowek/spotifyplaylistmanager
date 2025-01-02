import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy import SpotifyException
import itertools
from SpotifyModel import Playlist, Track


class SpotifyConnection:
    def __init__(self, basicInfo: dict):
        # initializing the spotify session
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=basicInfo.get("cid"),
                client_secret=basicInfo.get("secret"),
                redirect_uri=basicInfo.get("redirectURI"),
                scope=basicInfo.get("scope"),
            )
        )

    def __generateTrackObject(self, track: dict) -> Track:
        return Track(
            track.get("name"), track.get("artists")[0].get("name"), track.get("id")
        )

    def __combinePlaylistTracks(self, pls: list[Playlist]) -> list:
        """returns single list of all tracks in all playlists in pls
        params:
            pls -- list of playlists to combine tracks
        """

        items = [pl.getItems() for pl in pls]
        allPlaylistSongs = list(itertools.chain.from_iterable(items))

        return allPlaylistSongs

    def __getPlaylistID(self, link: str) -> str:
        """takes a playlist link and returns its id"""

        linkArr = link.strip().split("/")
        if len(linkArr) == 1 or "playlist" not in linkArr:
            return ""

        index = linkArr.index("playlist") + 1
        if len(linkArr) <= index:
            return ""

        playlistID = (
            linkArr[index]
            if "?" not in linkArr[index]
            else linkArr[index][: linkArr[index].index("?")]
        )
        return playlistID

    def getPlaylist(self, link: str):
        """takes playlist link as string, returns playlist dict if the playlist exists, empty dict if playlist does not exist"""
        id = self.__getPlaylistID(link)

        if link:
            # try/except block to make sure the playlist id is valid
            try:
                playlist = self.sp.playlist(id)
            except SpotifyException:
                print("Playlist with link %s does not exist" % link)
                return None
            else:
                tracks = self.getPlaylistTracks(id)
                return Playlist(id, playlist.get("name"), tracks)
        else:
            return None

    def getDuplicateSongs(
        self, ref: Playlist, playlists: list[Playlist]
    ) -> list[Track]:
        """return a list of duplicate songs"""
        allSongs = self.__combinePlaylistTracks(playlists)

        allRefSongs = ref.getItems()

        return [song for song in allRefSongs if song in allSongs]

    def getPlaylistTracks(self, playlistID: str) -> list[Track]:
        """
        returns list of tracks in the playlist with playlistID
        Params:
            playlistID -- playlist id to get tracks from
        """
        playlistTracks = []
        playlist = self.sp.playlist_items(playlistID)
        if not playlist:
            return []

        tracks = playlist.get("items")

        while playlist.get("next"):
            playlist = self.sp.next(playlist)
            tracks.extend(playlist.get("items"))

        for item in tracks:
            # getting the specific track from the rest of the data
            track = item.get("track")
            playlistTracks.append(self.__generateTrackObject(track))

        return playlistTracks

    def updatePlaylistTracks(self, playlist: Playlist) -> bool:
        """updates tracks in playlist parameter"""

        id = playlist.getId()
        tracks = self.getPlaylistTracks(id)

        if not tracks:
            return False

        playlist.updateTracks(tracks)
        return True

    def removeSongs(self, tracks: list[Track], playlist: Playlist) -> list[Track]:
        """remove and return songs from the playlist with id playlistID

        Params:
            tracks -- list of track objects to remove from playlist
            playlistID -- playlist id from which to remove songs
        """

        removedSongs = []
        songPages = [[]]
        # making list of blocks of 100 songs
        # worse time complexity but simpler than slicing from tail
        while tracks:
            songPages.append(tracks[:100])
            tracks = tracks[100:]

        # removing songs from each page
        for page in songPages:
            idList = [song.getId() for song in page]
            self.sp.playlist_remove_all_occurrences_of_items(
                playlist.getId(), idList, snapshot_id=None
            )
            removedSongs.extend([song for song in page])

        return removedSongs

    def validatePlaylist(self, link: str) -> bool:
        """takes playlist link as string, returns True if playlist exists else returns False"""
        id = self.__getPlaylistID(link)
        if id:
            # try/except block to make sure the playlist id is valid
            try:
                self.sp.playlist(id)
            except SpotifyException:
                print("Playlist with link %s does not exist" % link)
                return False
            else:
                return True
        else:
            return False

    def getPlaylistName(self, plid: str) -> str:
        """assumes parameter is a valid playlist id"""
        return self.sp.playlist(plid).get("name")
