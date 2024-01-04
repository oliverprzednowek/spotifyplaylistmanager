class Playlist:
    def __init__(self, plid: str = "", name: str = "", items: list["Track"] = []):
        self.__id = plid
        self.__name = name
        self.__items = items

    def __str__(self):
        return self.__name

    def getId(self):
        return self.__id

    def getName(self):
        return self.__name

    def getItems(self):
        return self.__items

    def updateTracks(self, items: list["Track"]):
        self.__items = items

    def initializePlaylist(self, plid: str, name: str, items: list["Track"]):
        self.__id = plid
        self.__name = name
        self.__items = items


class Track:
    def __init__(self, name: str = "", artist: str = "", id: str = ""):
        self.__name = name
        self.__artist = artist
        self.__id = id

    def __str__(self):
        return self.__name + " by " + self.__artist

    def __eq__(self, other):
        if isinstance(other, Track):
            return self.__id == other.__id
        return False

    def getName(self):
        return self.__name

    def getArtist(self):
        return self.__artist

    def getId(self):
        return self.__id
