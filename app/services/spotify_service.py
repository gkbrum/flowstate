from spotipy.client import Spotify
from spotipy.cache_handler import MemoryCacheHandler
from spotipy import SpotifyOAuth
from app.core import config
from app.services import schemas

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
                "playlist-modify-private,"
                "playlist-read-collaborative"
            ),
            cache_handler=MemoryCacheHandler(), #faz com que os dados do autorizador sejam deletados da cache ao fim da execução
            open_browser=False
        )
    
    def get_authorize_url(self, state:str):
        return self.oauth.get_authorize_url(state)
    
    def get_access_token(self, code:str):
        return self.oauth.get_access_token(code, check_cache=False)

class SpotifyDataService:
    def __init__(self, tokens: dict, settings: config.Settings):
        
        #instancia um gerenciador de autenticação para a classe Spotify
        mgr = SpotifyOAuth(
            client_id=settings.spotipy_client_id,
            client_secret=settings.spotipy_client_secret,
            redirect_uri=settings.spotipy_redirect_uri,
            
            cache_handler=MemoryCacheHandler(token_info=tokens)     
        )
        
        self._client = Spotify(oauth_manager=mgr)
        
    def get_user_playlists(self):
        raw_data = self._client.current_user_playlists(limit=50)
        playlists: list[schemas.PlaylistDTO] = []
        
        for item in raw_data["items"]:
            playlist = schemas.PlaylistDTO(**item)
            playlists.append(playlist)            
        
        return playlists