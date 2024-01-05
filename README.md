# Spotify Playlist Manager

Spotify Playlist Manager extends Spotify's limited playlist editing tools to help users manage playlists in their Spotify library, by making API calls through Spotipy 2.0. Currently its main purpose is to remove songs from a given playlist that also appear in other playlists in the user's library through a text-based UI. I hope to implement more features in the future.

## How to use:

Follow the instructions for getting started with the spotify api here: https://developer.spotify.com/documentation/web-api/tutorials/getting-started

Create a BASIC_INFO.json file in the src folder with the following:

```json
{
    "scope": "playlist-modify-private playlist-modify-public",
    "cid": YOUR_CLIENT_ID,
    "secret": YOUR_CLIENT_SECRET,
    "redirectURI": "http://localhost:8888/callback"
}
```
Run `py main.py`. Then, follow instructions in the text-based UI.


