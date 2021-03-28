import requests
import config

headers = {}

# Auth URL for time-limited tokens
AUTH_URL = 'https://accounts.spotify.com/api/token'

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

def get_spotify_token():
  auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': config.CLIENT_ID,
    'client_secret': config.CLIENT_SECRET,
  })
  auth_response_data = auth_response.json();
  access_token = auth_response_data['access_token']
  return(access_token)

def get_artist_info():
  # Soundgarden
  artist_id = '5xUf6j4upBrXZPg6AI4MRK'
  # pull all artists albums
  response = requests.get(BASE_URL + 'artists/' + artist_id + '/albums', 
                 headers=headers, 
                 params={'include_groups': 'album', 'limit': 50})
  artist_data = response.json()
  return artist_data

if __name__ == "__main__":
  access_token = get_spotify_token()
  headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
  }
  print(get_artist_info())