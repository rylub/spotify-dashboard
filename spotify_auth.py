import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

class SpotifyAuthenticator:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect = os.getenv('SPOTIFY_REDIRECT_URI')
        self.scope = 'user-read-recently-played user-top-read user-read-private'
        self.oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.secret,
            redirect_uri=self.redirect,
            scope=self.scope,
            cache_path=".cache"
        )

    def get_auth_url(self):
        """Generate the authorization url for user to visit"""
        return self.oauth.get_authorize_url()

    def get_token_from_url(self, response_url):
        """Extract token from the callback URL"""
        if not response_url:
            print('Warning: There is no response_url')
            return None

        try:
            token_info = self.oauth.get_access_token(response_url)
            print("Success! Got authentication token")
            return token_info
        except Exception as e:
            print(f"Error getting token {e}")
            return None

    def get_authenticated_client(self):
        """Create authenticated spotify client"""
        try:
            #Step 1: Get a valid token (SpotipyOAuth handles refresh auto)
            token_info = self.oauth.get_cached_token()

            #Step 2: Check if we got a token
            if token_info:
                #Step 3: Create and return spotipy client
                return spotipy.Spotify(auth=token_info['access_token'])
            else:
                return None

        except Exception as e:
            print(f"Error creating client: {e}")
            return None

    def is_authenticated(self):
        """Check if user is already authenticated"""
        try:
            # Step 1: Try to get cached token
            cached_token = self.oauth.get_cached_token()

            # Step 2: Check if token exists and isn't expired
            if cached_token and not self.oauth.is_token_expired(cached_token):
                return True
            else:
                return False

        except:
            return False