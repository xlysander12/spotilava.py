import spotipy
import lavalink
from spotilavapy import exceptions
from spotipy.oauth2 import SpotifyClientCredentials

class SpotiLava:
    def __init__(self, player, *, spotify_token=None, client_id=None, client_secret=None, tracks_limit=100):
        if player is None:
            raise exceptions.InvalidPlayer(f"Lavalink player is None") # Player Not Found

        if type(player) is not lavalink.DefaultPlayer:
            raise exceptions.InvalidPlayer(f"Lavalink player not of type lavalink.DefaultPlayer [{type(player)}]")

        self._player = player

        # Auth
        if spotify_token is not None:
            self._spotify = spotipy.Spotify(auth=spotify_token)
        elif client_id is not None and client_secret is not None:
            self._spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
        else:
            raise exceptions.Forbidden("No Authentication method found (token or app)") # Auth not found
        self._limit = tracks_limit


    def get_track(self, url):
        """
        Regular Spotify API request (no transform)
        :param url:
        :return:
        """
        try:
            track = self._spotify.track(url)
        except spotipy.SpotifyException as err:
            if err.http_status == 404:
                raise exceptions.NotFound("No track found")
            else:
                raise err
        return track

    def get_playlist_tracks(self, url):
        """
        Regular Spotify API request (no transform)
        :param url:
        :return:
        """
        try:
            tracks = self._spotify.playlist_items(url, limit=self._limit)
        except spotipy.SpotifyException as err:
            if err.http_status == 404:
                raise exceptions.NotFound("No playlist found")
            else:
                raise err
        return tracks

    async def convert_track(self, url):
        """
        Convert a spotify track to a lavalink one so it can be played by it
        :param url: URL, URI or STR_URI of the track
        :return list with all tracks:
        """
        track = self.get_track(url)
        result = await self._player.node.get_tracks(f"ytsearch:{', '.join(track['artists'][i]['name'] for i in range(len(track['artists'])))} - {track['name']}")
        return result["tracks"][0]

    async def convert_playlist(self, url):
        """
        Convert a spotify playlist to a list of lavalink tracks so they can be played by it
        :param url: URL, URI or STR_URI of the track
        :return:
        """
        items = self.get_playlist_tracks(url)
        tracks = []
        for item in items["items"]:
            tracks.append(await self.convert_track(item["track"]["uri"]))

        return tracks