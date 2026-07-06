class Releases:
    def __init__(self, discogID = 0, artists = [], year = 0, labels = [], genres = [], tracklist = [], imageURL = None):
        self._discogID = discogID
        self._artists = artists
        self._year = year
        self._labels = labels
        self._genres = genres
        self._tracklist = tracklist
        self._image = imageURL

    