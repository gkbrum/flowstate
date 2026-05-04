from functools import lru_cache
from fastapi import FastAPI, Depends, Cookie, Request, HTTPException
from starlette.middleware.sessions import SessionMiddleware
from fastapi.responses import RedirectResponse
from app.core import config 
from app.services import spotify_service
import secrets

@lru_cache
def get_settings():
    return config.Settings()

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=get_settings().api_secret_token)

#função para extrair os tokens de acesso e refresh
def get_current_user_tokens(request: Request):
    tokens = request.session.get("spotify-tokens")
    
    if tokens is None:
        raise HTTPException(status_code=303, headers={"Location": "http://127.0.0.1:8000"})
    
    return tokens     

@app.get("/login")
def login(_settings=Depends(get_settings)):
    state = secrets.token_urlsafe(16)
    
    authenticator = spotify_service.SpotifyAuthenticator(_settings)
    
    response = RedirectResponse(url=authenticator.get_authorize_url(state))
    response.set_cookie(key="spotify_auth_state", value=state, httponly=True)
    
    return response


@app.get("/callback")
def callback(state: str,
        request: Request,
        _settings=Depends(get_settings),
        code: str | None = None,
        error: str | None = None,
        cookieState: str =Cookie(default=None, alias="spotify_auth_state")
    ):
    
    if error != None:
        redirectUrl = "/?error=" + error
        
        response = RedirectResponse(url=redirectUrl, status_code= 303)
        return response
        
     
    if state == cookieState: 
        authenticator = spotify_service.SpotifyAuthenticator(_settings)
        
        tokens = authenticator.get_access_token(code)
        request.session["spotify-tokens"] = tokens
        
        return RedirectResponse(url="/playlists", status_code=303)
    
@app.get("/playlists")
def playlists(
        tokens=Depends(get_current_user_tokens),
        settings=Depends(get_settings)
    ):
    
    sp = spotify_service.SpotifyDataService(tokens, settings)
    
    return sp.get_user_playlists()