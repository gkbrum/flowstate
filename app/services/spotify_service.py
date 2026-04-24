from spotipy.cache_handler import MemoryCacheHandler
from spotipy import SpotifyOAuth
from app.core import config 

class SpotifyAuthenticator:
    def __init__(self, settings: config.Settings):
        self.client_id = settings.spotipy_client_id
        self.client_secret = settings.spotipy_client_secret
        self.redirect_uri = settings.spotipy_redirect_uri
        
        self.oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=(
                "playlist-read-private,"
                "playlist-modify-public,"
                "playlist-modify-private"
            ),
            cache_handler=MemoryCacheHandler(),
            open_browser=False
        )
    
    def get_authorize_url(self, state:str):
        return self.oauth.get_authorize_url(state)
    
    def get_access_token(self, code:str):
        return self.oauth.get_access_token(code, check_cache=False)
